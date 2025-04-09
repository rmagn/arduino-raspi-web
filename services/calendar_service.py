from services.auth_manager import get_provider

from services.graph_service import (
    get_calendar_shared_calendars as ms_get_calendars,
    get_events_between as ms_get_events_between,
    get_calendar_list as ms_get_calendar_list,
    create_or_update_event as ms_create_or_update_event,
    delete_event as ms_delete_event
)

from services.google_calendar_service import (
    get_calendar_shared_calendars as g_get_calendars,
    get_events_between as g_get_events_between,
    get_calendar_list as g_get_calendar_list,
    create_or_update_event as g_create_or_update_event,
    delete_event as g_delete_event
)


def get_provider_name():
    return get_provider() or "microsoft"


def normalize_event(event, provider):
    if provider == "google":
        return {
            "id": event.get("id"),
            "subject": event.get("summary", "Sans titre"),
            "start": {"dateTime": event.get("start", {}).get("dateTime")},
            "end": {"dateTime": event.get("end", {}).get("dateTime")},
            "organizer": {"emailAddress": {"name": event.get("organizer", {}).get("displayName", "?")}},
            "location": {"displayName": event.get("location", "Lieu non précisé")},
            "categories": [],  # ou extraire via `event.get("colorId")` si nécessaire
            "calendarId": event.get("calendarId")
        }
    else:  # Microsoft
        return event



def get_calendar_shared_calendars():
    if get_provider() == "google":
        print("📅 Google provider")
        return g_get_calendars()
    print("📅 Microsoft provider")
    return ms_get_calendars()


def get_events_between(calendars, start, end):
    provider = get_provider()
    raw_events = []

    if provider == "google":
        raw_events = g_get_events_between(calendars, start, end)
    else:
        raw_events = ms_get_events_between(calendars, start, end)

    return [normalize_event(e, provider) for e in raw_events]



def get_events_for_period(start_datetime, end_datetime):
    calendars = get_calendar_shared_calendars()
    return get_events_between(calendars, start_datetime, end_datetime)


def get_calendar_list():
    if get_provider() == "google":
        return g_get_calendar_list()
    return ms_get_calendar_list()


def create_or_update_event(calendar_id, data):
    if get_provider() == "google":
        return g_create_or_update_event(calendar_id, data)
    return ms_create_or_update_event(calendar_id, data)


def delete_event(calendar_id, event_id):
    if get_provider() == "google":
        return g_delete_event(calendar_id, event_id)
    return ms_delete_event(calendar_id, event_id)
