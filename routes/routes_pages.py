from flask import Blueprint, render_template
from utils.decorators import login_required
from utils.formater import get_week_bounds
from services.graph_service import  get_events_between, get_calendar_shared_calendars

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
