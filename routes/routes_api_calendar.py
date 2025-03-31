from flask import Blueprint, request, jsonify
from utils.decorators import login_required
from services.graph_service import get_calendar_shared_calendars, get_events_between
from utils.formater import get_week_bounds

api_calendar = Blueprint("api_calendar", __name__)

@api_calendar.route("/api/calendar_events")
@login_required
def calendar_events():
    periode = request.args.get("periode", "thisweek")

    offset_map = {
        "thisweek": 0,
        "nextweek": 1,
        "longterm": 2
    }

    offset = offset_map.get(periode.lower(), 0)
    calendars = get_calendar_shared_calendars()
    start, end = get_week_bounds(offset)
    events = get_events_between(calendars, start, end)

    return jsonify(events)
