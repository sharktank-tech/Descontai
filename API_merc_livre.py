import requests
import json

# Carrega o token de acesso atualizado
with open('web/modules/mercado_livre/tokens/tokens.json') as f:
    tokens = json.load(f)

headers = {
    'Authorization': f"Bearer {tokens['access_token']}"
}

# Exemplo: Busca de produtos da categoria 'celulares' com ordenação por maior desconto
# Você pode trocar 'MLB1055' (categoria de celulares) por outras categorias
url = 'https://api.mercadolibre.com/sites/MLB/search?category=MLB1055&sort=discount_percentage_desc&limit=10'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    for item in data.get('results', []):
        print({
            'nome': item['title'],
            'preco_original': item.get('original_price'),
            'preco_atual': item['price'],
            'desconto': round((1 - item['price'] / item['original_price']) * 100, 2) if item.get('original_price') else 0,
            'link': item['permalink'],
            'imagem': item['thumbnail']
        })
else:
    print(f"Erro: {response.status_code}")
    print(response.json())