# ==============================================================================
# MOTOR DE PROCESAMIENTO BIOMÉTRICO, TRANSFORMACIÓN Y MÉTRICAS DERIVADAS
# TFG: Análisis y predicción del rendimiento en corredores
# Autor: Jaume Antoni Soler Sánchez
# ==============================================================================


from logic.db_utils import activity_user, get_max_ef_index, get_max_hr, get_user_from_id, sql_commit, user_stats
from datetime import datetime
import pandas as pd
import numpy as np
from scipy.stats import linregress
import math

def calculate_trimp(duration_sec, avg_hr, max_hr, rest_hr=60, gender='male'):
    """
    Calcula el Impulso de Entrenamiento (TRIMP Score) mediante el modelo matemático de Banister.
    Pondera de forma exponencial la duración in-intensity según la deriva cardíaca de reserva.
    """
    if not (avg_hr and max_hr and rest_hr): return 0
    
    duration_min = duration_sec / 60
    # Intensidad relativa (Delta HR)
    delta_hr = (avg_hr - rest_hr) / (max_hr - rest_hr)
    
    # Constantes según género
    s = 1.92 if gender == 'male' else 1.86
    factor = 0.64 if gender == 'male' else 0.86
    
    trimp = duration_min * delta_hr * factor * math.exp(s * delta_hr)
    return round(trimp, 1)


def speed_to_pace(speed):
    """Transforma magnitudes de velocidad lineal (m/s) al sistema métrico de ritmo deportivo (min/km)."""
    if speed is None or speed <= 0.8: 
        return '00:00'

    pace_decimal = 16.6667 / speed
    if pace_decimal > 12.0: 
        return '00:00'

    minutes = int(pace_decimal)
    seconds = round((pace_decimal - minutes) * 60)
    if seconds == 60:
        minutes += 1
        seconds = 0
        
    return f"{minutes:02d}:{seconds:02d}"

def seconds_to_hrs(sec):
    """Abstrae la conversión de segundos brutos a formato extendido cronológico de pantalla (HH:MM:SS)."""
    hour = sec // 3600
    minutes = sec % 3600 // 60
    seconds = minutes % 60
    if int(hour) == 0 : return f"{int(minutes):02d}:{int(seconds):02d}"
    
    return f"{int(hour):02d}:{int(minutes):02d}:{int(seconds):02d}"

def seconds_to_min(sec):
    """Abstrae la conversión de segundos brutos a formato intermedio de pantalla (MM:SS)."""
    minutes = sec // 60
    seconds = sec % 60
    return f"{int(minutes):02d}:{int(seconds):02d}"

def calculate_elevation_gain(list):
    """
    Calcula el desnivel positivo acumulado real aplicando un filtro de umbral (Histeresis).
    Mitiga el ruido de medición instrumental y las oscilaciones barométricas menores a 0.5 metros.
    """
    alt = [list[0]]
    threshold = 0.5 
    el = 0

    for l in list:
        diff = l - alt[-1]
        if diff > threshold:
            el = el+ diff
        alt.append(l)
    return round(el, 2)

def get_max_heartrate(age):
    """Determina la FC Máxima basal teórica estimada mediante la ecuación clásica de Fox y Haskell."""
    return (220-age)

def format_date_human(dt):
    """Transforma objetos de fecha en cadenas literales antropocéntricas legibles en castellano."""
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    nombre_dia = days[dt.weekday()]
    dia_num = dt.day
    nombre_mes = months[dt.month - 1]
    
    return f"{nombre_dia}, {dia_num} de {nombre_mes}"

def format_short_date(dt):
    """Serializa la estampa cronológica en formato estándar de barra europeo."""
    return dt.strftime('%d/%m/%Y')

def get_age_from_date(date):
    """Calcula la edad cronológica exacta cruzando la fecha corriente frente al nacimiento del atleta."""
    today = datetime.now()
    age = today.year - date.year
    if (today.month, today.day) < (date.month, date.day):
        age -= 1
    return age
    
def distance_to_km(meters):
    """Normaliza distancias transformando metros brutos a kilómetros escalados."""
    return round(meters/1000, 2)

