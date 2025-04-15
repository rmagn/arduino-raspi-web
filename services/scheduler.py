from apscheduler.schedulers.background import BackgroundScheduler
from services.database_service import get_all_localites, insert_meteo_previsions, purge_old_previsions
from services.meteo_client import fetch_meteo_previsions

# 🔁 Scheduler global
scheduler = BackgroundScheduler()

def update_all_localites_previsions():
    purge_old_previsions()  # 🧹 Nettoyage
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
    if not scheduler.running:
        scheduler.start()
        print("✅ Scheduler APS démarré")
    else:
        print("ℹ️ Scheduler déjà en cours")

    # ✅ Ajout du job uniquement s’il n’existe pas déjà
    job_id = "update_previsions_job"
    if not scheduler.get_job(job_id):
        scheduler.add_job(
            func=update_all_localites_previsions,
            trigger="interval",
            minutes=30,
            id=job_id,
            replace_existing=False
        )
        print("🗓️ Job météo ajouté (chaque 30 minutes)")
    else:
        print("⏱️ Job météo déjà existant, non recréé")
