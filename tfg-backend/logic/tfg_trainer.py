# ==============================================================================
# PIPELINE DE ENTRENAMIENTO Y EVALUACIÓN PROSPECTIVA (MACHINE LEARNING)
# TFG: Análisis y predicción del rendimiento en corredores
# Autor: Jaume Antoni Soler Sánchez
# ==============================================================================

import os 
import sys
import joblib
import argparse 
import json 
import numpy as np 
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
from sqlalchemy import create_engine, text

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.metrics import slope

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('--user_id', type=int, default=3)
parser.add_argument('--window', type=int, default=15)
args = parser.parse_args()

# Inicialización de constantes del sistema, configuraciones biométricas e hiperparámetros del modelo matemático
DATABASE_URL = os.getenv("DATABASE_URL")
USER_ID = args.user_id
WINDOW = args.window
TARGETS = ['t_5k', 't_10k', 't_21k', 't_42k']
TARGET_LABELS = ['5k', '10k', '21k', '42k']
RIEGEL_EXP = 1.06

def riegel(t, d, d2, exp=RIEGEL_EXP):
    """
    Implementa el modelo cinético clásico de Riegel para la estimación de marcas.
    Calcula el tiempo equivalente (t2) para una distancia objetivo (d2) en base a un rendimiento previo (t, d).
    """
    if not t or not d or d <= 0:
        return np.nan
    return t*(d2/d) ** exp

def fmt_time(seconds): 
    """Abstrae la conversión de magnitudes temporales de segundos brutos a cadenas formateadas (HH:MM:SS)."""
    if np.isnan(seconds) or seconds <= 0:
        return "N/A"
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    return f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"

# ==============================================================================
# FASE 1: EXTRACCIÓN DE DATOS Y CONEXIÓN CON EL MOTOR DE PERSISTENCIA (POSTGRESQL)
# ==============================================================================
engine = create_engine(DATABASE_URL)
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    user_row = conn.execute(
        text('SELECT max_hr, rest_hr, weight, gender, level, custom_zones FROM "Users" WHERE user_id = :uid'), {"uid": USER_ID}
    ).fetchone()

    if not user_row:
        print(f"user {USER_ID} not found.")
        exit(0)
    # Control de fallos e imputación de valores biométricos por defecto en caso de registros nulos
    USER_MAX_HR = int(user_row.max_hr) if user_row.max_hr else 195
    USER_REST_HR = int(user_row.rest_hr) if user_row.rest_hr else 60
    USER_WEIGHT = float(user_row.weight) if user_row.weight else None
    USER_GENDER = user_row.gender or "M"
    USER_LEVEL = user_row.level or "amateur"
    HR_RESERVE = USER_MAX_HR - USER_REST_HR
    CUSTOM_ZONES = user_row.custom_zones

    print(f"max_hr={USER_MAX_HR}  rest_hr={USER_REST_HR}  weight={USER_WEIGHT}  gender={USER_GENDER}  level={USER_LEVEL}    HR Reserve (Karvonen): {HR_RESERVE} bpm")
    if CUSTOM_ZONES:
        print(f"   Custom zones defined: {len(CUSTOM_ZONES)} zones — will use these for zone classification")
    else:
        print(f"   No custom zones — using %HRR Karvonen method")

    # Ingesta y filtrado SQL de los metadatos globales de actividades macro (Solo carreras válidas de más de 500m)
    df_act = pd.read_sql(text("""
    SELECT
        activity_id, 
        type, 
        distance, 
        mov_time,
        elp_time,
        workout_density,
        date, avg_heartrate,
        max_heartrate, 
        avg_pace, 
        max_pace, 
        positive_slope, 
        perceived_effort
    FROM "Activity"
    WHERE user_id = :uid
        AND type IN ('Run', 'Virtual Run')
        AND distance > 500
        AND mov_time > 0
    ORDER BY date ASC
"""), conn, params={'uid': USER_ID})
    # Consulta analítica de agregación temporal sobre la tabla de telemetría por segundo (ActivityStream)
    df_stream = pd.read_sql(text("""
        SELECT
            s.activity_id,
            AVG(s.heartrate) AS stream_hr_mean,
            STDDEV(s.heartrate) AS stream_hr_std,
            MAX(s.heartrate) AS stream_hr_max,
            AVG(s.current_speed) AS stream_speed_mean,
            STDDEV(s.current_speed) AS stream_speed_std,
            MAX(s.current_speed) AS stream_speed_max,
            AVG(s.grade) AS stream_grade_mean,
            STDDEV(s.grade) AS stream_grade_std,
            SUM(CASE WHEN s.grade > 0 THEN s.grade ELSE 0 END) AS stream_elev_gain
        FROM "ActivityStream" s
        JOIN "Activity" a ON s.activity_id = a.activity_id
        WHERE a.user_id = :uid
            AND a.type IN ('Run', 'VirtualRun')                               
        GROUP BY s.activity_id
    """), conn, params={'uid': USER_ID})

    print(f"Activities: {len(df_act)}")
    print(f"Activities with streams: {len(df_stream)}")
