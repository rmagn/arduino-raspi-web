import requests
import base64
from datetime import datetime 
from config import app_config as config
from services.auth_service import auth



def get_calendar_shared_calendars():
    """
    Récupère la liste des IDs des calendriers accessibles.
    """
    token = auth.get_token_for_user(config.SCOPE)
    if not token or "access_token" not in token:
        print("❌ Token manquant pour chercher les calendriers")       

    headers = {
        "Authorization": f"Bearer {token['access_token']}"
    }

    response = requests.get("https://graph.microsoft.com/v1.0/me/calendars", headers=headers)

    if response.status_code == 200:
        calendars = response.json().get("value", [])
        return [calendar["id"] for calendar in calendars]
    else:
        print(f"❌ Erreur lors de la récupération des calendriers : {response.status_code}")
        return []

def get_events_between(calendars, startDateTime, endDateTime): 
    # print("📅 Récupération des événements de la semaine")

    token = auth.get_token_for_user(config.SCOPE)
    if not token or "access_token" not in token:
        print("❌ Token manquant pour récupérer les événements")
        return []

    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "Prefer": 'outlook.timezone="Europe/Paris"'
    }
    
    params = {
        "startDateTime": startDateTime.isoformat()+"Z",
        "endDateTime": endDateTime.isoformat()+"Z",
        "$select": "subject,organizer,start,end,categories",                 
        "$top": 50,        
    } 

    events = []

    for calendar in calendars:
        url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar}/calendarView"
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=5
        )

        if response.status_code == 200:
            events_batch = response.json().get("value", [])

            # Ajouter le calendarId à chaque événement
            for event in events_batch:
                event["calendarId"] = calendar

            events.extend(events_batch)
        else:
            print(f"❌ Erreur lors de la récupération des événements : {response.status_code} - {response.text}")
            return []
    
    # Trier les événements par ordre chronologique en utilisant le champ 'start'
    events = sorted(events, key=lambda event: event['start']['dateTime'])

    return events
    
def get_user_photo():
    """
    Récupère la photo de profil de l'utilisateur connecté via Microsoft Graph.
    Retourne une URL base64 à utiliser dans <img src="...">.
    """
    try:
        token = auth.get_token_for_user(config.SCOPE)
        if not token or "access_token" not in token:
            print("❌ Token non trouvé.")
            return None

        access_token = token['access_token']
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(
            "https://graph.microsoft.com/v1.0/me/photo/$value",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            return "data:image/jpeg;base64," + base64.b64encode(response.content).decode("utf-8")
        else:
            print(f"❌ Erreur HTTP : {response.status_code}")
            return None

    except Exception as e:
        print("❌ Exception :", str(e))
        return None

def get_calendar_list():
    """
    Retourne une liste de calendriers avec leur id et nom pour affichage dans un select.
    """
    token = auth.get_token_for_user(config.SCOPE)
    if not token or "access_token" not in token:
        print("❌ Token manquant pour chercher les calendriers")       
        return []

    headers = {
        "Authorization": f"Bearer {token['access_token']}"
    }

    response = requests.get("https://graph.microsoft.com/v1.0/me/calendars", headers=headers)

    if response.status_code == 200:
        calendars = response.json().get("value", [])
        return [
            {"id": calendar["id"], "name": calendar["name"]}
            for calendar in calendars
        ]
    else:
        print(f"❌ Erreur récupération calendriers : {response.status_code}")
        return []


def create_or_update_event(calendar_id, data):
    """
    Crée ou met à jour un événement dans le calendrier spécifié.
    """
    token = auth.get_token_for_user(config.SCOPE)
    if not token or "access_token" not in token:
        print("❌ Token manquant")
        return {"success": False, "message": "Token manquant"}

    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "Content-Type": "application/json"
    }

    event_payload = {
        "subject": data.get("subject", ""),
        "start": {
            "dateTime": data.get("start"),
            "timeZone": "Europe/Paris"
        },
        "end": {
            "dateTime": data.get("end"),
            "timeZone": "Europe/Paris"
        },
        "location": {
            "displayName": data.get("location", "")
        }
    }

    # Ajout de la catégorie si renseignée
    category = data.get("category")
    if category:
        event_payload["categories"] = [category]

    if data.get("id"):  # Édition
        url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events/{data['id']}"
        response = requests.patch(url, headers=headers, json=event_payload)
        if response.status_code == 200:
            return {"success": True, "message": "Événement mis à jour"}
    else:  # Création
        url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events"
        response = requests.post(url, headers=headers, json=event_payload)
        if response.status_code == 201:
            created_event = response.json()
            return {
                "success": True,
                "message": "Événement créé",
                "id": created_event.get("id")  # 🔁 très utile pour focus/animation côté JS
            }

    print(f"❌ Erreur Graph: {response.status_code} - {response.text}")
    return {"success": False, "message": "Erreur Graph lors de la création ou mise à jour"}

def delete_event(calendar_id, event_id):
    """
    Supprime un événement donné dans le calendrier.
    """
    token = auth.get_token_for_user(config.SCOPE)
    if not token or "access_token" not in token:
        return {"success": False, "message": "Token manquant"}

    headers = {
        "Authorization": f"Bearer {token['access_token']}"
    }

    url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events/{event_id}"
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {"success": True, "message": "Événement supprimé"}
    else:
        print(f"❌ Erreur suppression Graph: {response.status_code} - {response.text}")
        return {"success": False, "message": "Erreur lors de la suppression"}
