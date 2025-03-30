from apscheduler.schedulers.background import BackgroundScheduler
from services.database_service import get_all_localites, insert_meteo_previsions, purge_old_previsions
from services.meteo_client import fetch_meteo_previsions

def update_all_localites_previsions():
    purge_old_previsions()  # 🧹 Nettoyage d'abord
    localites = get_all_localites()
    for loc_id, nom, lat, lon in localites:
        print(f"⏳ Mise à jour de {nom}...")
        try:
            data1, data2 = fetch_meteo_previsions(lat, lon)
            insert_meteo_previsions(loc_id, data1, data2)
            print(f"✅ Prévisions insérées pour {nom}")
        except Exception as e:
            print(f"❌ Erreur pour {nom} : {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_all_localites_previsions, trigger="interval", minutes=30)
    scheduler.start()
    print("⏱️ Scheduler météo lancé (intervalle : 30 minutes)")