# Consolidación de ambos subconjuntos de datos mediante un Left Join por el identificador de la actividad
df = df_act.merge(df_stream, on='activity_id', how='left')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# ==============================================================================
# FASE 2: INGENIERÍA DE VARIABLES (FEATURE ENGINEERING) BIOMÉTRICAS Y DE CARGA
# ==============================================================================
df['days_since_last'] = df['date'].diff().dt.days.fillna(7)
df['elev_per_km'] = df['positive_slope'] / (df['distance'] / 1000).replace(0, np.nan)
df['hr_effort_ratio'] = df['avg_heartrate'] / df['max_heartrate'].replace(0, np.nan)
df['speed_ms'] = 1000 / (df['avg_pace'] * 60).replace(0, np.nan)
# Normalización matemática de la intensidad cardíaca basada en el porcentaje de la FC de Reserva (%HRR)
df['hrr_pct'] = (df['avg_heartrate'] - USER_REST_HR) / HR_RESERVE
df['hrr_max_pct'] = (df['max_heartrate'] - USER_REST_HR) / HR_RESERVE
df['hrr_pct'] = df['hrr_pct'].clip(0,1)
df['hrr_max_pct'] = df['hrr_max_pct'].clip(0,1)
# Asignación discreta de zonas de carga de entrenamiento (Custom vs Fallback de Karvonen)
if CUSTOM_ZONES:
    zone_ranges = sorted(CUSTOM_ZONES, key=lambda z: z['min'])

    def hr_zone_custom(avg_hr):
        for i, z in enumerate(zone_ranges):
            if z['min'] <= avg_hr <= z['max']:
                return i+1
        if avg_hr < zone_ranges[0]['min']:
            return 1
        return len(zone_ranges)
    
    df['hr_zone'] = df['avg_heartrate'].apply(hr_zone_custom)
    zone_method = "custome_zones (user_defined)"
else:
    def hr_zone_karvonen(hrr_pct):
        if hrr_pct < 0.50: return 1
        if hrr_pct < 0.60: return 2
        if hrr_pct < 0.70: return 3
        if hrr_pct < 0.80: return 4
        return 5
    
    df['hr_zone'] = df['hr' \
    'r_pct'].apply(hr_zone_karvonen)
    zone_method = "%HRR Karvonen (fallback)"

print(f"HR zone method: {zone_method}")
print(f"Zone distribution: \n{df['hr_zone'].value_counts().sort_index().to_dict()}")
# Modelado del TRIMP (Training Impulse Score) ponderado por variables antropométricas y factor de género de la escala de Banister
df['trimp_score'] = (df['mov_time'] / 60) * df['hrr_pct']
if USER_WEIGHT: df['trimp_score'] = df['trimp_score'] * USER_WEIGHT
df['trimp_score'] = df['trimp_score'] * (1.67 if USER_GENDER == 'F' else 1.92)
# Generación automática de variables objetivo (Targets) mediante proyecciones empíricas generalizadas de Riegel
df['t_5k'] = df.apply(lambda r: riegel(r['mov_time'], r['distance'], 5000), axis=1)
df['t_10k'] = df.apply(lambda r: riegel(r['mov_time'], r['distance'], 10000), axis=1)
df['t_21k'] = df.apply(lambda r: riegel(r['mov_time'], r['distance'], 21097), axis=1)
df['t_42k'] = df.apply(lambda r: riegel(r['mov_time'], r['distance'], 42195), axis=1)

