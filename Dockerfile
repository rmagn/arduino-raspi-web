FROM python:3.11-slim

# Installer les dépendances
RUN apt-get update && apt-get install -y sqlite3 && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
