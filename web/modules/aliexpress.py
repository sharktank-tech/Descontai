import requests


def buscar_detalhes_produto(item_id):
    url = "https://aliexpress-datahub.p.rapidapi.com/item_detail_2"
    querystring = {"itemId": item_id}

    headers = {
        "X-RapidAPI-Key": "5f1edfd8e9mshfb6d81a2b537baep1cb965jsn3d5d162397f7",  # Troque pela sua chave se necessário
        "X-RapidAPI-Host": "aliexpress-datahub.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        item = data.get("data", {})
        if not item:
            return None

        preco_original = item.get("target_sale_price", {}).get("price", 0)
        preco_promocional = item.get("sale_price", {}).get("price", preco_original)

        # Cálculo do desconto
        try:
            preco_original_float = float(preco_original)
            preco_promocional_float = float(preco_promocional)
            desconto = round(((preco_original_float - preco_promocional_float) / preco_original_float) * 100)
        except:
            desconto = 0

        return {
            "name": item.get("title", "Sem nome"),
            "image": item.get("image", ""),
            "originalPrice": preco_original,
            "salePrice": preco_promocional,
            "discount": desconto,
            "detailUrl": item.get("detail_url", "#")
        }
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None


# Exemplo de chamada para testar
if __name__ == "__main__":
    produto = buscar_detalhes_produto("1005005244562338")
    if produto:
        from pprint import pprint

        pprint(produto)
    else:
        print("Produto não encontrado ou erro na API.")