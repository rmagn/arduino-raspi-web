# /Features/HardwareManagement/alias_routes.py

from flask import Blueprint, render_template, request, jsonify
from utils.decorators import login_required, role_required
import Features.HardwareManagement.hardware_service as hardware_service
from models.arduino_model import Arduino
from models.sensor_model import Sensor

alias_bp = Blueprint("alias_bp", __name__, template_folder="Templates", static_folder="Static")

@alias_bp.route("/HardwareManagement")
@login_required
@role_required("administrateur")
def admin_aliases():
    """
    Affiche la page de gestion des alias.
    La page liste tous les alias avec leur Arduino associé.
    """
    aliases = hardware_service.get_all_sensors()
    # On peut également transmettre la liste des Arduino pour le formulaire
    arduinos = Arduino.query.order_by(Arduino.id).all()
    return render_template("aliases.html", aliases=aliases, arduinos=arduinos)


@alias_bp.route("/HardwareManagement/sensors/create", methods=["POST"])
@login_required
@role_required("administrateur")
def create_alias():
    data = request.form.to_dict()
    new_sensor = hardware_service.create_sensor(data)
    if new_sensor:
        # On renvoie quelques infos pour le rafraîchissement de la grille via AJAX
        return jsonify({
            "success": True,
            "message": "Nouvel alias créé avec succès !",
            "alias": {
                "id": new_sensor.id,
                "arduino_id": new_sensor.arduino_id,
                "arduino_nom": new_sensor.arduino.nom,
                "index_capteur": new_sensor.index_capteur,
                "type": new_sensor.type,
                "adresse_mac": new_sensor.adresse_mac,
                "alias": new_sensor.alias,
            }
        })
    else:
        return jsonify({"success": False, "message": "Erreur lors de la création"}), 500


@alias_bp.route("/HardwareManagement/sensors/edit", methods=["POST"])
@login_required
@role_required("administrateur")
def edit_alias():
    data = request.form.to_dict()
    sensor_id = data.get("id")
    if not sensor_id:
        return jsonify({"success": False, "message": "ID manquant"}), 400

    updated_alias = hardware_service.update_sensor(sensor_id, data)
    if updated_alias:
        return jsonify({
            "success": True,
            "message": "Capteur mis à jour avec succès",
            "alias": {
                "id": updated_alias.id,
                "arduino_id": updated_alias.arduino_id,
                "arduino_nom": updated_alias.arduino.nom,
                "index_capteur": updated_alias.index_capteur,
                "alias": updated_alias.alias,
                "type": updated_alias.type,
                "adresse_mac": updated_alias.adresse_mac,
            }
        })
    else:
        return jsonify({"success": False, "message": "Capteur non trouvé"}), 404


@alias_bp.route("/HardwareManagement/sensors/delete", methods=["POST"])
@login_required
@role_required("administrateur")
def delete_alias():
    sensor_id = request.form.get("id")
    if not sensor_id:
        return jsonify({"success": False, "message": "ID manquant"}), 400

    success = hardware_service.delete_sensor(sensor_id)
    if success:
        return jsonify({"success": True, "message": "Capteur supprimé avec succès"})
    else:
        return jsonify({"success": False, "message": "Capteur non trouvé"}), 404
    
@alias_bp.route("/HardwareManagement/arduinos/create", methods=["POST"])
@login_required
@role_required("administrateur")
def create_arduino():
    data = request.form.to_dict()
    new_arduino = hardware_service.create_arduino(data)
    if new_arduino:
        return jsonify({
            "success": True,
            "message": "Arduino créé avec succès !",
            "arduino": {
                "id": new_arduino.id,
                "nom": new_arduino.nom,
                "description": new_arduino.description  ,
                "type": new_arduino.type,
                "adresse_ip": new_arduino.adresse_ip,
            }
        })
    return jsonify({"success": False, "message": "Erreur lors de la création"}), 500


@alias_bp.route("/HardwareManagement/arduinos/edit", methods=["POST"])
@login_required
@role_required("administrateur")
def edit_arduino():
    data = request.form.to_dict()
    arduino_id = data.get("id")
    if not arduino_id:
        return jsonify({"success": False, "message": "ID manquant"}), 400

    updated = hardware_service.update_arduino(arduino_id, data)
    if updated:
        return jsonify({
            "success": True,
            "message": "Arduino mis à jour avec succès",
            "arduino": {
                "id": updated.id,
                "nom": updated.nom,
                "description": updated.description,
                "adresse_ip": updated.adresse_ip,
                "type": updated.type
            }
        })
    return jsonify({"success": False, "message": "Arduino non trouvé"}), 404


@alias_bp.route("/HardwareManagement/arduinos/delete", methods=["POST"])
@login_required
@role_required("administrateur")
def delete_arduino():
    arduino_id = request.form.get("id")
    if not arduino_id:
        return jsonify({"success": False, "message": "ID manquant"}), 400

    success = hardware_service.delete_arduino(arduino_id)
    if success:
        return jsonify({"success": True, "message": "Arduino supprimé avec succès"})
    else:
        return jsonify({"success": False, "message": "Arduino non trouvé"}), 404
