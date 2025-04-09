# services/auth_microsoft.py

from flask import session, request, redirect, url_for
from config import app_config as config
from identity.web import Auth  # 🔄 On importe directement ici
from services.database_service import get_user_by_email
import requests
import base64

# 🧠 Création d’un objet Auth dédié à Microsoft
ms_auth = Auth(
    session=session,
    authority=config.AUTHORITY,
    client_id=config.CLIENT_ID,
    client_credential=config.CLIENT_SECRET,
)

def start_microsoft_login():
    session["provider"] = "microsoft"
    return redirect(ms_auth.log_in(
        scopes=config.SCOPE,
        redirect_uri=config.REDIRECT_URI,
        prompt="login"
    )["auth_uri"])

def handle_microsoft_callback():
    result = ms_auth.complete_log_in(request.args)
    if "error" in result:
        return None, result["error"]

    ms_user = ms_auth.get_user()
    email = (
        ms_user.get("mail") or
        ms_user.get("userPrincipalName") or
        ms_user.get("preferred_username")
    )
    pre_auth_email = session.pop("pre_auth_email", None)

    if not email or email.lower() != pre_auth_email:
        return None, f"L'email retourné par Microsoft ne correspond pas ({email} ≠ {pre_auth_email})"

    user = get_user_by_email(email)
    if not user:
        return None, "Utilisateur non autorisé."

    session["user"] = {
        "email": email.lower(),
        "name": ms_user.get("displayName"),
        "provider": "microsoft",
        "access_token": result.get("access_token")
    }
    return session["user"], None

def get_microsoft_user_photo():
    token = get_microsoft_token()
    if not token or "access_token" not in token:
        return None

    headers = { "Authorization": f"Bearer {token['access_token']}" }
    response = requests.get("https://graph.microsoft.com/v1.0/me/photo/$value", headers=headers)

    if response.status_code == 200:
        return "data:image/jpeg;base64," + base64.b64encode(response.content).decode("utf-8")
    return None

def get_microsoft_token():
    return ms_auth.get_token_for_user(config.SCOPE)