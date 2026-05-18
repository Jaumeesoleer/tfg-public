import operator
from database import db
from models.activity import Activity
from models.user import User
from models.activityStream import ActivityStream
from models.predictionLog import PredictionLog
from models.modelAnalysis import ModelAnalysis
from sqlalchemy import exists, select, delete, insert, func
from datetime import datetime, timedelta

def pagination_user_activity(user_id, per_page, page, zones, filter_type = 'aerobic'):
    """
    Gestiona la paginación de actividades de un usuario aplicando filtros dinámicos
    basados en las zonas de intensidad de frecuencia cardíaca del atleta.
    """
    stmt = select(Activity).where(Activity.user_id == user_id)

    # Filtro temporal: Últimos 30 días
    if filter_type == '30_last_days':
        since = datetime.now() - timedelta(days=30)
        stmt = stmt.where(Activity.date >= since)
    # Filtro por Intensidad: Zona 2 (Regenerativo / Recuperación)
    elif filter_type == 'recovery':
        z2 = zones[1]
        stmt = stmt.where(Activity.avg_heartrate.between(z2['min'], z2['max']))
    # Filtro por Intensidad: Zonas 3 y 4 (Umbral Aeróbico y Tempo)
    elif filter_type == 'aerobic':
        z3_min = zones[2]['min']
        z4_max = zones[3]['max']
        stmt = stmt.where(Activity.avg_heartrate.between(z3_min, z4_max))
    # Filtro por Intensidad: Zona 5 (Capacidad Anaeróbica / Máxima Intensidad)
    elif filter_type == 'high_intensity':
        z5 = zones[4]
        stmt = stmt.where(Activity.avg_heartrate >= z5['min'])

    # Orden cronológico inverso y ejecución de la paginación ORM
    stmt = stmt.order_by(Activity.date.desc())
    pagination = db.paginate(stmt, page=page, per_page = per_page, error_out = False)
    return pagination

def get_last_activity_(user_id):
    """Recupera la última sesión de entrenamiento registrada por el usuario."""
    stmt = select(Activity).where(Activity.user_id == user_id).order_by(Activity.date.desc())
    last_activity = db.session.execute(stmt).scalar()
    return last_activity

def get_all_activities(user_id, limit=None):
    """Obtiene el histórico completo o limitado de actividades del atleta."""
    stmt = select(Activity).where(Activity.user_id == user_id).order_by(Activity.date.desc()).limit(limit)
    activities = db.session.execute(stmt).scalars().all()
    return activities

def activity_user(user_id, activity_id):
    """Valida y recupera una actividad específica asegurando la propiedad del dato (Multitenancy)."""
    stmt = select(Activity).where((Activity.user_id == user_id) & (Activity.activity_id == activity_id))
    activity = db.session.execute(stmt).scalar()
    return activity

def get_activity_db(external_id):
    stmt = select(Activity).where(Activity.external_id == external_id)
    last_activity = db.session.execute(stmt).scalar()
    return last_activity

def get_activity_streams(activity_id):

    stmt = select(ActivityStream).where(ActivityStream.activity_id == activity_id).order_by(ActivityStream.timestamp)
    streams = db.session.execute(stmt).scalars().all()
    return streams

def get_activities_streams(activity_ids):
    """
    Extrae la serie temporal granular (ActivityStream) asociada a una actividad,
    garantizando el orden secuencial de los puntos mediante el timestamp.
    """
    stmt = select(ActivityStream).where(ActivityStream.activity_id.in_(activity_ids))
    streams = db.session.execute(stmt).scalars().all()
    return streams

def get_recent_activities_with_streams(user_id, limit=15):
    """
    Optimiza la carga combinada de metadatos de actividades y sus correspondientes
    series temporales de datos granulares mediante un pipeline secuencial de consultas.
    """
    activities = get_all_activities(user_id, limit)
    if not activities: return [], []

    activity_ids = [a.activity_id for a in activities]
    streams = get_activities_streams(activity_ids)

    return activities, streams

def get_existing_ids(ids):
    stmt = select(Activity.external_id).where(Activity.external_id.in_(ids))
    existing_ids = db.session.execute(stmt).all()
    return set(existing_ids)

def get_existing_id(id, user_id):
    clean_id = int(id)
    clean_user_id = int(user_id)
    stmt = select(Activity.activity_id).where((Activity.external_id == clean_id) & (Activity.user_id == clean_user_id))
    existing_id = db.session.execute(stmt).scalar()
    return existing_id

def check_user(col, value):
    return db.session.query(exists().where(getattr(User, col) == value)).scalar()

def get_user(username):
    stmt = select(User).where(User.username == username)
    return db.session.execute(stmt).scalar_one_or_none()

