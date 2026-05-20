import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # ============== Flask =================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    FLASK_APP = os.getenv("FLASK_APP", "run")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")

    # ============== Database =================
    DATABASE_URL = os.getenv("DATABASE_URL") or '//postgres:NDsfA3kxD5guZOLa@db.zbhornbobznuzollgovo.supabase.co:5432/postgres'
    DATABASE_KEY = os.getenv("DATABASE_KEY")
    DATABASE_SERVICE_ROLE_KEY = os.getenv("DATABASE_SERVICE_ROLE_KEY")

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL não configurada.")

    # ============= SQLAlchemy ==================
    SQLALCHEMY_DATABASE_URI = (
        DATABASE_URL
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # ============= Email ==================
    EMAIL_DESTINE = os.getenv("EMAIL_DESTINE")
    EMAIL_SERVER = os.getenv("EMAIL_SERVER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")

    # ============= OAuth ==================
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    # ============ Shopee ===================
    APPID = os.getenv("APPID")
    SECRET = os.getenv("SECRET")
    ENDPOINT = os.getenv("ENDPOINT")