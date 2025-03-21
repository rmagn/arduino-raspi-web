from dotenv import load_dotenv
import os

# 🔹 Mode de l’environnement
ENV_MODE = os.getenv("ENV_MODE", "DEV")

# 🔹 Configuration des chemins et fichiers selon le mode
if ENV_MODE == "PROD":
    DATABASE = '/app/data/temperature_logs.db'
    BASE_DIR = "/app"
else:
    DATABASE = './data/DEV_temperature_logs.db'
    BASE_DIR = "."

# 📂 Dossiers pour Flask
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# 📌 Adresse IP de l’Arduino (à adapter si besoin)
ARDUINO_IP = "http://192.168.1.111:7777/ajax_inputs"

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
SCOPE = ["User.ReadBasic.All", "Calendars.ReadBasic", "Calendars.Read", "Calendars.ReadWrite"]

# Tells the Flask-session extension to store sessions in the filesystem
SESSION_TYPE = "filesystem"
# Using the file system will not work in most production systems,
# it's better to use a database-backed session store instead.

# Vérifie que tout est bien chargé
# Vérifie que tout est bien chargé
print(f'####################################################')
print(f"# ENV_MODE: {ENV_MODE}")
print(f"# DATABASE: {DATABASE}")
print(f"# BASE_DIR: {BASE_DIR}")
print(f"# TEMPLATES_DIR: {TEMPLATES_DIR}")
print(f"# STATIC_DIR: {STATIC_DIR}")
print(f"# ARDUINO_IP: {ARDUINO_IP}")
print(f"# CLIENT_ID: {CLIENT_ID}")
print(f"# CLIENT_SECRET: {CLIENT_SECRET}")
print(f"# AUTHORITY: {AUTHORITY}")
print(f"# REDIRECT_PATH: {REDIRECT_PATH}")
print(f"# ENDPOINT: {ENDPOINT}")
print(f"# ENDPOINT_EVENTS: {ENDPOINT_EVENTS}")
print(f"# SCOPE: {SCOPE}")
print(f"# SESSION_TYPE: {SESSION_TYPE}")
print(f'####################################################')