# ==============================================================================
# CONTROLADOR DE INGESTA MASIVA Y PROCESAMIENTO DE ARCHIVOS DEPORTIVOS (API)
# TFG: Análisis y predicción del rendimiento en corredores
# Autor: Jaume Antoni Soler Sánchez
# ==============================================================================

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import pandas as pd
import io

from utils.csv_parser import check_cols
from services.data_processing import save_activity, save_stream 
from services.metrics import *

upload_bp = Blueprint('upload_bp', __name__)
@upload_bp.route('/upload', methods = ['POST'])
@jwt_required()
def upload_files():
    """
    Endpoint de Ingesta de Telemetría. Recibe una colección multifichero (CSV/GPX),
    lee el contenido in-memory codificado en UTF-8, valida el esquema estructural
    y discrimina el almacenamiento entre actividades macro o flujos de series temporales.
    """
    uploaded_files = request.files.getlist('activities')
    user_id = get_jwt_identity()

    if not uploaded_files: return jsonify({'error': 'No se han enviado archivos'}), 400
    
    processed_count = 0
    errors = []

    for file in uploaded_files:
        if file.filename == '': continue 

        try:
            content = file.stream.read().decode('UTF8')
            df = pd.read_csv(io.StringIO(content))
            message = check_cols(df)
        
            if not message:
                errors.append(f"Archivo {file.filename}: Formato no válido")
                continue
            
            if message[0] == 'activity': processed_count += save_activity(user_id, message[1:])
            if message[0] == 'streams': processed_count += save_stream( message[1:], user_id)

        except Exception as e:
            errors.append(f"Archivo {file.filename}: {str(e)}")
            continue
    return jsonify({
        'message': f"Procesados {processed_count} elementos",
        'errors': errors
    }), 201 if processed_count > 0 else 400
        

        