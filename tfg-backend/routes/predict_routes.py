# ==============================================================================
# CONTROLADOR DE INFERENCIA PREDICTIVA Y SIMULACIÓN CINÉTICA (API ENDPOINTS)
# TFG: Análisis y predicción del rendimiento en corredores
# Autor: Jaume Antoni Soler Sánchez
# ==============================================================================

from flask import Blueprint, jsonify, request
from logic.db_utils import check_predictions, get_prediction, get_recent_activities_with_streams, sql_add, sql_commit, get_model, sql_expire
from services.metrics import aggregate_activity_data, build_feature_vector, prediction_dto, model_dto
from flask_jwt_extended import get_jwt_identity, jwt_required
import pandas as pd
import joblib
from models.predictionLog import PredictionLog

predict_bp = Blueprint('predict_bp', __name__)

MODEL_PATH = './artifacts/running_model_v1_may.pkl'
try:
    model_package = joblib.load(MODEL_PATH)
except:
    model_package = None

@predict_bp.route('/prediction', methods=['POST'])
@jwt_required()
def prediction():
    """
    Endpoint principal de Inferencia Bajo Demanda. Recupera el histórico de telemetría del atleta,
    reconstruye su matriz analítica de características en caliente y genera proyecciones de marcas.
    """
    if not model_package: return jsonify({'error': 'Modelo no disponible'}), 500

    user_id = get_jwt_identity()
    data = request.get_json()
    print(data)
    limit = data.get('activityDepth') or 15
    print(limit)
    activities, streams = get_recent_activities_with_streams(user_id, limit)
    if len(activities) < 10: return jsonify({'error': 'Datos insuficientes'})


    df = aggregate_activity_data(activities, streams)
    X_input = build_feature_vector(df, model_package['feature_cols'])

    if X_input is None or (isinstance(X_input, pd.DataFrame) and X_input.empty):
        return jsonify({'error': 'No se pudieron generar para este usuario'}), 400
    
    X_values = X_input.values
    if X_values.ndim == 1:
        X_values = X_values.reshape(1,-1)
    
    try:
        X_imp = model_package['imputer'].transform(X_input)
        preds = model_package['model'].predict(X_imp)
    except Exception as e:
        return jsonify({'error': f'Error en el modelo: {str(e)}'}), 500
    res = {label: float(preds[0][i]) for i, label in enumerate(model_package['target_labels'])}
    
    try:
        last_act_id = int(df['activity_id'].iloc[-1])
        new_log = PredictionLog(
            user_id = user_id,
            last_activity_id = last_act_id,
            pred_5k = res['5k'],
            pred_10k = res['10k'],
            pred_21k = res['21k'],
            pred_42k = res['42k'],
            mae=None
        )
        sql_add(new_log)
        sql_commit()
        sql_expire()
        model = get_model()

    except Exception as e:
        return jsonify({'error' : f'No se pudo guardar el log: {e}'})
    return jsonify({
        'prediction': True,
        'PredictionSnapshots': prediction_dto(new_log),
        'ModelSnapshots': model_dto(model)
    })


@predict_bp.route('/check', methods=['GET'])
@jwt_required()
def check():
    """Verifica de forma ágil la existencia previa de logs predictivos para acelerar el renderizado en el cliente."""
    user_id = get_jwt_identity()
    if check_predictions(user_id): 
        pred = get_prediction(user_id)
        model = get_model()
        return jsonify({'prediction': True, 'PredictionSnapshots' : prediction_dto(pred), 'ModelSnapshots': model_dto(model)})
    else: return jsonify({'prediction' : False})

@predict_bp.route('/simulate', methods=['POST'])
@jwt_required()
def run_simulation():
    """
    ENDPOINT DEL SIMULADOR ANALÍTICO ("What-If Analysis").
    Modifica las variables latentes del vector de características aplicando coeficientes de estrés
    mecánico y restricciones meteorológicas ambientales (temperatura) para evaluar escenarios de carrera.
    """
    if not model_package: return jsonify({'error': 'Modelo no disponible'}), 500

    user_id = get_jwt_identity()
    data = request.get_json()

    activity_depth = int(data.get('activityDepth'))
    load_factor = float(data.get('loadFactor')) / 100.0
    temperature = int(data.get('temperature'))

    activities, streams = get_recent_activities_with_streams(user_id, limit=activity_depth)
    df = aggregate_activity_data(activities, streams)
    X_input = build_feature_vector(df, model_package['feature_cols'])

    if 'mean_pace' in X_input.columns:
        X_input['mean_pace'] = X_input['mean_pace'] * (1 + load_factor)
        if temperature > 20:
            weather_penalty = (temperature - 20) * 0.008
            X_input['mean_pace'] = X_input['mean_pace'] * (1 + weather_penalty)

    X_imp = model_package['imputer'].transform(X_input)
    preds = model_package['model'].predict(X_imp)

    res = {label: float(preds[0][i]) for i, label in enumerate(model_package['target_labels'])}
    
    return jsonify({
        'simulation': True,
        'ml_points': [
            {"distance": 5, "time": res['5k'], "confidence_range": [res['5k']*0.95, res['5k']*1.05]},
            {"distance": 10, "time": res['10k'], "confidence_range": [res['10k']*0.95, res['10k']*1.05]},
            {"distance": 21.1, "time": res['21k'], "confidence_range": [res['21k']*0.95, res['21k']*1.05]},
            {"distance": 42.2, "time": res['42k'], "confidence_range": [res['42k']*0.95, res['42k']*1.05]}
        ]
    })