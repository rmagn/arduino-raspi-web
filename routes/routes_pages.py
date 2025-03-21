from flask import Blueprint, render_template

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
def home():
    return render_template("index.html")

@pages_bp.route("/logs")
def logs():
    return render_template("logs.html")

@pages_bp.route("/SupervisonPlancher")
def SupervisonPlancher():
    return render_template("SupervisonPlancher.html")

@pages_bp.route("/SupervisionLocalChaudiere")
def SupervisionLocalChaudiere():
    return render_template("SupervisionLocalChaudiere.html")
