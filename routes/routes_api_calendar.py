from dateutil import parser
from flask import Blueprint, request, jsonify
from utils.decorators import login_required
from services.graph_service import get_calendar_shared_calendars, get_events_between, create_or_update_event, delete_event, get_events_for_period
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

@api_calendar.route("/api/calendar_events_range")
@login_required
def calendar_events_range():
    from dateutil import parser

    start_str = request.args.get("start")
    end_str = request.args.get("end")

    if not start_str or not end_str:
        return jsonify({"success": False, "message": "start/end manquants"}), 400

    try:
        # utilisation de parser pour gérer les +01:00, Z, etc.
        start = parser.parse(start_str)
        end = parser.parse(end_str)
    except Exception as e:
        print(f"❌ Erreur parsing date : {e}")
        return jsonify({"success": False, "message": "Format de date invalide"}), 400

    calendars = get_calendar_shared_calendars()
    events = get_events_between(calendars, start, end)
    return jsonify(events)



@api_calendar.route("/api/calendar_list")
@login_required
def calendar_list():
    from services.graph_service import get_calendar_list

    calendars = get_calendar_list()
    return jsonify(calendars)

@api_calendar.route("/api/calendar/update", methods=["POST"])
@login_required
def api_update_calendar():
    data = request.get_json()
    calendar_id = data.get("calendar_id")

    if not calendar_id:
        return jsonify({"success": False, "message": "Calendrier non spécifié"}), 400

    result = create_or_update_event(calendar_id, data)
    return jsonify(result)

@api_calendar.route("/api/calendar/delete", methods=["POST"])
@login_required
def delete_calendar_event():
    data = request.get_json()
    event_id = data.get("id")
    calendar_id = data.get("calendar_id")

    if not event_id or not calendar_id:
        return jsonify({"success": False, "message": "Données incomplètes"}), 400

    result = delete_event(calendar_id, event_id)
    return jsonify(result)
