import requests
from flask import Blueprint, jsonify
from config.app_config import ARDUINO_IPS

arduino_bp = Blueprint('arduino', __name__)

@arduino_bp.route("/proxy_inputs/<arduino_name>")
def proxy_inputs(arduino_name):
    ip = ARDUINO_IPS.get(arduino_name)
    if not ip:
        return jsonify({"error": f"Arduino inconnu : {arduino_name}"}), 404

    try:
        url = f"http://{ip}:7777/ajax_inputs"
        response = requests.get(url, timeout=50)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Erreur de connexion à l'Arduino '{arduino_name}' : {e}"}), 500