print('Riegel: sample most recent activity')
last = df.iloc[-1]
print(f"Distance: {last['distance'] / 1000:2f} km MovTime: {fmt_time(last['mov_time'])}")
print(f"5k: {fmt_time(last['t_5k'])}  \
      10k: {fmt_time(last['t_10k'])} \
      21k: {fmt_time(last['t_21k'])}  \
      42k: {fmt_time(last['t_42k'])}")


ACTIVITY_FEATURES = [
    # Activity summary
    'distance', 'mov_time', 'workout_density',
    'avg_heartrate', 'max_heartrate', 'avg_pace', 'max_pace',
    'positive_slope', 'elev_per_km', 'hr_effort_ratio',
    'speed_ms', 'perceived_effort', 'days_since_last',
    # HR Reserve (Karvonen) 
    'hrr_pct', 'hrr_max_pct', 'hr_zone', 'trimp_score',
    # Stream aggregates
    'stream_hr_mean', 'stream_hr_std', 'stream_hr_max',
    'stream_speed_mean', 'stream_speed_std', 'stream_speed_max',
    'stream_grade_mean', 'stream_grade_std', 'stream_elev_gain',
]
 
for col in ACTIVITY_FEATURES:
    if col not in df.columns:
        df[col] = np.nan

records_ml = []
records_riegel = []

# ==============================================================================
# FASE 3: CONSTRUCCIÓN DE MATRICES TEMPORALES (VENTANAS DESLIZANTES / TIME WINDOWS)
# ==============================================================================
for i in range(WINDOW, len(df)):
    window = df.iloc[i - WINDOW: i]
    target_row = df.iloc[i]

    if any(np.isnan(target_row[t]) for t in TARGETS):
        continue
    # Generación de la línea base competitiva (Riegel baseline) tomando el mejor ritmo dentro de la ventana de entrenamiento
    best = window.loc[window['avg_pace'].idxmin()]
    records_riegel.append({
        'riegel_5k': riegel(best['mov_time'], best['distance'], 5000),
        'riegel_10k': riegel(best['mov_time'], best['distance'], 10000),
        'riegel_21k': riegel(best['mov_time'], best['distance'], 21097),
        'riegel_42k': riegel(best['mov_time'], best['distance'], 42195),
        't_5k': target_row['t_5k'],
        't_10k': target_row['t_10k'],
        't_21k': target_row['t_21k'],
        't_42k': target_row['t_42k'],
    })

    feat = {}
    for col in ACTIVITY_FEATURES:
        vals = window[col].values.astype(float)
        feat[f'{col}_mean'] = np.nanmean(vals)
        feat[f'{col}_std'] = np.nanstd(vals)
        feat[f'{col}_min'] = np.nanmin(vals)
        feat[f'{col}_max'] = np.nanmax(vals)
        feat[f'{col}_trend'] = slope(vals)
    # Cuantificación agregada de variables de carga acumulativa (Volumen de Kilómetros, Horas, Estrés TRIMP e Índices de Consistencia)
    feat['load_total_km'] = window['distance'].sum() / 1000
    feat['load_total_time_h'] = window['mov_time'].sum() / 3600
    feat['load_total_elevation'] = window['positive_slope'].sum()
    feat['load_avg_density'] = window['workout_density'].sum()
    feat['load_total_trimp'] = window['trimp_score'].sum()
    feat['load_avg_trimp'] = window['trimp_score'].mean()
    feat['load_trimp_trend'] = slope(window['trimp_score'].values)
    feat['recent_form_delta'] = window.iloc[-5:]['speed_ms'].mean() - window.iloc[:10]['speed_ms'].mean()
    feat['pace_consistency'] = 1- (window['avg_pace'].std() / window['avg_pace'].mean())
    feat['avg_days_between'] = window['days_since_last'].mean()
    feat['total_rest_days'] = window['days_since_last'].sum()

    for t in TARGETS:
        feat[t] = target_row[t]

    records_ml.append(feat)
    df_ml = pd.DataFrame(records_ml)
    df_riegel = pd.DataFrame(records_riegel)
