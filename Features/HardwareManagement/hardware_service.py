# / Features/HardwareManagement/alias_service.py
from models.sensor_model import Sensor
from models.arduino_model import Arduino
from models import db

def get_all_sensors():
    """
    Récupère tous les alias, triés par Arduino puis par index_capteur.
    """
    return Sensor.query.join(Arduino).order_by(Arduino.nom, Sensor.index_capteur).all()

def get_sensor_by_id(sensor_id):
    return Sensor.query.get(sensor_id)

def create_sensor(data):
    try:
        new_sensor = Sensor(
            arduino_id=data.get("arduino_id"),
            index_capteur=data.get("index_capteur"),
            alias=data.get("alias"),
            type=data.get("type"),
            adresse_mac=data.get("adresse_mac")
        )
        db.session.add(new_sensor)
        db.session.commit()
        return new_sensor
    except Exception as e:
        print("Erreur création de capteur :", e)
        db.session.rollback()
        return None

def update_sensor(sensor_id, data):
    sensor_obj = Sensor.query.get(sensor_id)
    if not sensor_obj:
        return False

    sensor_obj.arduino_id = data.get("arduino_id", sensor_obj.arduino_id)
    sensor_obj.index_capteur = data.get("index_capteur", sensor_obj.index_capteur)
    sensor_obj.alias = data.get("alias", sensor_obj.alias)
    sensor_obj.type = data.get("type", sensor_obj.type)
    sensor_obj.adresse_mac = data.get("adresse_mac", sensor_obj.adresse_mac)

    try:
        db.session.commit()
        return sensor_obj
    except Exception as e:
        print("Erreur mise à jour du capteur :", e)
        db.session.rollback()
        return False
    

def delete_sensor(sensor_id):
    sensor_obj = Sensor.query.get(sensor_id)
    if sensor_obj:
        db.session.delete(sensor_obj)
        db.session.commit()
        return True
    return False


def create_arduino(data):
    try:
        new_arduino = Arduino(
            nom=data.get("nom"),
            type=data.get("type"),
            description=data.get("description"),
            adresse_ip=data.get("adresse_ip")
        )
        db.session.add(new_arduino)
        db.session.commit()
        return new_arduino
    except Exception as e:
        print("Erreur création Arduino :", e)
        db.session.rollback()
        return None



def update_arduino(arduino_id, data):
    arduino = Arduino.query.get(arduino_id)
    if not arduino:
        return None

    arduino.nom = data.get("nom", arduino.nom)
    arduino.description = data.get("description", arduino.description)
    arduino.adresse_ip = data.get("adresse_ip", arduino.adresse_ip)
    arduino.type = data.get("type", arduino.type)

    try:
        db.session.commit()
        return arduino
    except Exception as e:
        print("Erreur mise à jour Arduino :", e)
        db.session.rollback()
        return None


def delete_arduino(arduino_id):
    arduino = Arduino.query.get(arduino_id)
    if arduino:
        db.session.delete(arduino)
        db.session.commit()
        return True
    return False
