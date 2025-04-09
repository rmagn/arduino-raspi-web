# routes/routes_auth.py

from flask import Blueprint, render_template, request, redirect, url_for, session
from services import auth_manager

auth_bp = Blueprint("auth_bp", __name__)

# 🔑 Page de connexion
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        provider = request.form.get("provider")
        return auth_manager.start_login(provider, email)

    return render_template("auth/login.html")

# 🎯 Callback après authent Google
@auth_bp.route("/auth/google/callback")
def google_callback():
    user, error = auth_manager.handle_callback("google")
    if error:
        return render_template("auth/auth_error.html", result={"error": error})
    return redirect(url_for("pages.home"))

# 🎯 Callback après authent Microsoft
@auth_bp.route("/callback")
def microsoft_callback():
    user, error = auth_manager.handle_callback("microsoft")
    if error:
        return render_template("auth/auth_error.html", result={"error": error})
    return redirect(url_for("pages.home"))

# 🔓 Déconnexion
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_bp.login"))