# Umbral crítico de seguridad estadística para poder entrenar y segmentar los modelos predictivos
if len(df_ml) < 10: exit(1)

split = int(len(df_ml) * 0.8)
feature_cols = [c for c in df_ml.columns if c not in TARGETS]

X_train = df_ml[feature_cols].iloc[:split]
X_test = df_ml[feature_cols].iloc[split:]
y_train = df_ml[TARGETS].iloc[:split]
y_test = df_ml[TARGETS].iloc[split:]

imputer = SimpleImputer(strategy='median')
X_train_imp = imputer.fit_transform(X_train)
X_test_imp = imputer.transform(X_test)
# ==============================================================================
# FASE 4: ENTRENAMIENTO DEL MODELO DE MACHINE LEARNING MULTI-SALIDA (RANDOM FOREST)
# ==============================================================================
model =  MultiOutputRegressor(RandomForestRegressor(
    n_estimators=300,
    max_depth=8,
    min_samples_split=3,
    min_samples_leaf=2,
    max_features='sqrt',
    random_state=42,
    n_jobs=1
))
model.fit(X_train_imp, y_train)
# ==============================================================================
# FASE 5: EVALUACIÓN DE MÉTRICAS DE RENDIMIENTO Y CONTRASTE COMPARATIVO (VALIDACIÓN)
# ==============================================================================
print('riegel baseline vs random forest')
y_pred = model.predict(X_test_imp)
riegel_test = df_riegel.iloc[split:]

results = []
for i, (target, label) in enumerate(zip(TARGETS, TARGET_LABELS)):
    mae_ml = mean_absolute_error(y_test.iloc[:, i], y_pred[:,i])
    r2_ml = r2_score(y_test.iloc[:, i], y_pred[:,i])
    riegel_col = f'riegel_{label}'
    mae_riegel = mean_absolute_error(riegel_test[target], riegel_test[riegel_col])
    improvement = ((mae_riegel - mae_ml) / mae_riegel) * 100
    winner = "ML" if mae_ml < mae_riegel else "Riegel"

    results.append({
        'distance': label,
        'mae_riegel_min': mae_riegel / 60,
        'mae_ml_min': mae_ml / 60,
        'r2_ml': r2_ml,
        'improvement_pct': improvement,
        'winner': winner
    })

    print(f"{label} \
        Riegel MAE:  {mae_riegel/60:6.1f} min \
        ML MAE:      {mae_ml/60:6.1f} min   R2: {r2_ml:.3f} \
        Difference:  {improvement:+.1f}%  → {winner} wins")

# Extracción de la importancia de características agregada (Feature Importance) promediando los estimadores del bosque
print('Top 15 feature importances')
importances = np.mean([e.feature_importances_ for e in model.estimators_], axis=0)
feat_imp = pd.Series(importances, index=feature_cols).sort_values(ascending=False)
for feat, imp in feat_imp.head(15).items():
    bar = '🟩' * int(imp*200)
    print(f'{feat:<35} {imp:.4f} {bar}')

model_data = {
    'model': model,
    'imputer': imputer,
    'feature_cols': feature_cols,
    'target_labels': TARGET_LABELS,
    'user_metadata': {
        'max_hr': USER_MAX_HR,
        'rest_hr': USER_REST_HR,
        'weight': USER_WEIGHT
    }
}

DISTANCES = [
    {'km': 5, 'label': '5k', 'meters': 5000},
    {'km': 10, 'label': '10k', 'meters': 10000},
    {'km': 21.1, 'label': '21k', 'meters': 21097},
    {'km': 42.2, 'label': '42k', 'meters': 42195},
]

