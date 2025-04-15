from models.database import db

class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)
    arduino_id = db.Column(db.Integer, db.ForeignKey("arduinos.id", name="fk_log_arduino_id"), nullable=False)

    Value0 = db.Column(db.Integer)
    Value1 = db.Column(db.Integer)
    Value2 = db.Column(db.Integer)
    Value3 = db.Column(db.Integer)
    Value4 = db.Column(db.Integer)
    Value5 = db.Column(db.Integer)
    Value6 = db.Column(db.Integer)
    Value7 = db.Column(db.Integer)
    Value8 = db.Column(db.Integer)
    Value9 = db.Column(db.Integer)

    arduino = db.relationship("Arduino", backref="logs")

