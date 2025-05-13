#!/bin/bash
echo "📦 Déploiement en cours..."

cd /home/Administrateur/arduino-raspi-web || exit 1

# Copier l’override de prod
cp docker-compose.override.prod.yml docker-compose.override.yml

# Charger l’image Docker
docker load -i /home/Administrateur/arduino-app.tar

# Recréer le conteneur
docker-compose down
docker-compose up -d --remove-orphans

echo "✅ Déploiement terminé sur le Raspberry Pi."