def stats_90(user_id):
    """Efectúa la extracción analítica de las líneas base macro del corredor en la ventana de 90 días."""
    stats = user_stats(user_id)
    if not stats or stats.avg_duration is None:
        return None
    return {
        'duration_baseline': stats.avg_duration, 
        'hr_baseline': stats.avg_hr,
        'distance_baseline': stats.avg_distance
    }

def max_ef_index(user_id):
    """Extrae el índice máximo de eficiencia cardiovascular registrado por el corredor."""
    ef = get_max_ef_index(user_id)
    if ef is None:
        return 1.0
    return ef

# ==============================================================================
# PIPELINE DE CONVERSIÓN DE CAPAS (DATA TRANSFER OBJECTS - DTOs)
# ==============================================================================
def activity_dto(activity, user_id, zone_time = ''):
    return {
        'activity_id': activity.activity_id,
        'type': activity.type,
        'title': activity.title,
        'distance_km': distance_to_km(activity.distance),
        'date_raw': activity.date.isoformat(timespec='seconds'),
        'date_human': format_date_human(activity.date),
        'training_metrics': {
            'trimp': calculate_trimp(
                activity.mov_time, 
                activity.avg_heartrate, 
                get_max_hr(user_id)
            ),
            'workout_density': activity.workout_density,
        },
        'duration': {
            'seconds': activity.mov_time,
            'formatted': seconds_to_hrs(activity.mov_time)
        },
        'heartrate': {
            'avg': activity.avg_heartrate,
            'max': activity.max_heartrate,
        },
        'pace': {
            'avg_raw': activity.avg_pace,
            'max_raw': activity.max_pace,
            'avg_formatted': speed_to_pace(activity.avg_pace),
            'max_formatted': speed_to_pace(activity.max_pace)
        },
        'elevation': {
            'gain': activity.positive_slope,
            'unit': 'm'
        },
        'position': {
            'lat': activity.start_lat,
            'lng': activity.start_lng
        },
        'zones': zone_time,
        'perceived_effort': activity.perceived_effort or '',
        'stats_90d': stats_90(user_id),
        'max_ef_index': max_ef_index(user_id)
    }


def activity_stream_dto(streams):
    return {
        'timestamp': streams.timestamp,
        'altitude': streams.altitude,
        'pace': {
            'raw': streams.current_speed,
            'formatted': speed_to_pace(streams.current_speed)
        },
        'distance_m': streams.distance,
        'grade': streams.grade,
        'heartrate': streams.heartrate,
        'position':{
            'lat': streams.latitude,
            'lng': streams.longitude
        }
    }

def prediction_dto(prediction):
    return {
        'last_activity_id': prediction.last_activity_id,
        'created_at': prediction.created_at,
        'pred': {
            '5k': prediction.pred_5k,
            '10k': prediction.pred_10k,
            '21k': prediction.pred_21k,
            '42k': prediction.pred_42k,
        },
        'version': prediction.model_version,
        'mae': prediction.mae or 'Not enought activities',
    }

def model_dto(model):
    return {
        'model_version': model.model_version,
        'ml_points': model.ml_points,
        'riegel_curve': model.riegel_curve,
        'user_bests': model.user_bests,
        'model_metrics': model.model_metrics,
        'runs_used': model.runs_used,
        'train_samples': model.train_samples,
        'r2_avg': model.r2_avg,
        'mae_avg': model.mae_avg
    }


