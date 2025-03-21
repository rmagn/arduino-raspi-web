from flask import Flask
import os
from routes.routes_logger import logger_bp
from routes.routes_pages import pages_bp
from config import app_config as config

print("🚀 Flask Application Running on Docker!")
print("version 1.02")

print(f"Mode : {config.ENV_MODE}, Base SQLite : {config.DATABASE}")

app = Flask(__name__, template_folder=config.TEMPLATES_DIR, static_folder=config.STATIC_DIR)
app.config["TEMPLATES_AUTO_RELOAD"] = config.ENV_MODE == "DEV"

# 📌 Enregistrement des Blueprints
app.register_blueprint(logger_bp)
app.register_blueprint(pages_bp)

# 📌 Lancer Flask
if __name__ == '__main__':
    debug_mode = config.ENV_MODE == "DEV"
    app.run(debug=debug_mode, host="0.0.0.0")