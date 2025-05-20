import requests

# Substitua pelos dados reais
client_id = "1364577661162644"
client_secret = "bvV8CKao9RNJ6tim83J7Krr6DUaWRMpQ"
redirect_uri = "https://bot-precos.vercel.app/"
authorization_code = "TG-682671751067b80001b4c1c3-1038284917"

url = "https://api.mercadolibre.com/oauth/token"

payload = {
    "grant_type": "authorization_code",
    "client_id": client_id,
    "client_secret": client_secret,
    "code": authorization_code,
    "redirect_uri": redirect_uri
}

response = requests.post(url, data=payload)
print(response.status_code)
print(response.json())