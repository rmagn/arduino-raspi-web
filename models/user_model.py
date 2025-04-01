from models import db

class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birthdate = db.Column(db.String)
    role = db.Column(db.String)
