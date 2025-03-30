
from flask import Flask
from flask_session import Session
from routes.routes_logger import logger_bp
from routes.routes_pages import pages_bp
from routes.routes_auth import auth_bp
from routes.routes_arduino import arduino_bp
from routes.routes_meteo import meteo_bp
from config import app_config as config
from services.auth_service import auth
from services.scheduler import start_scheduler
from utils.formater import todatetime, format_datetime
from werkzeug.middleware.proxy_fix import ProxyFix

import logging

# Configuration minimale du logger (console uniquement)
logging.basicConfig(
    level=logging.DEBUG,  # ou logging.INFO si tu veux moins de détails
    format="%(asctime)s [%(levelname)s] %(message)s"
)


print("🚀 Flask Application Running on Docker!")
print("version 1.03")

print(f"Mode : {config.ENV_MODE}, Base SQLite : {config.DATABASE}")

app = Flask(__name__, template_folder=config.TEMPLATES_DIR, static_folder=config.STATIC_DIR)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config["TEMPLATES_AUTO_RELOAD"] = config.ENV_MODE == "DEV"
app.secret_key = config.FLASK_SECRET_KEY

app.jinja_env.filters['todatetime'] = todatetime
app.jinja_env.filters['format_datetime'] = format_datetime

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

# print("📚 Liste des routes enregistrées :")
# for rule in app.url_map.iter_rules():
#     print(rule)

# 📌 Lancer le scheduler pour les prévisions météo
start_scheduler() 

# 📌 Lancer Flask
if __name__ == '__main__':
    debug_mode = config.ENV_MODE == "DEV"
    app.run(debug=debug_mode, host="0.0.0.0")