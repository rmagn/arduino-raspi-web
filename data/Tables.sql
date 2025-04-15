CREATE TABLE logs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  timestamp TIMESTAMP,
  arduino_id INT,
  Value0 INT,
  Value1 INT,
  Value2 INT,
  Value3 INT,
  Value4 INT,
  Value5 INT,
  Value6 INT,
  Value7 INT,
  Value8 INT,
  Value9 INT,
  FOREIGN KEY (arduino_id) REFERENCES arduinos(id)
);

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
    PRIMARY KEY (localite_id, date_heure_utc),
    FOREIGN KEY (localite_id) REFERENCES localites(id)
);

CREATE TABLE IF NOT EXISTS localites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    code_postal TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    UNIQUE(nom, code_postal)
);

CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    birthdate TEXT,
    role TEXT
);
INSERT INTO users (email, first_name, last_name, birthdate, role) VALUES 
('romain_magnan@hotmail.com', 'Romain', 'MAGNAN', '1983-07-01T00:00:00Z','administrateur'),
('marie_aubert26@hotmail.com', 'Marie', 'MAGNAN', '1983-09-11T00:00:00Z','utilisateur');

CREATE TABLE IF NOT EXISTS arduinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    description TEXT,
    adresse_ip TEXT NOT NULL,
);

CREATE TABLE IF NOT EXISTS sensor_aliases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    arduino_id INTEGER NOT NULL,
    index_capteur INTEGER NOT NULL CHECK(index_capteur BETWEEN 0 AND 9),
    alias TEXT NOT NULL,
    type TEXT NOT NULL,
    adresse_mac TEXT,
    FOREIGN KEY (arduino_id) REFERENCES arduinos(id) ON DELETE CASCADE
);
