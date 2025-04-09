# services/google_calendar_service.py

import requests
from flask import session
from utils.formater import ensure_seconds

def get_google_token():
    user = session.get("user", {})
    token = user.get("access_token")
    if not token:
        print("❌ Token Google non trouvé dans la session")
    return token

def get_calendar_shared_calendars():
    token = get_google_token()
    if not token:
        return []

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = "https://www.googleapis.com/calendar/v3/users/me/calendarList"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        calendars = response.json().get("items", [])

        valid_ids = []

        for cal in calendars:
            cal_id = cal.get("id", "")
            summary = cal.get("summary", "")
            print(f"📅 {summary} → {cal_id}")

            # Exclusions typiques (non consultables ou provoquent des 404)
            if cal_id.endswith("holiday@group.v.calendar.google.com"):
                continue
            if cal_id.startswith("e_"):
                continue
            if cal_id.endswith("weeknum@group.v.calendar.google.com"):
                continue

            # Ajoute seulement les valides
            valid_ids.append(cal_id)

        return valid_ids
    else:
        print(f"❌ Erreur Google lors de la récupération des calendriers : {response.status_code}")
        return []

def get_events_between(calendars, startDateTime, endDateTime):
    print(f"🔄 Récupération des événements Google entre {startDateTime} et {endDateTime}")
    token = get_google_token()
    if not token:
        return []

    headers = {
        "Authorization": f"Bearer {token}"
    }

    events = []

    for calendar_id in calendars:
        url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
        params = {
            "timeMin": startDateTime.isoformat() + "Z",
            "timeMax": endDateTime.isoformat() + "Z",
            "singleEvents": True,
            "orderBy": "startTime"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            items = response.json().get("items", [])
            for item in items:
                item["calendarId"] = calendar_id
            events.extend(items)
        else:
            print(f"❌ Erreur Google lors de la récupération des événements : {response.status_code} - {response.text}")

    return events

def create_or_update_event(calendar_id, data):
    token = get_google_token()
    if not token:
        return {"success": False, "message": "Token manquant"}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    event_payload = {
    "summary": data.get("subject", "").strip(),
    "start": {
        "dateTime": ensure_seconds(data.get("start")),
        "timeZone": "Europe/Paris"
    },
    "end": {
        "dateTime": ensure_seconds(data.get("end")),
        "timeZone": "Europe/Paris"
    },
    "location": data.get("location", "")
}


    if data.get("id"):
        # Édition
        url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{data['id']}"
        response = requests.put(url, headers=headers, json=event_payload)
        if response.status_code in [200, 201]:
            return {"success": True, "message": "Événement mis à jour"}
    else:
        # Création
        url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
        print("📤 Payload envoyé à Google :", event_payload)

        response = requests.post(url, headers=headers, json=event_payload)
        if response.status_code == 200:
            created_event = response.json()
            return {
                "success": True,
                "message": "Événement créé",
                "id": created_event.get("id")
            }

    print(f"❌ Erreur Google Calendar : {response.status_code} - {response.text}")
    return {"success": False, "message": "Erreur lors de la création ou mise à jour"}

def delete_event(calendar_id, event_id):
    token = get_google_token()
    if not token:
        return {"success": False, "message": "Token manquant"}

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}"
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {"success": True, "message": "Événement supprimé"}
    else:
        print(f"❌ Erreur suppression Google Calendar : {response.status_code} - {response.text}")
        return {"success": False, "message": "Erreur lors de la suppression"}

def get_calendar_list():
    """
    Retourne une liste de calendriers avec leur id et nom (filtrés, comme pour Microsoft).
    """
    print("🔄 Récupération des calendriers Google pour la liste déroulante...")
    token = get_google_token()
    if not token:
        return []

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = "https://www.googleapis.com/calendar/v3/users/me/calendarList"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        calendars = response.json().get("items", [])
        filtered = []

        for cal in calendars:
            cal_id = cal.get("id", "")
            summary = cal.get("summary", cal_id)

            # Exclusions typiques
            if cal_id.endswith("holiday@group.v.calendar.google.com"):
                continue
            if cal_id.endswith("weeknum@group.v.calendar.google.com"):
                continue
            if cal_id.startswith("e_"):
                continue

            filtered.append({
                "id": cal_id,
                "name": summary
            })
       
       
        print("📅 Liste des calendriers filtrés :", filtered)
        return filtered
    else:
        print(f"❌ Erreur récupération Google calendars : {response.status_code}")
        return []
