from flask import Blueprint, request, jsonify, send_file
import io
import csv
import datetime
from services.database_service import get_db, saveLog_to_database

logger_bp = Blueprint("logger", __name__)

# 📈 Enregistrement des températures envoyées par l’Arduino
@logger_bp.route('/log', methods=['GET'])
def log_data():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    saveLog_to_database(data)
    return "Données reçues", 200


# 🔹 API pour récupérer les logs
@logger_bp.route('/api/logs', methods=['GET'])
def get_logs():
    period = request.args.get("period", "3h")
    arduinoId = request.args.get("arduinoId")

    db = get_db()
    cursor = db.cursor()

    query = """
        SELECT timestamp, arduino_Id, Value0, Value1, Value2, Value3, Value4, Value5, Value6, Value7, Value8, Value9
        FROM logs
        WHERE timestamp >= datetime('now','localtime', ?) 
    """
    params = []

    if period == "7d":
        params.append("-7 days")
    elif period == "30d":
        params.append("-30 days")
    elif period == "24h":
        params.append("-1 day")
    else:
        params.append("-3 hours")

    if arduinoId:
        query += "AND arduino_Id = ? "
        params.append(arduinoId)

    query += "ORDER BY timestamp ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    db.close()

    logs = [{
        "timestamp": row[0],
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
        "Value9": row[11]
    } for row in rows]

    return jsonify(logs)


# 🔹 API pour exporter les logs en CSV
@logger_bp.route('/api/export-csv/TemperatureLogs', methods=['GET'])
def export_csv():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    db = get_db()
    cursor = db.cursor()

    try:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return "Format de date incorrect", 400

    cursor.execute("SELECT * FROM logs WHERE timestamp BETWEEN ? AND ?", (start_date, end_date))
    logs = cursor.fetchall()
    db.close()

    output = io.StringIO()
    csv_writer = csv.writer(output, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    output.write('\ufeff')

    csv_writer.writerow(["Id", "Horodatage", "Arduino_Id", "Value0", "Value1", "Value2", "Value3", "Value4", "Value5", "Value6", "Value7", "Value8", "Value9"])

    for row in logs:
        csv_writer.writerow(row)

    output.seek(0)

    filename = f"temperature_logs_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    return send_file(io.BytesIO(output.getvalue().encode("utf-8-sig")), 
                     mimetype="text/csv", 
                     as_attachment=True, 
                     download_name=filename)
