import requests
import time
import json
import os

# Caminho do arquivo de tokens
TOKEN_PATH = 'web/modules/tokens/tokens.json'

# Substitua com os seus dados reais
CLIENT_ID = '1364577661162644'
CLIENT_SECRET = 'bvV8CKao9RNJ6tim83J7Krr6DUaWRMpQ'


def refresh_token():
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError("Arquivo tokens.json não encontrado.")

    with open(TOKEN_PATH, 'r') as f:
        tokens = json.load(f)

    url = 'https://api.mercadolibre.com/oauth/token'

    payload = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': tokens['refresh_token']
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        print(f"Erro ao renovar token: {response.status_code}")
        print(response.json())
        return None

    new_tokens = response.json()

    with open(TOKEN_PATH, 'w') as f:
        json.dump({
            'access_token': new_tokens['access_token'],
            'refresh_token': new_tokens.get('refresh_token', tokens['refresh_token']),
            'expires_in': new_tokens['expires_in'],
            'timestamp': time.time()
        }, f, indent=2)

    return new_tokens['access_token']


def get_access_token():
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError("Arquivo tokens.json não encontrado.")

    with open(TOKEN_PATH, 'r') as f:
        tokens = json.load(f)

    expires_in = tokens.get('expires_in', 0)
    timestamp = tokens.get('timestamp', 0)

    # Verifica se o token está expirado ou quase expirando
    if time.time() - timestamp > expires_in - 60:
        return refresh_token()

    return tokens['access_token']