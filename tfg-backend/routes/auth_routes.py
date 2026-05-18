# ==============================================================================
# CONTROLADOR DE AUTENTICACIÓN, GESTIÓN DE ATLETAS Y BIOMETRÍA (API ENDPOINTS)
# TFG: Análisis y predicción del rendimiento en corredores
# Autor: Jaume Antoni Soler Sánchez
# ==============================================================================

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from sqlalchemy.orm.attributes import flag_modified
import os


from models.user import User
from services.metrics import check_zones, get_max_heartrate, get_age_from_date, get_user_data
from logic.db_utils import check_user, sql_add, sql_commit, get_user, get_user_from_id
# Configuración del entorno físico de persistencia para el sistema de ficheros de imágenes de perfil
UPLOAD_FOLDER = os.path.join('static', 'uploads', 'profiles')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


user_bp = Blueprint('user_bp', __name__)
@user_bp.route('/register', methods=['POST'])
def set_user():
    """
    Registra un nuevo corredor en el sistema, sanitiza las entradas de texto,
    calcula métricas biométricas basales por defecto y emite cookies JWT.
    """
    data = request.get_json()

    username = data.get('username','').strip().lower()
    if check_user('username',username): return jsonify({'errorUsername': True, 'error': 'Existe un error en el nombre de usuario'}), 400

    try:
        birthdate_format = '%Y-%m-%d'
        birthdate = datetime.strptime(data.get('birthDate'), birthdate_format).date()
    except (ValueError, TypeError):
        return jsonify({'errorDate': True, 'error': 'Existe un error en la fecha'}), 400
    
    email = data.get('email', '').strip().lower()
    if check_user('email', email): return jsonify({'errorEmail': True, 'error': 'Correo ya registrado'
    ''}), 400

    name = data.get('name', '').strip().lower()
    if not name: return jsonify({'errorName': True, 'error': 'Existe un error en el nombre'}), 400
    surname = data.get('surname', '').strip().lower()
    if not surname: return jsonify({'errorSurname': True, 'error': 'Existe un error en el apellido'}), 400
    nickname = data.get('nickname').strip().lower()
    if not nickname : return jsonify({'errorNickname': True, 'error': 'Existe un error en el nickname'}), 400    
    print(data.get('gender'))
    new_user = User(
        username = username,
        name = name,
        surname = surname,
        birthdate = birthdate,
        email = email,
        weight = float(data.get('weight') or 0),
        max_hr = data.get('max_hr') or get_max_heartrate(get_age_from_date(birthdate)),
        gender = data.get('gender'),
        nickname = nickname,
        level = data.get('level'),
        obj_distance = data.get('objRun')
    )
    new_user.set_password(data.get('password'))

    sql_add(new_user)
    sql_commit()

    access_token = create_access_token(identity=str(new_user.user_id))
    refresh_token = create_refresh_token(identity=str(new_user.user_id))
    response = jsonify({
        'msg': 'Usuario creado con éxito',
        'user': {
            'id': new_user.user_id,
            'username': new_user.username
        }
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

@user_bp.route('/login', methods=['POST'])
def login():
    """
    Autentica al usuario validando sus credenciales e inyecta las cookies de sesión
    con tiempos de expiración parametrizables según la opción de persistencia ('remember').
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    remember = data.get('remember', False)

    user = get_user(username)
    
    if not user: return jsonify({'error': 'Usuario no registrado'}), 404
    if not user.check_password(password): return jsonify({'error': 'Contraseña incorrecta'}), 401

    if remember: 
        access_expire = timedelta(days=30)
        refresh_expire = timedelta(days=30)
    else:
        access_expire = timedelta(days=1)
        refresh_expire = timedelta(days=1)
        

    access_token = create_access_token(identity=str(user.user_id), expires_delta=access_expire)
    refresh_token = create_refresh_token(identity=str(user.user_id), expires_delta=refresh_expire)

    response = jsonify({'msg': 'Login correcto',
                        'user': 
                            get_user_data(user.user_id)
                        })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200
    
@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Extrae de forma segura la instantánea completa del perfil del usuario autenticado."""
    user_id = get_jwt_identity()
    return jsonify({
        'user_snapshots': get_user_data(user_id)
    }), 200

@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Endpoint de refresco: Recibe un Refresh Token válido y emite una nueva cookie de acceso."""
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)

    response = jsonify({'msg': 'Token renovado'})
    set_access_cookies(response, new_access_token)
    return response, 200

@user_bp.route('/logout', methods=['POST'])
def logout():
    """Cierra la sesión destruyendo y limpiando de forma segura las cookies JWT del cliente."""
    response = jsonify({'msg': 'Sessión cerrada'})
    unset_jwt_cookies(response)
    return response, 200

@user_bp.route('/update-heart-rate-data', methods=['POST'])
@jwt_required()
def update_hr_data():
    """
    Modifica la configuración biométrica de entrenamiento del corredor, aplicando
    validación de consistencia relacional sobre los rangos de las zonas cardíacas de fatiga.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    rest_hr = data.get('rest_hr') or 60
    max_hr = data.get('max_hr')
    zones = data.get('custome_zones')

    if int(rest_hr) >= int(max_hr): return jsonify({'error': 'La frecuencia en reposo debe ser menor a la máxima'}), 400
    if not check_zones(zones): return jsonify({'error' : 'El valor minimo de la zona proxima y el maximo de la zona actual deben ser iguales.'})

    if int(zones[-1]['max']) != int(max_hr): zones[-1]['max'] = int(max_hr)
    user= get_user_from_id(user_id)
    user.max_hr = max_hr
    user.rest_hr = rest_hr
    user.custom_zones = zones
    user.last_edit = datetime.now()
    response =  jsonify({'message': 'Usuario actualizado correctamente',
                         'user': get_user_data(user_id)})

    sql_commit()
    return response, 200


@user_bp.route('/update', methods=['POST'])
@jwt_required()
def update():
    """
    Actualiza de forma integral los metadatos del corredor y gestiona físicamente 
    la carga, aislamiento dinámico de nombre y almacenamiento de la imagen de perfil.
    """
    user_id = get_jwt_identity()
    user = get_user_from_id(user_id)
    data = request.form
    r = ''

    if 'profile_photo' in request.files:
        file = request.files['profile_photo']
        if file.filename and allowed_file(file.filename):
            extension = file.filename.rsplit('.',1)[1].lower()

            filename = f"user_{user_id}.{extension}"

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            user.profile_image = f"static/uploads/profiles/{filename}"

    username = data.get('username', user.username)
    if(username != user.username): r = check_user('username',username)
    if(r): return jsonify({'error': 'Username ya esta siendo utilizado por otra persona', 'usernameError': True}), 400

    email = data.get('email', user.email)
    if(email != user.email): r = check_user('email', email)
    if(r): return jsonify({'error': 'El email ya esta siendo utilizado por otra persona', 'emailError': True}), 400

    weight = data.get('weight', user.weight)
    if(int(weight) <20 or int(weight) > 160): return jsonify({'error': 'Error en el peso', 'weightError': True}), 400

    max_hr = data.get('maxHr', user.max_hr)
    if(int(max_hr) < user.rest_hr or int(max_hr) > 215): return jsonify({'error': 'Error en la frecuencia cardiaca máxima', 'maxHrError': True}), 400

    birthdate = None
    try:
        birthdate = datetime.strptime(data.get('birthdate'), '%d/%m/%Y').date()
    except (ValueError, TypeError):
        try:
            birthdate = datetime.strptime(data.get('birthDate'), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return jsonify({'errorDate': True, 'error': 'Existe un error en la fecha'}), 400

    user.name = data.get('name', user.name)
    user.surname = data.get('surname', user.surname)
    user.username = username
    user.email = email
    user.weight = int(weight)
    user.max_hr = int(max_hr)
    user.birthdate = birthdate
    user.nickname = data.get('nickname', user.nickname)
    user.last_edit = datetime.now()
    user.obj_distance = data.get('objRun', user.obj_distance)
    user.level = data.get('level', user.level)

    if user.custom_zones:
        user.custom_zones[-1]['max'] = int(max_hr)
        flag_modified(user, 'custom_zones')

    sql_commit()

    return jsonify({
        'user_snapshots': get_user_data(user_id)
    }),200

@user_bp.route('/update-password', methods=['POST'])
@jwt_required()
def update_password():
    """Mutador seguro para la renovación de contraseñas con validaciones de identidad previas."""
    user_id = get_jwt_identity()
    data = request.get_json()
    user = get_user_from_id(user_id)
    password = data.get('password')
    if not user.check_password(password): return jsonify({'error': 'La contraseña no es correcta'}), 400

    new_password = data.get('newPassword')

    if password == new_password: return jsonify({'error': 'La contraseña debe ser diferente'}), 400
    user.set_password(new_password)
    sql_commit()

    return jsonify({
        'user_snapshots': get_user_data(user_id)
    })

@user_bp.route('/demo', methods=['POST'])
def login_demo():
    """Ruta de acceso Demo. Extrae credenciales seguras del entorno para permitir evaluaciones ágiles del tribunal."""
    demo_username = os.environ.get('DEMO_USER_USERNAME')
    demo_password = os.environ.get('DEMO_USER_PASSWORD')

    user = get_user(demo_username)
    
    if not user: return jsonify({'error': 'Usuario no registrado'}), 404
    if not user.check_password(demo_password): return jsonify({'error': 'Contraseña incorrecta'}), 401

    access_expire = timedelta(days=1)
    refresh_expire = timedelta(days=1)

    access_token = create_access_token(identity=str(user.user_id), expires_delta=access_expire)
    refresh_token = create_refresh_token(identity=str(user.user_id), expires_delta=refresh_expire)

    response = jsonify({'msg': 'Login correcto',
                        'user': 
                            get_user_data(user.user_id)
                        })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200