import time, hashlib, requests, json

APPID = "18391030753"
SECRET = "EKGCXKTULYROOEV54Z55UHNDADFZMWZ3"
ENDPOINT = "https://open-api.affiliate.shopee.com.br/graphql"

# montando a query
payload_dict = {
    "query": """
      query {
        productOfferV2(listType:0, sortType:5, page:0, limit:15) {
          nodes {
            productName
            imageUrl
            price
            productLink
            offerLink
            shopId
            shopName
            ratingStar
            sales
          }
        }
      }
    """,
    "operationName": None,
    "variables": {}
}


def info_produtos():
    # converte para JSON *compacto* (sem espaços desnecessários)
    payload = json.dumps(payload_dict, separators=(',', ':'))

    timestamp = str(int(time.time()))  # em segundos

    string_to_sign = f"{APPID}{timestamp}{payload}{SECRET}"
    signature = hashlib.sha256(string_to_sign.encode('utf-8')).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={APPID}, Timestamp={timestamp}, Signature={signature}"
    }

    resp = requests.post(ENDPOINT, headers=headers, data=payload)
    print(f"======= status code: {resp.status_code} ========")
    ps = resp.text
    print(ps)
    return ps
