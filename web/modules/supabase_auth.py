import requests
from flask_login import UserMixin
from config import Config

class SupabaseUser(UserMixin):
    def __init__(self, data):
        self.id = data["id"]
        self.email = data["email"]
        self.username = data.get("username", "")

def get_user_by_id(user_id):
    url = f"{Config.SUPABASE_REST_URL}/users?id=eq.{user_id}"
    headers = {
        "apikey": Config.SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {Config.SUPABASE_ANON_KEY}",
    }
    r = requests.get(url, headers=headers)
    data = r.json()
    return SupabaseUser(data[0]) if data else None