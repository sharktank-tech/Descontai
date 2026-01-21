import requests
from flask import current_app


def supabase_headers():
    return {
        "apikey": current_app.config["SUPABASE_SERVICE_ROLE_KEY"],
        "Authorization": f"Bearer {current_app.config['SUPABASE_SERVICE_ROLE_KEY']}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }


def supabase_get(table, params=None):
    url = f"{current_app.config['SUPABASE_REST_URL']}/{table}"
    return requests.get(url, headers=supabase_headers(), params=params)


def supabase_post(table, data):
    url = f"{current_app.config['SUPABASE_REST_URL']}/{table}"
    return requests.post(url, headers=supabase_headers(), json=data)


def supabase_patch(table, record_id, data):
    url = f"{current_app.config['SUPABASE_REST_URL']}/{table}"
    params = {"id": f"eq.{record_id}"}
    return requests.patch(url, headers=supabase_headers(), params=params, json=data)


def supabase_delete(table, record_id):
    url = f"{current_app.config['SUPABASE_REST_URL']}/{table}"
    params = {"id": f"eq.{record_id}"}
    return requests.delete(url, headers=supabase_headers(), params=params)
