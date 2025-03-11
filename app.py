from flask import Flask, request, jsonify, send_from_directory, render_template
import sqlite3
import os
import sys
print("coucou and Welcom !")

import datetime
import requests

# 🔹 Détermine le mode (dev ou prod)
ENV_MODE = os.getenv("ENV_MODE", "DEV")

# 🔹 Configuration conditionnelle des chemins
if ENV_MODE == "PROD":
    DATABASE = '/app/data/temperature_logs.db'
else:
    DATABASE = './data/DEV_temperature_logs.db'  # Dev local

print(f"Mode : {ENV_MODE}, Base SQLite : {DATABASE}")

# 📂 Définition des chemins
BASE_DIR = "/app"
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)


ARDUINO_IP = "http://192.168.1.111:7777/ajax_inputs"

# 📌 Vérification de la connectivité à l'arduino
@app.route('/arduino_status', methods=['GET'])
def check_arduino():
    print(f"DEBUG: DEV_MODE = {ENV_MODE}")  # Affiche DEV_MODE dans les logs
    
    if ENV_MODE == "DEV":  # Vérification correcte de DEV_MODE
        return jsonify({"status": "OK", "message": "Simulation Arduino connecté"}), 200
    
    try:
        response = requests.get(ARDUINO_IP, timeout=5)
        response.raise_for_status()
        return jsonify({"status": "OK", "message": "Arduino connecté"}), 200
    except requests.exceptions.RequestException:
        return jsonify({"status": "ERROR", "message": "Arduino injoignable"}), 500



# 📌 Route pour la page d'accueil (Dashboard)
@app.route('/')
def home():
    return render_template("index.html")

# 📌 Route pour la page des logs
@app.route('/logs')
def logs():
    return render_template("logs.html")

# 📌 Route pour servir les fichiers statiques
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

# 📌 Enregistrement des températures envoyées par l’Arduino
@app.route('/log', methods=['GET'])
def log_data():
    # Capture l’heure exacte de la réception
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Récupération des valeurs envoyées par l’Arduino
    data = (
        timestamp,
        request.args.get('temp_plancher_depart'),
        request.args.get('temp_plancher_retour'),
        request.args.get('temp_depart_alim'),
        request.args.get('temp_ambiance'),
        request.args.get('deltaT')
    )

    # Stockage des données dans SQLite
    save_to_database(data)
    
    return "Données reçues", 200

# 📌 API pour récupérer les logs
@app.route('/api/logs', methods=['GET'])
def get_logs():
    period = request.args.get("period", "3h")
    
    db = get_db()
    cursor = db.cursor()

    if period == "7d":
        cursor.execute("SELECT timestamp, temp_plancher_depart, temp_plancher_retour, temp_depart_alim, temp_ambiance, deltaT FROM logs WHERE timestamp >= datetime('now', '-7 days') ORDER BY timestamp ASC")
    elif period == "30d":
        cursor.execute("SELECT timestamp, temp_plancher_depart, temp_plancher_retour, temp_depart_alim, temp_ambiance, deltaT FROM logs WHERE timestamp >= datetime('now', '-30 days') ORDER BY timestamp ASC")
    elif period == "24h":
        cursor.execute("SELECT timestamp, temp_plancher_depart, temp_plancher_retour, temp_depart_alim, temp_ambiance, deltaT FROM logs WHERE timestamp >= datetime('now', '-1 day') ORDER BY timestamp ASC")
    else:
        cursor.execute("SELECT timestamp, temp_plancher_depart, temp_plancher_retour, temp_depart_alim, temp_ambiance, deltaT  FROM logs WHERE timestamp >= datetime('now', '-3 hours') ORDER BY timestamp ASC")

    rows = cursor.fetchall()
    db.close()

    logs = [{"timestamp": row[0],  # Assurer que c'est un format ISO 8601
             "temp_plancher_depart": row[1], 
             "temp_plancher_retour": row[2],
             "temp_depart_alim": row[3], 
             "temp_ambiance": row[4], 
             "deltaT": row[5]} for row in rows]

    return jsonify(logs)



# 📌 Fonction pour enregistrer les données dans SQLite
def save_to_database(data):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""INSERT INTO logs (timestamp, temp_plancher_depart, temp_plancher_retour, 
                        temp_depart_alim, temp_ambiance, deltaT) VALUES (?, ?, ?, ?, ?, ?)""", data)
    db.commit()
    db.close()

# 📌 Connexion à SQLite
def get_db():
    return sqlite3.connect(DATABASE)

# 📌 Lancer Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

