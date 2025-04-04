from flask import Blueprint, render_template
from utils.decorators import login_required, role_required
import services.users_service as users_service
from services.users_service import get_logged_user

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
@login_required
def home():
    return render_template("pages/index.html")

@pages_bp.route("/logs")
@login_required
def logs():
    return render_template("pages/supervision/logs.html")

@pages_bp.route("/SupervisonPlancher")
@login_required
def SupervisonPlancher():
    return render_template("pages/supervision/Plancher.html")

@pages_bp.route("/SupervisionLocalChaudiere")
@login_required
def SupervisionLocalChaudiere():
    return render_template("pages/supervision/LocalChaudiere.html")

@pages_bp.route("/calendar/manage")
@login_required
def manage_calendar():
    return render_template("pages/calendar/manage_calendar.html")

