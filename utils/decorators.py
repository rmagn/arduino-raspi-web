from functools import wraps
from flask import redirect, url_for
from services.auth_service import auth  # on récupère l'objet auth déjà configuré

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not auth.get_user():
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    return decorated_function