def get_segments_data(streams_list):
    """
    Segmenta la serie temporal de la actividad en 5 bloques proporcionales homogéneos.
    Analiza la cinética de potencia, ratios de eficiencia y la deriva cardiovascular acumulada.
    """
    if not streams_list:
        return {'explosive': [0]*5, 'efficiency': [0]*5, 'decoupling': [0]*5, 'score': 0}

    total_time = streams_list[-1]['timestamp']
    segment_duration = total_time / 5
    
    explosive_drills = [] # Basado en picos de velocidad
    efficiency_factors = [] # Basado en velocidad/pulso
    decoupling_trend = [] # Basado en la deriva cardiaca
    
    # 1. Calculamos los 5 bloques
    for i in range(5):
        start = i * segment_duration
        end = (i + 1) * segment_duration
        
        # Filtramos los puntos del segmento
        segment_points = [s for s in streams_list if start <= s['timestamp'] < end]
        
        if segment_points:
            avg_hr = sum(p['heartrate'] for p in segment_points) / len(segment_points)
            avg_speed = sum(p['pace']['raw'] for p in segment_points) / len(segment_points)
            max_speed = max(p['pace']['raw'] for p in segment_points)
            
            # A. Explosive Drills: Potencia pico en el segmento (Normalizado a 7 m/s como 100%)
            explosive_drills.append(round(min((max_speed / 7) * 100, 100)))
            
            # B. Efficiency Factor: Velocidad / Pulso (Normalizado: 0.03 m/s por latido = 100%)
            ef = avg_speed / avg_hr if avg_hr > 0 else 0
            efficiency_factors.append(round(min((ef / 0.03) * 100, 100)))
            
            # C. Aerobic Decoupling (Versión para barras 0-100)
            # Comparamos la eficiencia del segmento actual contra la eficiencia base (segmento 1)
            first_segment_ef = (sum(p['pace']['raw'] for p in [s for s in streams_list if s['timestamp'] < segment_duration]) / 
                            sum(p['heartrate'] for p in [s for s in streams_list if s['timestamp'] < segment_duration]))

            current_ef = avg_speed / avg_hr if avg_hr > 0 else 0

            # Si la eficiencia actual es igual a la del principio, la barra está al 100%
            # Si cae un 20%, la barra bajará.
            ratio = (current_ef / first_segment_ef) if first_segment_ef > 0 else 1
            decoupling_trend.append(round(max(0, min(100, ratio * 100))))


            
        else:
            

            explosive_drills.append(0); efficiency_factors.append(0); decoupling_trend.append(0)


    return {
        'explosive_drills': explosive_drills,
        'efficiency_factor': efficiency_factors,
        'aerobic_decoupling': decoupling_trend,
    }

def get_time_in_zone(streams_list, user_id):
    """Calcula el tiempo bajo tensión cardiovascular (TUT) acumulado por el atleta en cada una de sus 5 zonas de esfuerzo."""
    user = get_user_from_id(user_id)
    zones = user.heart_rate_zones
    time_in_zones = {1:0, 2:0, 3:0, 4:0, 5:0}

    for s in streams_list:
        hr = s['heartrate']
        z = 5
        for i in range(4):
            if hr <= zones[i]['max']:
                z = i + 1  
                break
        
        time_in_zones[z] +=1

    for key, value in time_in_zones.items():
        time_in_zones[key] = {
            'raw': value,
            'time': seconds_to_min(value)
        }
    return time_in_zones


def get_user_data(user_id):
    """Hidrata la instantánea estructurada del perfil completo del corredor mapeando la configuración biométrica."""
    user= get_user_from_id(user_id)

    return{
        'name': user.name,
        'surname' : user.surname,
        'nickname': user.nickname,
        'gender' : user.gender,
        'username' : user.username,
        'birthdate': {
            'formatted': format_date_human(user.birthdate),
            'raw' : user.birthdate,
            'short' : format_short_date(user.birthdate)
        },
        'email' : user.email,
        'weight' : user.weight,
        'max_hr' : user.max_hr,
        'rest_hr': user.rest_hr,
        'registration_date': {
            'raw' : user.registration_date,
            'formatted' : format_short_date(user.registration_date)
        },
        'last_update': {
            'raw': user.last_edit,
            'formatted' : format_short_date(user.last_edit)
        },
        'zones': user.heart_rate_zones,
        'profile_photo': user.profile_image or '',
        'obj_distance': user.obj_distance,
        'level': user.level
    }

def get_activity_data(activity):
    """Extrae exclusivamente los descriptores agregados macro de la entidad Activity."""
    return {
        'activity_id' : activity.activity_id,
        'user_id': activity.user_id,
        'type': activity.type,
        'distance': activity.distance,
        'moving_time': activity.mov_time,
        'average_heartrate': activity.avg_heartrate,
        'max_heartrate': activity.max_heartrate,
        'average_speed': activity.avg_pace,
        'max_speed': activity.max_pace,
        'total_elevation_gain': activity.positive_slope
    } 

