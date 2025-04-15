from models.database import db


class Arduino(db.Model):
    __tablename__ = "arduinos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)  # Arduino, Raspberry Pi, etc.
    description = db.Column(db.String)
    adresse_ip = db.Column(db.String(45))  # pour IPv4 / IPv6

    sensors = db.relationship("Sensor", back_populates="arduino", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Arduino {self.nom} ({self.adresse_ip})>"

