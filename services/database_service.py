import sqlite3
from config import app_config as config

def get_db():
    """Connexion à SQLite"""
    return sqlite3.connect(config.DATABASE)

def save_to_database(data):
    """Enregistrement des données dans la base SQLite"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO logs (
            timestamp, arduino_Id, Value0, Value1, Value2, Value3, Value4,
            Value5, Value6, Value7, Value8, Value9
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        data
    )
    db.commit()
    db.close()
