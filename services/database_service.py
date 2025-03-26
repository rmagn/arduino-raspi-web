import sqlite3
from config import app_config as config

def get_db():
    """Connexion à SQLite"""
    return sqlite3.connect(config.DATABASE)

bufferLog = []

def saveLog_to_database(data):
    """Enregistrement des données dans un buffer et insertion dans la base SQLite lorsque le buffer est plein"""
    global buffer
    buffer.append(data)
    
    if len(buffer) >= 10:  # Vérifie si le buffer contient 10 lignes
        db = get_db()
        cursor = db.cursor()
        cursor.executemany("""
            INSERT INTO logs (
                timestamp, arduino_Id, Value0, Value1, Value2, Value3, Value4,
                Value5, Value6, Value7, Value8, Value9
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            buffer
        )
        db.commit()
        db.close()
        bufferLog = []  # Vide le buffer après insertion
