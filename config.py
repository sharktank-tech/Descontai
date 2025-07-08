# config.py
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (apenas em desenvolvimento)
load_dotenv()

class Config:
    # Banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"

    # Segurança
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # E-mail
    EMAIL_DESTINE = os.environ.get("EMAIL_DESTINE")
    EMAIL_SERVER = os.environ.get("EMAIL_SERVER")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
    EMAIL_SENDER = os.environ.get("EMAIL_SENDER")

    # Login com Google
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
