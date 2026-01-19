import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ===============================
    # Configurações básicas do Flask
    # ===============================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    FLASK_APP = os.getenv("FLASK_APP", "run")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")

    # ===============================
    # Supabase (REST API / PostgREST)
    # ===============================
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    SUPABASE_REST_URL = (
        f"{SUPABASE_URL}/rest/v1" if SUPABASE_URL else None
    )

    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError(
            "SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY devem estar definidas no .env"
        )

    # ===============================
    # Headers padrão para Supabase REST
    # ===============================
    SUPABASE_HEADERS = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # ===============================
    # E-mail
    # ===============================
    EMAIL_DESTINE = os.getenv("EMAIL_DESTINE")
    EMAIL_SERVER = os.getenv("EMAIL_SERVER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    try:
        EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    except ValueError:
        EMAIL_PORT = 587

    EMAIL_SENDER = os.getenv("EMAIL_SENDER")

    # ===============================
    # Login com Google (OAuth)
    # ===============================
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    # ===============================
    # API Shopee
    # ===============================
    APPID = os.getenv("APPID")
    SECRET = os.getenv("SECRET")
    ENDPOINT = os.getenv("ENDPOINT")