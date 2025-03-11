# Arduino - Régulation Plancher Chauffant

Application Web de monitoring des températures via Raspberry Pi, Arduino et SQLite.

## Technologies utilisées
- Python / Flask
- SQLite
- Docker
- Arduino + Shield Ethernet

## Structure du projet
- `data/` - Base SQLite
- `templates/` - Pages web HTML
- `Dockerfile` - Environnement Docker
- `docker-compose.yml`

## Installation
```bash
docker-compose up -d
