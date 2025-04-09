# services/oauth_register.py
from services.oauth_client import oauth
from config import app_config as config

def register_providers(app):
    oauth.init_app(app)
    oauth.register(
    name='google',
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile https://www.googleapis.com/auth/calendar'
    }
)

