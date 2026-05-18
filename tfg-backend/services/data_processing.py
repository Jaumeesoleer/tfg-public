from models.activity import Activity
from models.activityStream import ActivityStream
from logic.db_utils import *


def save_activity(user_id, message):
    """
    Procesa y persiste un lote de metadatos macro de actividades deportivas.
    Implementa optimización de consulta por conjunto para mitigar el problema N+1.
    """
    id_message = [m['id'] for m in message]
    existing_id = get_existing_ids(id_message)

    count = 0
    for m in message:
        if m['id'] in existing_id: continue
        act = Activity(
            external_id = m['id'],
            user_id = user_id,
            type = m['type'],
            title = m['title'],
            distance = m['distance'],
            mov_time = m['mov_time'],
            elp_time = m['elp_time'],
            workout_density = m['workout_density'],
            date = m['date'],
            avg_heartrate = m['avg_heartrate'],
            max_heartrate = m['max_heartrate'],
            avg_pace = m['avg_speed_ms'],
            max_pace = m['max_speed_ms'],
            positive_slope = m['positive_slope'],
            start_lat = m['start_lat'],
            start_lng = m['start_lng']
        )
        sql_add(act)
        count += 1

    sql_commit()
    return count

def save_stream(message, user_id):
    """
    Gestiona la ingesta de telemetría de alta densidad por segundo (ActivityStream).
    Garantiza idempotencia vaciando duplicados e implementa Bulk Insert optimizado.
    """
    if not message: return 0

    act_id_message = message[0]['activity_id']
    activity_id = get_existing_id(act_id_message, user_id)
    if not activity_id: return 0
    sql_delete(ActivityStream, 'activity_id', activity_id, '==')

    list = []
    for m in message:
        list.append({
            'activity_id': activity_id,
            'altitude': m.get('altitude', -1),
            'current_speed': m.get('velocity_smooth', -1),
            'timestamp': m.get('time', 0),
            'heartrate': m.get('heartrate', -1),
            'grade': m.get('grade', 0),
            'distance': m.get('distance', 0),
            'latitude': m.get('lat', -1),
            'longitude': m.get('lng', -1)
        })
    if not list: return 0

    sql_bulk_save(ActivityStream, list)
    sql_commit()
    return 1

    
