# API de afiliados Shopee
A Shopee oferece um **Open API para afiliados**, com o qual você pode:

1. **Gerar deep links** automaticamente
2. Puxar listas de ofertas (produtos, comissões, preços)
3. Obter relatórios de conversões

---

## ✅ Como acessar a API

### 1. Receber credenciais

* Vá ao painel de afiliado da Shopee (país específico, ex. br, ph, my)
* Clique no item **“Open API”** ou similar (ex: "API aberta") e obtenha seu **App ID** e **Secret Key** ([youtube.com][1], [youtube.com][2])

### 2. Autenticação (criação de assinatura)

Cada requisição exige um cabeçalho `Authorization` com:

```
SHA256 Credential={AppID},Timestamp={timestamp},Signature={assinatura}
```

* `timestamp`: Epoch em segundos
* `assinatura`: SHA‑256 de (AppID + Timestamp + PayloadJSON + Secret)&#x20;

Um programador no StackOverflow confirmou que essa estrutura — concatenar os quatro elementos — funciona corretamente .

### 3. Exemplos de uso

* **GraphQL** para obter ofertas:

  ```python
  payload = '{"query": "...", "variables": {...}}'
  factor = f'{appID}{timestamp}{payload}{secret}'
  signature = sha256(factor).hexdigest()
  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'SHA256 Credential={appID},Timestamp={timestamp},Signature={signature}'
  }
  response = requests.post(API_URL, data=payload, headers=headers)
  ```
* **Rest/Playground**: alguns países têm páginas interativas (como Brasil) para testar endpoints como geração de short link, lista de ofertas e relatórios ([youtube.com][3]).

---

## 📌 Pontos importantes

| Item           | Dica                                                                                                             |
| -------------- | ---------------------------------------------------------------------------------------------------------------- |
| Trailing zeros | Certifique-se de que o JSON do `payload` não tenha espaçamentos ou quebras de linha extras — isso muda o hash.   |
| Timestamp      | Use sempre valores UNIX inteiros atualizados no momento.                                                         |
| Ambientes      | A URL base varia de país para país (ex: `.br`, `.ph`). Verifique o domínio correto no seu painel.                |
| Testes         | Use o **Playground oficial** (disponível para o Brasil) ou admire o vídeo acima para ver o passo a passo visual. |

---

## 📚 Recursos úteis

* Vídeo com passo a passo de habilitação da API no painel Shopee — desde obtenção das chaves até chamadas funcionais&#x20;
* Playgrounds/API docs no Brasil com endpoints comuns de link e relatórios&#x20;

---

### ✔ Recomendações

Se quiser, posso te ajudar a:

* configurar a assinatura (signature) em Python, Node.js, ou outra linguagem
* montar chamadas para gerar vários links ou pegar ofertas específicas
* validar respostas e tratar erros de autenticação

É só dizer de que forma você pretende usar a API e a gente monta juntos!

[1]: https://www.youtube.com/watch?pp=0gcJCfwAo7VqN5tD&v=dgh8YxjZKXw&utm_source=chatgpt.com "Como Solicitar API da Shopee para Vender MAIS com o Divulgador ..."
[2]: https://www.youtube.com/watch?v=0YkiOsmgqSg&utm_source=chatgpt.com "Como gerar links de afiliado pelo app mercado livre (novidade ..."
[3]: https://www.youtube.com/watch?v=vw9WciQUIxY&utm_source=chatgpt.com "(Atualizado!) Como Gerar Promoções Shopee no Divulgador ..."
