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


INSERT INTO bank_categories (id, nom) VALUES (1, 'Alimentation');
INSERT INTO bank_categories (id, nom) VALUES (2, 'Banque');
INSERT INTO bank_categories (id, nom) VALUES (3, 'Dons & Cadeaux');
INSERT INTO bank_categories (id, nom) VALUES (4, 'Enfants');
INSERT INTO bank_categories (id, nom) VALUES (5, 'Épargnes');
INSERT INTO bank_categories (id, nom) VALUES (6, 'Imprévus / Divers');
INSERT INTO bank_categories (id, nom) VALUES (7, 'Logement');
INSERT INTO bank_categories (id, nom) VALUES (8, 'Loisirs & Culture');
INSERT INTO bank_categories (id, nom) VALUES (9, 'Professionnel');
INSERT INTO bank_categories (id, nom) VALUES (10, 'Provisions');
INSERT INTO bank_categories (id, nom) VALUES (11, 'Revenus');
INSERT INTO bank_categories (id, nom) VALUES (12, 'Santé');
INSERT INTO bank_categories (id, nom) VALUES (13, 'Transport');
INSERT INTO bank_categories (id, nom) VALUES (14, 'Vie quotidienne');
INSERT INTO bank_categories (id, nom) VALUES (15, 'Virement');

-- Alimentation (1)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (1, 'Supermarché', 1);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (2, 'Marché / producteurs', 1);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (3, 'Courses Drive / en ligne', 1);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (4, 'Dépenses imprévues', 1);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (5, 'Pain', 1);

-- Banque (2)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (6, 'Frais bancaire', 2);

-- Dons & Cadeaux (3)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (7, 'Cadeaux (anniversaires, Noël...)', 3);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (8, 'Dons associatifs', 3);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (9, 'Aide familiale', 3);

-- Enfants (4)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (10, 'Cantine / Garderie / Internat', 4);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (11, 'Activités extrascolaires', 4);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (12, 'Transport scolaire', 4);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (13, 'Voyage scolaire', 4);

-- Épargnes (5)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (14, 'Enfants', 5);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (76, 'A catégoriser', 5);

-- Imprévus / Divers (6)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (15, 'Petits achats non classés', 6);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (16, 'Réparations', 6);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (17, 'Amendes, pénalités', 6);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (18, 'Autres', 6);

-- Logement (7)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (19, 'Crédit immobilier', 7);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (20, 'Bois de Chauffage', 7);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (21, 'Assurance habitation', 7);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (22, 'Électricité / Gaz', 7);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (23, 'Eau', 7);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (24, 'Internet / Téléphone fixe', 7);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (25, 'Impots / Taxes', 7);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (26, 'Assurance pret', 7);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (27, 'Ménage', 7);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (28, 'Équipements', 7);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (29, 'Loyer', 7);

-- Loisirs & Culture (8)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (30, 'Sorties / Restaurants', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (31, 'Livres / Films / Musées', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (32, 'Activités sportives', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (33, 'Musique', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (34, 'Vacances / Week-end', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (35, 'Assurance Caravane', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (36, 'Bricolage', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (37, 'Jardinage', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (38, 'Jeux video', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (39, 'Aquarelle / dessin', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (40, 'Geek', 8);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (41, 'Jeux / puzzle', 8);

-- Professionnel (9)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (42, 'Assurance Responsabilité civile', 9);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (43, 'Téléphone pro', 9);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (44, 'Notes de Frais', 9);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (45, 'Materiel grapho', 9);

-- Provisions (10)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (46, 'Bois', 10);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (47, 'Entretiens véhicules', 10);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (48, 'Frais de scolarité', 10);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (49, 'Vacances', 10);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (50, 'Impots', 10);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (51, 'Othodontie', 10);

-- Revenus (11)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (52, 'Salaire', 11);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (53, 'Allocation familliale', 11);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (54, 'Remboursement note de frais', 11);

-- Santé (12)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (55, 'Mutuelle', 12);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (56, 'Médecin', 12);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (57, 'Soins dentaires / optiques', 12);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (58, 'Thérapies / bien-être', 12);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (59, 'Pharmacie', 12);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (60, 'Remboursement CPAM', 12);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (61, 'Remboursement mutuelle', 12);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (62, 'Ostheo / Kine / Chiro / Acuponcture', 12);

-- Transport (13)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (63, 'Carburant', 13);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (64, 'Assurance auto', 13);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (65, 'Entretien / Réparations', 13);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (66, 'Transport en commun', 13);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (67, 'Péages / Parking', 13);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (68, 'Equipements', 13);

-- Vie quotidienne (14)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (69, 'Habillement', 14);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (70, 'Hygiène / beauté', 14);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (71, 'Abonnements (Netflix, Spotify…)', 14);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (72, 'Téléphonie mobile', 14);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (73, 'Assurance Multirisque/Assistance juridique', 14);
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (74, 'Cotisation syndicat', 14);

-- Virements (15)
INSERT INTO bank_sous_categories (id, nom, categorie_id) VALUES (75, 'retour provision', 15);