last_window_feat = imputer.transform(X_test.iloc[-1:])
last_pred = model.predict(last_window_feat)[0]
maes = [float(mean_absolute_error(y_test.iloc[:,i], y_pred[:,i])) for i in range(4)]

ml_points = []
for i, d in enumerate(DISTANCES):
    t = round(last_pred[i])
    mae_i = round(maes[i])
    ml_points.append({
        'distance': d['km'],
        'time': t,
        'confidence_range': [max(0, t - mae_i), t + mae_i]
    })

last_window_df = df.iloc[-WINDOW:]
best_idx = last_window_df['avg_pace'].idxmin()
best_act = last_window_df.loc[best_idx]

riegel_points = []
for d in DISTANCES:
    t = riegel(best_act['mov_time'], best_act['distance'], d['meters'])
    if not np.isnan(t):
        riegel_points.append({'distance': d['km'], 'time': round(t)})

BRACKETS = [
    {'km': 5, 'min_m': 4500, 'max_m': 5500, 'target': 5000},
    {'km': 10, 'min_m': 9000, 'max_m': 11000, 'target': 10000},
    {'km': 21.1, 'min_m': 19000, 'max_m': 23000, 'target': 21097},
    {'km': 42.2, 'min_m': 38000, 'max_m': 46000, 'target': 42195},
]

user_bests = []
for b in BRACKETS:
    bracket_runs = df[(df['distance'] >= b['min_m']) & (df['distance'] <= b['max_m'])]
    
    if bracket_runs.empty: continue

    bracket_runs = bracket_runs.copy()
    bracket_runs['normalized_time'] = bracket_runs.apply(
        lambda r: riegel(r['mov_time'], r['distance'], b['target']), axis=1
    )
    best_run = bracket_runs.loc[bracket_runs['normalized_time'].idxmin()]
    date_str = best_run['date'].strftime('%Y-%m-%d') if hasattr(best_run['date'], 'strftime') else str(best_run['date'])[:10]
    user_bests.append({
        'distance': b['km'],
        'time': round(best_run['mov_time']),
        'date': date_str
    })

metrics = []
for i, (r, mae_i) in enumerate(zip(results, maes)):
    metrics.append({
        'distance': r['distance'],
        'mae_seconds': round(mae_i),
        'mae_minutes': round(mae_i / 60, 1),
        'r2': round(r['r2_ml'], 4),
        'winner': r['winner'],
        'riegel_mae_seconds': round(r['mae_riegel_min'] * 60),
        'riegel_mae_minutes': round(r['mae_riegel_min'], 1)
    })

avg_r2 = np.mean([m['r2'] for m in metrics])
avg_mae = np.mean([m['mae_seconds'] for m in metrics])
# ==============================================================================
# FASE 6: AUDITORÍA Y ALMACENAMIENTO DE RESULTADOS EN BASE DE DATOS Y SERIALIZACIÓN
# ==============================================================================
with engine.begin() as conn:
    conn.execute(
        text("""
            INSERT INTO "ModelAnalysis" (
                user_id, model_version, ml_points, riegel_curve, user_bests, model_metrics, runs_used, train_samples, test_samples, r2_avg, mae_avg
            ) VALUES (
                :uid, :version, :ml_pts, :riegel, :bests, :metrics, :runs, :train, :test, :r2, :mae 
            )
        """),{
            'uid': USER_ID,
            'version': 'running_model_v1_may',
            'ml_pts': json.dumps(ml_points),
            "riegel": json.dumps({
                "exponent": RIEGEL_EXP,
                "points": riegel_points
            }),
            "bests": json.dumps(user_bests),
            "metrics": json.dumps(metrics),
            "runs": len(df),
            "train": len(X_train),
            "test": len(X_test),
            "r2": float(avg_r2),
            "mae": float(avg_mae)
        }
    )
# Serialización persistente binaria del binomio Modelo-Imputador en la carpeta de artefactos estáticos
joblib.dump(model_data, 'artifacts/running_model_v1_may.pkl')