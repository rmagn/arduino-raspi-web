from functools import wraps
from flask import redirect, url_for
from services.auth_service import auth  # on récupère l'objet auth déjà configuré
from services.users_service import get_logged_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not auth.get_user():
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_logged_user()
            if not user or user.role != required_role:
                return redirect(url_for("pages.logs"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
