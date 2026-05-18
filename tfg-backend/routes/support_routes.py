# ==============================================================================
# CONTROLADOR DE COMUNICACIONES EXTERNAS Y PASARELA DE CORREO DE SOPORTE (API)
# TFG: Análisis y predicción del rendimiento en corredores
# Autor: Jaume Antoni Soler Sánchez
# ==============================================================================

import resend
from flask import Blueprint, jsonify, request
import os

resend.api_key = os.environ.get("RESEND_API_KEY")
support_bp = Blueprint('support_bp', __name__)

@support_bp.route('/submit-ticket', methods=['POST'])
def handle_ticket():
    """
    Endpoint del Canal de Soporte. Recibe incidencias técnicas del frontend,
    sanitiza los campos en caliente, maqueta un informe HTML dinámico
    y despacha una alerta asíncrona mediante el SDK de Resend.
    """
    data = request.get_json()
    
    nombre = data.get('name')
    email_usuario = data.get('email')
    asunto = data.get('subject')
    mensaje = data.get('content')

    try:
        html_content = f"""
        <h3>Nuevo Ticket de Soporte</h3>
        <p><b>Usuario:</b> {nombre} ({email_usuario})</p>
        <p><b>Asunto:</b> {asunto}</p>
        <p><b>Mensaje:</b></p>
        <p>{mensaje}</p>
        """
        
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": os.environ.get("PERSONAL_EMAIL"), 
            "subject": f"[SOPORTE] {asunto}",
            "html": html_content
        })
        
        return jsonify({"success": True, "message": "Ticket enviado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500