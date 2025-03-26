from flask import Blueprint, render_template
from utils.decorators import login_required
from utils.formater import get_week_bounds
from services.graph_service import  get_events_between, get_calendar_shared_calendars

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
@login_required
def home():
    calendards = get_calendar_shared_calendars()
    
    current_start, current_end = get_week_bounds(0)
    thisWeek_events = get_events_between(calendards,current_start, current_end)
    
    next_start, next_end = get_week_bounds(1)
    nextWeek_events = get_events_between(calendards, next_start, next_end)

    longterm_start, longterm_end = get_week_bounds(2)
    longterm_events = get_events_between(calendards, longterm_start, longterm_end)
    
    return render_template("pages/index.html", thisWeek_events=thisWeek_events, nextWeek_events=nextWeek_events, longterm_events=longterm_events)


@pages_bp.route("/logs")
@login_required
def logs():
    return render_template("pages/supervision/logs.html")

@pages_bp.route("/SupervisonPlancher")
def SupervisonPlancher():
    return render_template("pages/supervision/Plancher.html")

@pages_bp.route("/SupervisionLocalChaudiere")
def SupervisionLocalChaudiere():
    return render_template("pages/supervision/LocalChaudiere.html")
