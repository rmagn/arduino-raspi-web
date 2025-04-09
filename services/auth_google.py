# services/auth_google.py

from flask import session, url_for
from services.database_service import get_user_by_email
from services.oauth_client import oauth


def start_google_login():
    session["provider"] = "google"
    redirect_uri = url_for("auth_bp.google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

def handle_google_callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.get("https://openidconnect.googleapis.com/v1/userinfo").json()

    email = user_info.get("email", "").lower()
    pre_auth_email = session.pop("pre_auth_email", None)

    if not email or email != pre_auth_email:
        return None, f"L'email retourné par Google ne correspond pas ({email} ≠ {pre_auth_email})"

    user = get_user_by_email(email)
    if not user:
        return None, "Utilisateur non autorisé."

    session["user"] = {
        "email": email,
        "name": user_info.get("name"),
        "provider": "google",
        "picture": user_info.get("picture"),
        "access_token": token["access_token"]
    }
    return session["user"], None

def get_google_user_photo():
    return session.get("user", {}).get("picture")
