from models.user_model import User
from models import db
from flask import session
from services.auth_service import auth

def get_all_users():
    return User.query.all()

def get_user_by_email(email):
    return User.query.get(email)

def create_user(data):
    try:
        user = User(
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            birthdate=data.get("birthdate"),
            role=data.get("role"),
        )
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as e:
        print("Erreur création utilisateur :", e)
        db.session.rollback()
        return False

def update_user(email, data):
    user = User.query.get(email)
    if not user:
        return False

    # Ne jamais mettre à jour l'email (clé primaire)
    fields_to_update = ['first_name', 'last_name', 'birthdate', 'role']
    for field in fields_to_update:
        if field in data:
            setattr(user, field, data[field])

    try:
        db.session.commit()
        return True
    except Exception as e:
        print("❌ Erreur lors de la mise à jour :", e)
        db.session.rollback()
        return False


def delete_user(email):
    user = User.query.get(email)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def get_logged_user():
    """Retourne l'objet User SQLAlchemy du user connecté, ou None si inconnu en base."""  
    ms_user = auth.get_user()

    email = (
        ms_user.get("mail") or
        ms_user.get("userPrincipalName") or
        ms_user.get("preferred_username")
    )

    print(f"👤 Email détecté : {email}")
    if email:
        return User.query.get(email)
    return None

