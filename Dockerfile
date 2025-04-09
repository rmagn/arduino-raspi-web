FROM python:3.11-slim

# Installer les dépendances système et les locales
RUN apt-get update && \
    apt-get install -y sqlite3 locales gcc build-essential libffi-dev && \
    echo "fr_FR.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=fr_FR.UTF-8 && \
    apt-get clean

# Définir les variables d'environnement pour les locales
ENV LANG=fr_FR.UTF-8
ENV LANGUAGE=fr_FR:fr
ENV LC_ALL=fr_FR.UTF-8
ENV PYTHONUNBUFFERED=1


# Définir le dossier de travail
WORKDIR /app

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port Flask
EXPOSE 5000

# Commande de démarrage
CMD ["python", "-u", "app.py"]

