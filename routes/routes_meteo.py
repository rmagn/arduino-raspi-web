from flask import Blueprint, jsonify
from services.database_service import get_Ephemeris, get_all_previsions

meteo_bp = Blueprint("meteo", __name__)

@meteo_bp.route("/api/previsions/<localite_id>")
def meteo_previsions(localite_id):
    """Récupère les prévisions météo pour une localité donnée"""
    previsions = get_all_previsions(localite_id)
    if not previsions:
        return jsonify({"status": "error", "message": "Aucune prévision trouvée."}), 404
    
    return jsonify(previsions)

@meteo_bp.route("/api/meteo/ephemeris")
def meteo_ephemeris():
    getEphemeris = get_Ephemeris()
    return jsonify(getEphemeris)