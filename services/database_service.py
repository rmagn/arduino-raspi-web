import sqlite3
from datetime import datetime, timezone as dt_timezone  # Renamed to avoid conflict
from config import app_config as config
from dateutil import parser
from pytz import timezone as pytz_timezone  # Renamed to avoid conflict
from utils.formater import to_local_datetime

def get_db():
    """Connexion à SQLite"""
    return sqlite3.connect(config.DATABASE)

bufferLog = []

def saveLog_to_database(data):
    """Enregistrement des données dans un buffer et insertion dans la base SQLite lorsque le buffer est plein"""
    global bufferLog
    bufferLog.append(data)
    
    if len(bufferLog) >= 10:  # Vérifie si le buffer contient 10 lignes
        db = get_db()
        cursor = db.cursor()
        cursor.executemany("""
            INSERT INTO logs (
                timestamp, arduino_Id, Value0, Value1, Value2, Value3, Value4,
                Value5, Value6, Value7, Value8, Value9
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            bufferLog
        )
        db.commit()
        db.close()
        bufferLog = []  # Vide le buffer après insertion

def insert_meteo_previsions(localite_id, data1, data2):
    conn = get_db()
    cur = conn.cursor()
    dates = data1["data"][0]["coordinates"][0]["dates"]

    for i in range(len(dates)):
        values = {
            "localite_id": localite_id,
            "date_heure_utc": dates[i]["date"],
            "wind_speed": data1["data"][0]["coordinates"][0]["dates"][i]["value"],
            "wind_dir": data1["data"][1]["coordinates"][0]["dates"][i]["value"],
            "wind_gusts_1h": data1["data"][2]["coordinates"][0]["dates"][i]["value"],
            "wind_gusts_24h": data1["data"][3]["coordinates"][0]["dates"][i]["value"],
            "temp": data1["data"][4]["coordinates"][0]["dates"][i]["value"],
            "temp_max": data1["data"][5]["coordinates"][0]["dates"][i]["value"],
            "temp_min": data1["data"][6]["coordinates"][0]["dates"][i]["value"],
            "pression": data1["data"][7]["coordinates"][0]["dates"][i]["value"],
            "pluie_1h": data1["data"][8]["coordinates"][0]["dates"][i]["value"],
            "pluie_24h": data1["data"][9]["coordinates"][0]["dates"][i]["value"],
            "symbole_1h": data2["data"][0]["coordinates"][0]["dates"][i]["value"],
            "symbole_24h": data2["data"][1]["coordinates"][0]["dates"][i]["value"],
            "uv": data2["data"][2]["coordinates"][0]["dates"][i]["value"],
            "lever_soleil": data2["data"][3]["coordinates"][0]["dates"][i]["value"],
            "coucher_soleil": data2["data"][4]["coordinates"][0]["dates"][i]["value"]
        }

        cur.execute("""
            INSERT OR REPLACE INTO meteo_previsions (
                localite_id, date_heure_utc, wind_speed, wind_dir, wind_gusts_1h, wind_gusts_24h,
                temp, temp_max, temp_min, pression, pluie_1h, pluie_24h,
                symbole_1h, symbole_24h, uv, lever_soleil, coucher_soleil
            ) VALUES (
                :localite_id, :date_heure_utc, :wind_speed, :wind_dir, :wind_gusts_1h, :wind_gusts_24h,
                :temp, :temp_max, :temp_min, :pression, :pluie_1h, :pluie_24h,
                :symbole_1h, :symbole_24h, :uv, :lever_soleil, :coucher_soleil
            )
        """, values)

    conn.commit()
    conn.close()

def get_Ephemeris():
    """Récupère les éphémérides (lever et coucher de soleil)"""
    conn = get_db()
    cur = conn.cursor()
    today_date = datetime.now(dt_timezone.utc).strftime("%Y-%m-%dT12:00:00Z")  # Use datetime.timezone
    cur.execute("""
        SELECT lever_soleil, coucher_soleil
        FROM meteo_previsions        
        WHERE localite_id = 1 AND date_heure_utc = ?
    """, (today_date,))
    rows = cur.fetchall()
    conn.close()

    if rows:
        lever_soleil_utc = to_local_datetime(rows[0][0])
        coucher_soleil_utc = to_local_datetime(rows[0][1])

        # Convertir en heure
        lever_soleil_local = lever_soleil_utc.strftime("%H:%M")
        coucher_soleil_local = coucher_soleil_utc.strftime("%H:%M")

        return {
            "lever_soleil": lever_soleil_local,
            "coucher_soleil": coucher_soleil_local
        }
    return None

def get_all_localites():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nom, latitude, longitude FROM localites")
    rows = cursor.fetchall()
    db.close()
    return rows

def purge_old_previsions():
    """Supprime les prévisions dont la date est passée (en UTC)"""
    utc_now = datetime.now(dt_timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        DELETE FROM meteo_previsions
        WHERE date_heure_utc < ?
    """, (utc_now,))
    db.commit()
    db.close()
    print(f"🧹 Purge terminée. Prévisions avant {utc_now} supprimées.")

def get_all_previsions(localite_id):
    """Récupère toutes les prévisions"""
    db = get_db()
    today_date = datetime.now(dt_timezone.utc).strftime("%Y-%m-%dT%H:00:00Z")  # Use datetime.timezone
    cursor = db.cursor()
    cursor.execute("""
        SELECT localites.nom, meteo_previsions.*
        FROM meteo_previsions
                   JOIN localites ON meteo_previsions.localite_id = localites.id
        WHERE localite_id = ? AND  date_heure_utc >= ?
        ORDER BY date_heure_utc ASC
    """, (localite_id,today_date))
    rows = cursor.fetchall()
    db.close()

    previsions = []
    for row in rows:
        prevision = {
            "localite_nom": row[0],
            "localite_id": row[1],
            "date_heure_utc": row[2],
            "wind_speed": row[3],
            "wind_dir": row[4],
            "wind_gusts_1h": row[5],
            "wind_gusts_24h": row[6],
            "temp": row[7],
            "temp_max": row[8],
            "temp_min": row[9],
            "pression": row[10],
            "pluie_1h": row[11],
            "pluie_24h": row[12],
            "symbole_1h": row[13],
            "symbole_24h": row[14],
            "uv": row[15],
        }
        previsions.append(prevision)

    return previsions