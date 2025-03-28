from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_session import Session
from services.auth_service import auth
import identity.web
from config import app_config as config

# 🔐 Création du blueprint
auth_bp = Blueprint("auth_bp", __name__)

# 🔑 Page de connexion Microsoft
@auth_bp.route("/login")
def login():
    # print("🧭 URI redirection (config.REDIRECT_URI):", config.REDIRECT_URI)
    return render_template("auth/login.html", version=identity.__version__, **auth.log_in(
        scopes=config.SCOPE,
        redirect_uri=config.REDIRECT_URI  # <-- Utilise celui défini dans .env
    ))

# 🎯 Redirection après authentification
@auth_bp.route(config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        # print("❌ Erreur d'authentification :", result)
        return render_template("auth/auth_error.html", result=result)
    
    # print("✅ Authentification réussie ! Redirection vers la home.")
    return redirect(url_for("pages.home"))

# 🔓 Déconnexion
@auth_bp.route("/logout")
def logout():
    return redirect(auth.log_out(config.REDIRECT_HOST + url_for("pages.home")))

# 👤 Info utilisateur (optionnel)
@auth_bp.route("/me")
def profile():
    user = auth.get_user()
    if not user:
        return redirect(url_for("auth_bp.login"))
    return render_template("profile.html", user=user)
