from datetime import datetime, timedelta
import locale

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


# 📅 Récupère les dates de début et de fin pour une semaine donnée
def get_week_bounds(offset_weeks=0):
    """
    Retourne les dates de début et de fin pour une semaine donnée (offset = 0 = semaine actuelle, 1 = semaine suivante).
    """
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=offset_weeks)

    if offset_weeks == 0:
        start_of_week = today
        
    if offset_weeks < 2 :        
        end_of_week = start_of_week + timedelta(days=7)
    else:
        print("📅 Récupération des événements à long terme")
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=offset_weeks)
        end_of_week = start_of_week + timedelta(weeks=10) 

    return start_of_week, end_of_week