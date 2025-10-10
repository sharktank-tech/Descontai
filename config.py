import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()

class Config:
    # Banco de dados
    user = os.getenv("DB_USER")
    raw_password = os.getenv("DB_PASSWORD")
    if raw_password is None:
        raise RuntimeError("Variável de ambiente DB_PASSWORD não está definida.")
    password = quote_plus(raw_password)
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_APP = os.getenv("FLASK_APP", "run")
    UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER')

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