def get_streams_data(streams):
    """Extrae las magnitudes físicas puntuales del modelo ActivityStream."""
    return {
        'activity_id': streams.activity_id,
        'altitude': streams.altitude,
        'current_speed': streams.current_speed,
        'heartrate': streams.heartrate,
        'grade': streams.grade,
        'distance': streams.distance
    }


def check_zones(zones):
    """Valida la consistencia relacional y continuidad continua matemática de los umbrales de las zonas de fatiga."""
    for i in range(len(zones) -1) :
        if zones[i]['max'] != zones[i+1]['min']: return False
    return True

def check_activity(user_id, activity_id):
    """Valida la propiedad jurídica del recurso para evitar brechas de seguridad entre usuarios."""
    activity = activity_user(user_id, activity_id)
    if activity: return activity
    return False 

def update_perceived_effort(user_id, activity_id, perceived_effort):
    """Persiste la magnitud subjetiva del esfuerzo de la sesión (Escala de Borg RPE)."""
    activity = activity_user(user_id,activity_id)
    activity.perceived_effort = perceived_effort
    sql_commit()

def slope(series):
    """
    Calcula la pendiente o gradiente de tendencia lineal utilizando mínimos cuadrados ponderados.
    Aísla de forma matemática e in-memory la tasa de progresión temporal del parámetro deportivo.
    """
    arr = np.array(series, dtype=float)
    if len(arr) < 2 or np.nanstd(arr) == 0:
        return 0.0
    mask = ~np.isnan(arr)
    if mask.sum() <2: 
        return 0.0
    return linregress(np.arange(len(arr))[mask], arr[mask]).slope

def aggregate_activity_data(activities, streams):
    """
    Unifica las estructuras jerárquicas en DataFrames de Pandas, calcula descriptores agregados de flujo
    y consolida una matriz analítica de series temporales combinadas para el motor de Inteligencia Artificial.
    """
    df_act = pd.DataFrame([a.__dict__ for a in activities]).drop('_sa_instance_state', axis=1, errors="ignore")
    df_str = pd.DataFrame([s.__dict__ for s in streams]).drop('_sa_instance_state', axis=1, errors="ignore")

    stream_agg = df_str.groupby('activity_id').agg(
        stream_hr_mean = ('heartrate', 'mean'),
        stream_hr_std = ('heartrate', 'std'),
        stream_speed_mean = ('current_speed', 'mean'),
        stream_grade_mean = ('grade', 'mean'),
        stream_grade_std = ('grade', 'std')
    ).reset_index()

    df = df_act.merge(stream_agg, on='activity_id', how='left').sort_values('date')
    df['speed_ms'] = 1000 / (df['avg_pace'] * 60)
    df['hr_effort_ratio'] = df['avg_heartrate'] / df['max_heartrate']

    return df

def build_feature_vector(df, feature_cols):
    """
    Construye la matriz de descriptores matemáticos finales calculando métricas de ventana (mean, std, min, max, trend).
    Reindexa de forma estricta las columnas resultantes frente al catálogo estructural del modelo RandomForest.
    """
    input_features = {}
    base_cols = ['distance', 'mov_time', 'avg_heartrate', 'max_heartrate', 
        'avg_pace', 'max_pace', 'positive_slope', 'elev_per_km', 
        'hr_effort_ratio', 'speed_ms', 'stream_hr_mean', 'stream_hr_std', 
        'stream_speed_mean', 'stream_grade_mean', 'stream_grade_std'
    ]

    for col in base_cols:
        if col in df.columns: 
            vals = df[col].values
            input_features[f'{col}_mean'] = np.nanmean(vals)
            input_features[f'{col}_std'] = np.nanstd(vals)
            input_features[f'{col}_min'] = np.nanmin(vals)
            input_features[f'{col}_max'] = np.nanmax(vals)
            input_features[f'{col}_trend'] = slope(vals)
    
    input_features['load_total_km'] = df['distance'].sum() / 1000
    input_features['load_total_time_h'] = df['mov_time'].sum() / 3600
    input_features['pace_consistency'] = 1- (df['avg_pace'].std() - df['avg_pace'].mean())

    X = pd.DataFrame([input_features])
    X = X.reindex(columns=feature_cols)
    return X