#!/bin/bash

# 🧠 Variables à personnaliser si besoin
RASPBERRY_USER="Administrateur"
RASPBERRY_HOST="192.168.1.176"
RASPBERRY_PATH="/home/Administrateur"
REMOTE_PROJECT_DIR="$RASPBERRY_PATH/arduino-raspi-web"
IMAGE_NAME="magnus-home"
TAR_NAME="${IMAGE_NAME}.tar"

echo "🚀 Build de l'image Docker pour ARMv7..."
docker buildx build --platform linux/arm/v7 -t $IMAGE_NAME:latest -o type=docker,dest=$TAR_NAME .

echo "📤 Transfert de l'image Docker vers le Raspberry Pi..."
scp $TAR_NAME ${RASPBERRY_USER}@${RASPBERRY_HOST}:$RASPBERRY_PATH

echo "🔧 Exécution du script de déploiement sur le Raspberry Pi..."
ssh ${RASPBERRY_USER}@${RASPBERRY_HOST} "cd $REMOTE_PROJECT_DIR && ./deploy.sh"

echo "🧹 Nettoyage local du fichier image..."
rm -f $TAR_NAME

echo "✅ Déploiement terminé avec succès."
