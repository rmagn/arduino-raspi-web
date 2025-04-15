from models.database import db

class Sensor(db.Model):
    __tablename__ = "sensors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    arduino_id = db.Column(db.Integer, db.ForeignKey("arduinos.id", name="fk_sensor_arduino_id"), nullable=False)
    index_capteur = db.Column(db.Integer, nullable=False)
    alias = db.Column(db.String, nullable=False)
    type = db.Column(db.String)  # exemple: DHT22, thermocouple, etc.
    adresse_mac = db.Column(db.String(48))  # format standard XX:XX:XX:XX:XX:XX

    arduino = db.relationship("Arduino", back_populates="sensors")

    def __repr__(self):
        return f"<Sensor alias='{self.alias}' (Index {self.index_capteur})>"

