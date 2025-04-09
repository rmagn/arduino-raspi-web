# services/auth_manager.py

from flask import session
from services.auth_google import (
    start_google_login, handle_google_callback, get_google_user_photo
)
from services.auth_microsoft import (
    start_microsoft_login, handle_microsoft_callback, get_microsoft_user_photo
)

def get_provider():
    return session.get("user", {}).get("provider")

def get_user():
    return session.get("user")

def is_authenticated():
    return "user" in session

def start_login(provider, email):
    session["pre_auth_email"] = email
    if provider == "google":
        return start_google_login()
    elif provider == "microsoft":
        return start_microsoft_login()
    else:
        raise ValueError("Provider non supporté")

def handle_callback(provider):
    if provider == "google":
        return handle_google_callback()
    elif provider == "microsoft":
        return handle_microsoft_callback()
    else:
        raise ValueError("Provider non supporté")

def get_user_photo():
    provider = get_provider()
    if provider == "google":
        return get_google_user_photo()
    elif provider == "microsoft":
        return get_microsoft_user_photo()
    return None
