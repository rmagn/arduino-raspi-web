import sqlite3

# Connexion à la base existante
db_path = "DEV_temperature_logs.db"  # ou le chemin complet si ailleurs
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Création de la nouvelle table
cursor.execute("""
CREATE TABLE meteo_previsions (
    localite_id TEXT,
    date_heure_utc TEXT,
    wind_speed REAL,
    wind_dir REAL,
    wind_gusts_1h REAL,
    wind_gusts_24h REAL,
    temp REAL,
    temp_max REAL,
    temp_min REAL,
    pression REAL,
    pluie_1h REAL,
    pluie_24h REAL,
    symbole_1h INTEGER,
    symbole_24h INTEGER,
    uv REAL,
    lever_soleil TEXT,
    coucher_soleil TEXT,
    PRIMARY KEY (localite_id, date_heure_utc)
);
CREATE TABLE IF NOT EXISTS localites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    code_postal TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    UNIQUE(nom, code_postal)
);
""")

conn.commit()
conn.close()
print("✅ Table 'meteo_previsions' créée avec succès.")
