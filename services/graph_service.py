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
        "fields": "subject,organizer,start,end",                 
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
            # print("✅ Récupération des événements OK")
            events.extend(response.json().get("value", []))
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