def get_user_from_id(user_id):
    stmt = select(User).where(User.user_id == user_id)
    return db.session.execute(stmt).scalar_one_or_none()

def get_level(user_id):
    stmt = select(User.level).where(User.user_id == user_id)
    return db.session.execute(stmt).scalar_one_or_none()

def get_max_hr(user_id):
    stmt = select(User.max_hr).where(User.user_id == user_id)
    return db.session.execute(stmt).scalar_one_or_none()

def get_weight(user_id):
    stmt = select(User.weight).where(User.user_id == user_id)
    return db.session.execute(stmt).scalar_one_or_none()

def check_predictions(user_id):
    return db.session.query(exists().where(getattr(PredictionLog, 'user_id') == user_id)).scalar()

def user_stats(user_id):
    """
    Calcula métricas agregadas macro (duración, FC y distancia medias) 
    sobre una ventana deslizante de los últimos 90 días de entrenamiento.
    """
    start_date = datetime.now() - timedelta(days=90)
    stmt = (
        select(
            func.avg(Activity.mov_time).label('avg_duration'),  # <-- Cambiado aquí
            func.avg(Activity.avg_heartrate).label('avg_hr'),
            func.avg(Activity.distance).label('avg_distance')
        )
        .where(
            Activity.user_id == user_id,
            Activity.date >= start_date,
            Activity.date < datetime.now() 
        )
    )
    return db.session.execute(stmt).first()

def get_max_ef_index(user_id):
    """
    Calcula el Índice de Eficiencia Fisiológica Máxima (Pace/HR) en una ventana de 90 días.
    Determina la máxima velocidad alcanzada por unidad de esfuerzo cardiovascular.
    """
    start_date = datetime.now() - timedelta(days=90)
    stmt = (
        select(
            func.max(Activity.avg_pace / Activity.avg_heartrate).label('max_ef')
        )
        .where(
            Activity.user_id == user_id,
            Activity.avg_heartrate > 0,
            Activity.avg_pace > 0,
            Activity.date >= start_date,
            Activity.date < datetime.now()       
        )
    )
    return db.session.execute(stmt).scalar_one_or_none()
def get_prediction(user_id):
    stmt = select(PredictionLog).where(PredictionLog.user_id == user_id).order_by(PredictionLog.prediction_log_id.desc()).limit(1)
    return db.session.execute(stmt).scalar_one_or_none()

def get_threshold_seconds(user_id, hr_threshold = 160, init_date = datetime.now(), end_date = None):
    stmt = select(func.sum(Activity.mov_time)).filter(
        Activity.user_id == user_id,
        Activity.avg_heartrate >= hr_threshold,
        Activity.date >= init_date
    )
    if end_date:
        stmt = stmt.filter(Activity.date < end_date)
    
    return db.session.execute(stmt).scalar() or 0


def get_threshold_run(user_id, hr_threshold = 160):
    stmt = select(Activity).filter(Activity.user_id == user_id,
        Activity.avg_heartrate >= hr_threshold).order_by(Activity.date.desc())
    return db.session.execute(stmt).scalars().all()

def get_avg_hr(user_id):
    stmt = select(func.avg(Activity.avg_heartrate)).where(Activity.user_id == user_id)
    return db.session.execute(stmt).scalar_one_or_none()

def get_avg_efficiency(user_id):
    stmt = select(func.avg(Activity.workout_density)).where(Activity.user_id == user_id)
    return db.session.execute(stmt).scalar_one_or_none()

def get_model():
    stmt = select(ModelAnalysis).order_by(ModelAnalysis.generated_at.desc()).limit(1)
    return db.session.execute(stmt).scalar_one_or_none()

def sql_bulk_save(model, list):
    """
    Ejecuta una inserción masiva (Bulk Insert) en la base de datos
    para optimizar el rendimiento en la ingesta de series temporales largas.
    """
    if not list: return
    stmt = insert(model).values(list)
    db.session.execute(stmt)

def sql_add(model):
    
    db.session.add(model)

def sql_delete(model, col = False, value = False, op = False):
    if col == False or value == False:
        delete(model)
    else:
        operators = {
            '==' : operator.eq,
            '!=' : operator.ne,
            '>' : operator.gt,
            '>=' : operator.ge,
            '<' : operator.lt,
            '<=' : operator.le
        }
        column = getattr(model, col)
        condition = operators[op](column, value)
        
        stmt = delete(model).where(condition) 
        db.session.execute(stmt)
        sql_commit()

def sql_commit():
    """Abstrae el ciclo de transacciones ACID garantizando Rollback seguro ante fallos."""
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar: {e}")

def sql_expire():
    db.session.expire_all()