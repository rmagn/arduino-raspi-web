import requests
from flask import Blueprint, jsonify
from config.app_config import ARDUINO_IPS
import logging
logger = logging.getLogger(__name__)


arduino_bp = Blueprint('arduino', __name__)

@arduino_bp.route("/proxy_inputs/<arduino_name>")
def proxy_inputs(arduino_name):
    # logger.info(f"🔧 Appel proxy_inputs pour : {arduino_name}")
    ip = ARDUINO_IPS.get(arduino_name)
    if not ip:
        # logger.warning(f"❌ Arduino inconnu : {arduino_name}")
        return jsonify({"error": f"Arduino inconnu : {arduino_name}"}), 404

    try:
        url = f"http://{ip}:7777/ajax_inputs"
        # logger.debug(f"Requête envoyée vers {url}")
        response = requests.get(url, timeout=50)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        # logger.error(f"Erreur de connexion à l'Arduino '{arduino_name}' : {e}")
        return jsonify({"error": f"Erreur de connexion à l'Arduino '{arduino_name}' : {e}"}), 500
