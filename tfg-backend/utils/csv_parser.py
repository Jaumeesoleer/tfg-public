# ==============================================================================
# PARSER DE INGESTA, SANITIZACIÓN Y VALIDACIÓN DE ESQUEMAS DE TELEMETRÍA (UTILS)
# TFG: Análisis y predicción del rendimiento en corredores
# Autor: Jaume Antoni Soler Sánchez
# ==============================================================================

import pandas as pd
from datetime import datetime

def parse_cords(val):
    """
    Abstrae el parseo y la normalización de coordenadas geoespaciales (Lat, Lng).
    Soporta estructuras nativas serializadas tanto en formato de listas como en strings con delimitadores.
    """
    if isinstance(val, list) and len(val) == 2:
        return float(val[0]), float(val[1])
    if isinstance(val, str) and ',' in val:
        coords = val.strip('[]').split(',')
        return float(coords[0]), float(coords[1])
    return -1.0, -1.0

def activity_cols(df, msg):
    """
    Filtra, sanitiza y ejecuta ingeniería de variables básicas sobre archivos macro de actividad.
    Mapea el esquema crudo del sensor hacia el modelo relacional unificado de la plataforma.
    """
    df_filetered = df[
        df['type'].isin(['Run', 'Walk', 'VirtualRun']) &
        (df['distance'] > 0) &
        (pd.to_datetime(df['start_date']).dt.tz_localize(None) <= datetime.now())
    ].copy()

    df_filetered['workout_density'] = df_filetered['moving_time'] / df_filetered['elapsed_time']
    df_filetered['avg_heartrate'] = df_filetered['average_heartrate'].fillna(-1)
    df_filetered['max_heartrate'] = df_filetered['max_heartrate'].fillna(-1)

    coords = df_filetered['start_latlng'].apply(parse_cords)
    df_filetered[['start_lat', 'start_lng']] = pd.DataFrame(coords.tolist(), index=df_filetered.index)


    col_names = {
        'id': 'id', 'type': 'type', 'name': 'title', 'start_date': 'date', 'distance': 'distance', 'moving_time': 'mov_time', 'elapsed_time': 'elp_time', 'average_speed': 'avg_speed_ms', 'max_speed': 'max_speed_ms', 'total_elevation_gain': 'positive_slope'
    }

    final_col = list(col_names.values()) + ['workout_density', 'avg_heartrate', 'max_heartrate', 'start_lat', 'start_lng']

    df_final = df_filetered.rename(columns=col_names) 
    msg.extend(df_final[final_col].to_dict(orient="records"))


def streams_cols(df, msg):
    """Sanitiza las series temporales de alta densidad imputando nulos antes de su conversión a diccionario."""
    clean_df = df.fillna(-1)
    msg.extend(clean_df.to_dict(orient='records'))

def check_cols(df):
    """
    Punto de entrada del validador. Evalúa mediante álgebra de conjuntos si el archivo
    coincide con el esquema macro ('activity') o micro ('streams'), orquestando su procesamiento.
    """
    required = {
        'activity': {
            'id', 'type', 'name', 'distance', 'moving_time', 'elapsed_time',  'start_date', 'max_heartrate', 'elev_high', 'average_speed'
        },
        'streams': {
            'velocity_smooth', 'time', 'heartrate',  'distance', 'activity_id'
        }
        
    }

    current_cols = set(df.columns)
    msg = [name for name, cols in required.items() if cols.issubset(current_cols)]
    if not msg: return []
    if msg[0] == 'activity': activity_cols(df, msg)
    elif msg[0] == 'streams': streams_cols(df, msg)

    return msg