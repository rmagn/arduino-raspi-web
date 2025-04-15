from models.database import db

class Localite(db.Model):
    __tablename__ = "localites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String, nullable=False)
    code_postal = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('nom', 'code_postal', name='uq_nom_code_postal'),
    )
