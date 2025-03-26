import identity.web
from flask import session
from config import app_config as config


# 🧠 Création de l'objet Auth à partager dans toute l'app
auth = identity.web.Auth(
    session=session,
    authority=config.AUTHORITY,
    client_id=config.CLIENT_ID,
    client_credential=config.CLIENT_SECRET,
)

