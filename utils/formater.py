from datetime import datetime, timedelta
import locale
import pytz

# 🔁 Force le format français
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    # Pour Windows ou systèmes ne supportant pas fr_FR.UTF-8
    locale.setlocale(locale.LC_TIME, 'fr_FR')

# 🔄 Convertit l'ISO 8601 en datetime Python
def todatetime(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))

# 📅 Formatte selon le format demandé
def format_datetime(value, format_str="%A %d %B %Y %H:%M"):
    return value.strftime(format_str)

# 📅 Convertit une date UTC en en datetime local (Europe/Paris)
def to_local_datetime(utc_str):
    """
    Convertit une date UTC (str) en datetime local (Europe/Paris)
    """
    utc_dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    paris_tz = pytz.timezone("Europe/Paris")
    return utc_dt.astimezone(paris_tz)

# 📅 Récupère les dates de début et de fin pour une semaine donnée
def get_week_bounds(offset_weeks=0):
    """
    Retourne les dates de début et de fin pour une semaine donnée.
    - offset_weeks = 0 → aujourd'hui à dimanche de cette semaine
    - offset_weeks = 1 → lundi prochain à dimanche suivant
    - offset_weeks >= 2 → lundi de la semaine + 10 semaines
    """
    today = datetime.now()

    if offset_weeks == 0:
        start_of_week = today
        # Fin = dimanche de cette semaine (dimanche = 6)
        days_until_sunday = 6 - today.weekday()
        end_of_week = today + timedelta(days=days_until_sunday)
    elif offset_weeks == 1:
        # Semaine suivante, lundi → dimanche
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=1)
        end_of_week = start_of_week + timedelta(days=6)
    else:
        print("📅 Récupération des événements à long terme")
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=offset_weeks)
        end_of_week = start_of_week + timedelta(weeks=10)

    return start_of_week, end_of_week
