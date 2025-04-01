from flask import Flask
from flask_session import Session
from routes.routes_logger import logger_bp
from routes.routes_pages import pages_bp
from routes.routes_auth import auth_bp
from routes.routes_arduino import arduino_bp
from routes.routes_meteo import meteo_bp
from routes.routes_api_user import api_user
from routes.routes_api_calendar import api_calendar
from routes.routes_admin import admin_bp

from config import app_config as config
from services.auth_service import auth
from services.scheduler import start_scheduler
from utils.formater import todatetime, format_datetime,format_date_fr
from werkzeug.middleware.proxy_fix import ProxyFix
from models import db
import logging
import os

# Configuration minimale du logger (console uniquement)
logging.basicConfig(
    #level=logging.INFO,  # ou logging.INFO si tu veux moins de détails
    level=logging.DEBUG,  # ou logging.INFO si tu veux moins de détails
    format="%(asctime)s [%(levelname)s] %(message)s"
)


print("🚀 Flask Application Running on Docker!")
print("version 1.04")

print(f"Mode : {config.ENV_MODE}, Base SQLite : {config.DATABASE}")

# print("📂 Chemin absolu DB :", os.path.abspath(config.DATABASE))
# print("🛠 Existe ?          :", os.path.exists(config.DATABASE))
# print("✍️ Droit d'écriture :", os.access(os.path.dirname(config.DATABASE), os.W_OK))

app = Flask(__name__, template_folder=config.TEMPLATES_DIR, static_folder=config.STATIC_DIR)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config["TEMPLATES_AUTO_RELOAD"] = config.ENV_MODE == "DEV"
app.secret_key = config.FLASK_SECRET_KEY


app.jinja_env.filters['todatetime'] = todatetime
app.jinja_env.filters['format_datetime'] = format_datetime
app.jinja_env.filters['format_date_fr'] = format_date_fr

# 📦 SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath(config.DATABASE)}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 🔐 context processor pour injecter "current_user" automatiquement dans tous les templates
@app.context_processor
def inject_user():
    return {"current_user": auth.get_user()}

@app.context_processor
def inject_user_avatar():
    from services.graph_service import get_user_photo
    user_photo = get_user_photo()
    return dict(user_photo = user_photo )


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

# print("📚 Liste des routes enregistrées :")
#for rule in app.url_map.iter_rules():
#   print(rule)

# 📌 Lancer le scheduler pour les prévisions météo
start_scheduler() 

# 📌 Lancer Flask
if __name__ == '__main__':
    debug_mode = config.ENV_MODE == "DEV"
    app.run(debug=debug_mode, host="0.0.0.0")