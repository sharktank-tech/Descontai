import os

class Config:
    # ========== Configuração da aplicação ==========
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_APP = os.getenv("FLASK_APP", "run")

    # ========== Configuração do envio de e-mail ==========
    EMAIL_DESTINE = os.getenv("EMAIL_DESTINE")
    SERVIDOR = os.getenv("EMAIL_SERVER", "smtp.gmail.com")
    PASWD = os.getenv("EMAIL_PASSWORD")
    PORTA_SMPT = int(os.getenv("EMAIL_PORT", 587))
    REMETENTE = os.getenv("EMAIL_SENDER")

    # ========== Configuração do login com Google ==========
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")