from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
import sqlite3
import os
import sys
print("🚀 Flask Application Running on Docker!")
print("version 1.02")

print("coucou and Welcom !")
import csv
import io
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
        request.args.get('arduino_Id'),
        request.args.get('Value0', None),
        request.args.get('Value1', None),
        request.args.get('Value2', None),
        request.args.get('Value3', None),
        request.args.get('Value4', None),
        request.args.get('Value5', None),
        request.args.get('Value6', None),
        request.args.get('Value7', None),
        request.args.get('Value8', None),
        request.args.get('Value9', None)
    )

    # Stockage des données dans SQLite
    save_to_database(data)
    
    return "Données reçues", 200

# 📌 API pour récupérer les logs
@app.route('/api/logs', methods=['GET'])
def get_logs():
    period = request.args.get("period", "3h")
    arduinoId = request.args.get("arduinoId")
    
    db = get_db()
    cursor = db.cursor()

    query = "SELECT timestamp, arduino_Id, Value0, Value1, Value2, Value3, Value4, Value5, Value6, Value7, Value8, Value9 FROM logs WHERE timestamp >= datetime('now','localtime', ?) "
    params = []

    if period == "7d":
        params.append("-7 days")
    elif period == "30d":
        params.append("-30 days")
    elif period == "24h":
        params.append("-1 day")
    else:
        params.append("-3 hours")

    # Vérifier si arduinoId est fourni et l'ajouter aux conditions
    if arduinoId:
        query += "AND arduino_Id = ? "
        params.append(arduinoId)

    query += "ORDER BY timestamp ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    db.close()

    logs = [{"timestamp": row[0],  # Assurer que c'est un format ISO 8601
                "arduino_Id": row[1],
                "Value0": row[2],
                "Value1": row[3],
                "Value2": row[4],
                "Value3": row[5],
                "Value4": row[6],
                "Value5": row[7],
                "Value6": row[8],
                "Value7": row[9],
                "Value8": row[10],
                "Value9": row[11]} for row in rows]

    return jsonify(logs)

# 📌 API pour exporter les logs en CSV
import datetime

@app.route('/api/export-csv/TemperatureLogs', methods=['GET'])
def export_csv():
    
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")    

    db = get_db()
    cursor = db.cursor()

    print(f"🔍 Requête CSV - Start: {start_date}, End: {end_date}")  # Debug

    # 🔹 Vérifier et convertir le format de date
    try:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("❌ Erreur : format de date incorrect reçu !")
        return "Format de date incorrect", 400

    print(f"✅ Date convertie - Start: {start_date}, End: {end_date}")  # Debug

    cursor.execute("SELECT * FROM logs WHERE timestamp BETWEEN ? AND ?", (start_date, end_date))

    logs = cursor.fetchall()
    db.close()

    # Vérifier s'il y a des logs
    if not logs:
        print("⚠️ Aucun log trouvé pour cette plage de dates !")
    
    # 📌 Création du fichier CSV en mémoire avec UTF-8 + BOM
    output = io.StringIO()
    csv_writer = csv.writer(output, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # 📌 Ajouter le BOM UTF-8 pour compatibilité Excel
    output.write('\ufeff')

    # 📌 Ajouter les en-têtes
    csv_writer.writerow(["Id", "Horodatage", "Plancher Départ", "Plancher Retour", "Départ Alim", "Ambiance", "DeltaT", "Consigne Ambiance", "Consigne Plancher"])

    # 📌 Ajouter les logs
    for row in logs:
        csv_writer.writerow(row)

    output.seek(0)

    # 📌 Générer le fichier CSV pour téléchargement
    filename = f"temperature_logs_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    return send_file(io.BytesIO(output.getvalue().encode("utf-8-sig")), 
                     mimetype="text/csv", 
                     as_attachment=True, 
                     download_name=filename)


# 📌 Fonction pour enregistrer les données dans SQLite
def save_to_database(data):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""INSERT INTO logs (timestamp, arduino_Id, Value0, Value1, Value2, Value3, Value4, Value5, Value6, Value7, Value8, Value9) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)
    db.commit()
    db.close()

# 📌 Connexion à SQLite
def get_db():
    return sqlite3.connect(DATABASE)

# 📌 Lancer Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

