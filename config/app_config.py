from dotenv import load_dotenv
import os

# 🔹 Mode de l’environnement
ENV_MODE = os.getenv("ENV_MODE", "DEV")

# 🔹 Dossiers du projet (restent relatifs)
BASE_DIR = "."
if ENV_MODE == "PROD":
    DATABASE = './data/temperature_logs.db'
else:
    DATABASE = './data/DEV_temperature_logs.db'

# # 🔹 Configuration des chemins et fichiers selon le mode
# if ENV_MODE == "PROD":
#     DATABASE = '/app/data/temperature_logs.db'
#     BASE_DIR = "/app"
# else:
#     DATABASE = './data/DEV_temperature_logs.db'
#     BASE_DIR = "."

# 📂 Dossiers pour Flask
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# 📌 Adresse IP de l’Arduino (à adapter si besoin)
ARDUINO_IP = "http://192.168.1.111:7777/ajax_inputs"
ARDUINO_IP_CHAUDIERE = "http://192.168.1.112:7777/ajax_inputs"

ARDUINO_IPS = {
    "chaudiere": "192.168.1.112",
    "plancher": "192.168.1.111"
}

load_dotenv()  # Charge les variables d'environnement depuis .env

# Application (client) ID of app registration
CLIENT_ID = os.getenv("CLIENT_ID")
# Application's generated client secret: never check this into source control!
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app
#AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID', 'common')}"

REDIRECT_PATH = "/callback" # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# Récupération des événements du calendrier
ENDPOINT_EVENTS = 'https://graph.microsoft.com/v1.0/me/events?$top=5'

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.Read", "Calendars.ReadBasic", "Calendars.Read", "Calendars.ReadWrite"]

# Tells the Flask-session extension to store sessions in the filesystem
SESSION_TYPE = "filesystem"
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
# Using the file system will not work in most production syst
# ems,
# it's better to use a database-backed session store instead.

REDIRECT_HOST = os.getenv("REDIRECT_HOST", "http://localhost:5000")
REDIRECT_URI = REDIRECT_HOST + REDIRECT_PATH

GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

