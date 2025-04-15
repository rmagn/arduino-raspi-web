from models.database import db

class MeteoPrevision(db.Model):
    __tablename__ = "meteo_previsions"

    localite_id = db.Column(db.Integer, db.ForeignKey("localites.id", name="fk_meteo_previsions_localite_id"), primary_key=True)
    date_heure_utc = db.Column(db.String, primary_key=True)

    wind_speed = db.Column(db.Float)
    wind_dir = db.Column(db.Float)
    wind_gusts_1h = db.Column(db.Float)
    wind_gusts_24h = db.Column(db.Float)
    temp = db.Column(db.Float)
    temp_max = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    pression = db.Column(db.Float)
    pluie_1h = db.Column(db.Float)
    pluie_24h = db.Column(db.Float)
    symbole_1h = db.Column(db.Integer)
    symbole_24h = db.Column(db.Integer)
    uv = db.Column(db.Float)
    lever_soleil = db.Column(db.String)
    coucher_soleil = db.Column(db.String)

    localite = db.relationship("Localite", backref="previsions")
    def __repr__(self):
        return f"<MeteoPrevision {self.localite_id} {self.date_heure_utc}>"
