import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ===============================
    # Flask
    # ===============================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    FLASK_APP = os.getenv("FLASK_APP", "run")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")

    # ===============================
    # Supabase
    # ===============================
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Configuração do Supabase incompleta.")

    SUPABASE_REST_URL = f"{SUPABASE_URL.rstrip('/')}/rest/v1"

    SUPABASE_HEADERS = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    }

    # ===============================
    # Email
    # ===============================
    EMAIL_DESTINE = os.getenv("EMAIL_DESTINE")
    EMAIL_SERVER = os.getenv("EMAIL_SERVER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")

    # ===============================
    # OAuth
    # ===============================
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    # ===============================
    # Shopee
    # ===============================
    APPID = os.getenv("APPID")
    SECRET = os.getenv("SECRET")
    ENDPOINT = os.getenv("ENDPOINT")