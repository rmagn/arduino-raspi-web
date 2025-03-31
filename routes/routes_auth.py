from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_session import Session
from services.database_service import get_user_by_email
from services.auth_service import auth
import identity.web
from config import app_config as config

# 🔐 Création du blueprint
auth_bp = Blueprint("auth_bp", __name__)

# 🔑 Page de connexion Microsoft
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = get_user_by_email(email)

        if user:
            session["pre_auth_email"] = email
            session.modified = True
            return redirect(auth.log_in(
                scopes=config.SCOPE,
                redirect_uri=config.REDIRECT_URI,
                prompt="login"
            )["auth_uri"])
        else:
            return render_template(
                "auth/login.html",
                version=identity.__version__,
                error="Adresse email non autorisée."
            )

    # méthode GET : afficher le formulaire
    return render_template("auth/login.html", version=identity.__version__)



# 🎯 Redirection après authentification
@auth_bp.route(config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth/auth_error.html", result=result)

    pre_auth_email = session.pop("pre_auth_email", None)
    ms_user = auth.get_user()
    print("🧠 ms_user:", ms_user)  # debug temporaire

    ms_email = (
        ms_user.get("mail") or
        ms_user.get("userPrincipalName") or
        ms_user.get("preferred_username")
    )

    if not ms_email:
        return render_template("auth/auth_error.html", result={
            "error": "Impossible de récupérer une adresse email valide depuis Microsoft.",
            "details": ms_user
        })

    if not pre_auth_email or ms_email.lower() != pre_auth_email.lower():
        return render_template("auth/auth_error.html", result={
            "error": f"L'adresse email validée par Microsoft ({ms_email}) ne correspond pas à celle saisie ({pre_auth_email})."
        })

    return redirect(url_for("pages.home"))

# 🔓 Déconnexion
@auth_bp.route("/logout")
def logout():
    session.clear()  # <-- vide la session côté Flask
    return redirect(auth.log_out(config.REDIRECT_HOST + url_for("pages.home")))

# 👤 Info utilisateur (optionnel)
@auth_bp.route("/me")
def profile():
    user = auth.get_user()
    if not user:
        return redirect(url_for("auth_bp.login"))
    return render_template("profile.html", user=user)
