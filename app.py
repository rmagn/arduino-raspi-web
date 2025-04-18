from flask import Flask
from flask_session import Session
from flask_migrate import Migrate


from routes.routes_logger import logger_bp
from routes.routes_pages import pages_bp
from routes.routes_auth import auth_bp
from routes.routes_arduino import arduino_bp
from routes.routes_meteo import meteo_bp
from routes.routes_api_user import api_user
from routes.routes_api_calendar import api_calendar
from routes.routes_admin import admin_bp
from Features.HardwareManagement.hardware_routes import alias_bp
from Features.Bank.bank_route import bank_bp
from Features.Bank.bank_ml import predictor  # Import pour initialiser le prédicteur

from config import app_config as config
from services.auth_manager import get_user, get_user_photo
from services.oauth_client import oauth
from services.oauth_register import register_providers
from services.scheduler import start_scheduler

from utils.formater import todatetime, format_datetime,format_date_fr

from werkzeug.middleware.proxy_fix import ProxyFix
from models import db
import logging
import os
import sys

# Configuration minimale du logger (console uniquement)
logging.basicConfig(
    level=logging.INFO,  # ou logging.INFO si tu veux moins de détails
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Utiliser sys.stdout pour Docker
    ]
)

# Configuration spécifique pour le prédicteur
bank_logger = logging.getLogger('Features.Bank.bank_ml')
bank_logger.setLevel(logging.INFO)
if not bank_logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))
    bank_logger.addHandler(handler)
bank_logger.propagate = True  # Permettre la propagation des logs

# Configuration pour tous les loggers
for logger_name in ['Features.Bank.bank_ml', 'Features.Bank.bank_route']:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))
        logger.addHandler(handler)
    logger.propagate = True

print("🚀 Flask Application Running on Docker!")
print("version 1.05")

print(f"Mode : {config.ENV_MODE}, Base SQLite : {config.DATABASE}")

app = Flask(__name__, template_folder=config.TEMPLATES_DIR, static_folder=config.STATIC_DIR)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config["TEMPLATES_AUTO_RELOAD"] = config.ENV_MODE == "DEV"
app.secret_key = config.FLASK_SECRET_KEY

oauth.init_app(app)
register_providers(app)

app.jinja_env.filters['todatetime'] = todatetime
app.jinja_env.filters['format_datetime'] = format_datetime
app.jinja_env.filters['format_date_fr'] = format_date_fr

# 📦 SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath(config.DATABASE)}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


# 🔐 context processor pour injecter "current_user" automatiquement dans tous les templates
@app.context_processor
def inject_user():
    return {"current_user": get_user()}


@app.context_processor
def inject_user_avatar():
    return {"user_photo": get_user_photo()}


# 🔐 Active le stockage serveur de session
app.config["SESSION_TYPE"] = config.SESSION_TYPE
Session(app)

# 📌 Enregistrement des Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(logger_bp)
app.register_blueprint(pages_bp)
app.register_blueprint(arduino_bp, url_prefix="/arduino")
app.register_blueprint(meteo_bp)
app.register_blueprint(api_user)
app.register_blueprint(api_calendar)
app.register_blueprint(admin_bp)
app.register_blueprint(alias_bp)
app.register_blueprint(bank_bp)

# 📌 Lancer le scheduler pour les prévisions météo
start_scheduler() 

# 📌 Lancer Flask
if __name__ == '__main__':
    debug_mode = config.ENV_MODE == "DEV"
    app.run(debug=debug_mode, host="0.0.0.0")