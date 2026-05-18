# ==============================================================================
# CONTROLADOR DE RUTAS DE ACTIVIDADES DEPORTIVAS (API ENDPOINTS)
# TFG: Análisis y predicción del rendimiento en corredores
# Autor: Jaume Antoni Soler Sánchez
# ==============================================================================

from flask import Blueprint, jsonify, request
from services.metrics import activity_dto, activity_stream_dto, check_activity, get_segments_data, get_time_in_zone, update_perceived_effort
from logic.db_utils import get_activity_streams, get_avg_efficiency, get_avg_hr, get_threshold_run, get_threshold_seconds, get_user_from_id, pagination_user_activity, get_last_activity_
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import numpy as np



activity_bp = Blueprint('activity_bp', __name__)
@activity_bp.route('/activities', methods=['POST'])
@jwt_required()
def get_activities():
    """
    Ruta principal del Dashboard. Devuelve el histórico paginado de actividades del usuario
    autenticado junto con un bloque analítico de auditoría macro del estado de forma.
    """
    user_id = get_jwt_identity()
    data = request.get_json().get('params')
    per_page = data.get('per_page')
    page = data.get('page')
    filter_type = data.get('filter')

    user = get_user_from_id(user_id)

    if not user_id: return jsonify({'error': 'Falta user_id'}), 400

    pagination = pagination_user_activity(user_id, per_page, page, user.heart_rate_zones, filter_type)
    activities_list = [activity_dto(a, user_id) for a in pagination.items]
    
    # Obtención del tiempo total acumulado (en segundos) por encima del umbral de Zona 3 (aeróbico/tempo)
    last_30_days = datetime.now() - timedelta(days=30)
    last_60_days = datetime.now() - timedelta(days=60)
    load = get_threshold_seconds(user_id, user.heart_rate_zones[3]['min'], last_30_days)
    prev_load = get_threshold_seconds(user_id, user.heart_rate_zones[3]['min'], last_60_days, last_30_days)
    inc_load = 0
    if prev_load > 0:
        inc_load = round(((load / prev_load) - 1) * 100, 1)

    last_thresholds_runs = get_threshold_run(user_id, user.heart_rate_zones[3]['min'])
    mean_vel = [run.avg_pace for run in last_thresholds_runs if run.avg_pace is not None]
    run_name = last_thresholds_runs[0].title or "Threshold Run"
    calc_var = 0.0
    abs_var = np.var(mean_vel)
    global_mean = np.mean(mean_vel)
    calc_var = round((abs_var / global_mean) * 100, 1)
    return jsonify({
        'activities': activities_list,
        'pagination' : {
            'total_pages': pagination.pages,
            'current_page': pagination.page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
            'total_items': pagination.total,
            'total_page_items': len(activities_list)
        },
        'audit': {
            'inc_intensity': inc_load,
            'last_thre_name': run_name,
            'calc_var': calc_var,
            'avg_hr': get_avg_hr(user_id),
            'avg_efficiency': get_avg_efficiency(user_id)
        }
    }), 200

@activity_bp.route('/last-activity', methods=['POST'])
@jwt_required()
def get_last_activity():
    """
    Devuelve los datos granulares de la última actividad registrada por el usuario,
    extrayendo las series temporales por segundo y computando la distribución por zonas.
    """
    user_id = get_jwt_identity()
    if not user_id: return jsonify({'error' : 'error'}), 400

    user = get_user_from_id(user_id)
    last_activity = get_last_activity_(user_id)
    st = get_activity_streams(last_activity.activity_id)
    streams_list = [activity_stream_dto(s) for s in st]
    streams_card = get_segments_data(streams_list)
    zone_time = get_time_in_zone(streams_list, user_id)

    return jsonify({
        'activity': activity_dto(last_activity, user_id, zone_time),
        'streams' : streams_list,
        'streams_card' : streams_card,
        'user_snapshots': {
            'name': user.name,
            'surname': user.surname,
            'nickname': user.nickname,
            'user_img': user.profile_image or '',
            'weight' : user.weight,
            'max_hr' : user.max_hr,
            'rest_hr' : user.rest_hr,
            'zones' : user.heart_rate_zones
        }
    })

@activity_bp.route('/activity', methods=['GET'])
@jwt_required()
def get_activity():
    """Recupera los datos detallados de una sesión deportiva específica mediante su identificador único."""
    user_id = get_jwt_identity()
    activity_id = request.args.get('activity_id')
    user = get_user_from_id(user_id)
    activity = check_activity(user_id, activity_id)
    streams = get_activity_streams(activity_id)
    str_list = [activity_stream_dto(s) for s in streams]
    zone_time = get_time_in_zone(str_list, user_id)
    if not activity: return jsonify({'error': '/dashboard'})

    return jsonify({
        'activity': activity_dto(activity, user_id, zone_time), 
        'streams': str_list,
        'user_snapshots':{
            'zones': user.heart_rate_zones
        }
    })
    

@activity_bp.route('/update-effort', methods=['POST'])
@jwt_required()
def update_effort():
    """
    Actualiza la métrica subjetiva de esfuerzo (RPE - Rate of Perceived Exertion)
    del corredor para una sesión específica, aplicando validación de rango estricto.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    activity_id = data.get('activityId')
    perceived_effort = data.get('effort')

    if perceived_effort is None or not (0 <= int(perceived_effort) <= 10): return jsonify({'error': ''})

    update_perceived_effort(user_id, activity_id, perceived_effort)
    
    return jsonify({
        'message': 1
    })