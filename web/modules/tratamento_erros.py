class HTTPErrorHandler:
    def __init__(self):
        self.errors = {
            # 1xx - Informational
            100: "Continue enviando a requisição.",
            101: "Mudança de protocolo aceita.",
            102: "Processando requisição.",
            103: "Pré-carregamento iniciado.",

            # 2xx - Sucesso
            200: "Requisição realizada com sucesso.",
            201: "Recurso criado com sucesso.",
            202: "Requisição recebida e será processada.",
            203: "Informações retornadas podem não ser do servidor original.",
            204: "Sem conteúdo para retornar.",
            205: "Reinicie o formulário.",
            206: "Conteúdo parcial retornado.",
            207: "Múltiplos status retornados.",
            208: "Recurso já reportado.",
            226: "Resposta processada com sucesso (IM Used).",

            # 3xx - Redirecionamento
            300: "Múltiplas opções disponíveis.",
            301: "Recurso movido permanentemente.",
            302: "Recurso movido temporariamente.",
            303: "Veja outro recurso.",
            304: "Recurso não modificado.",
            305: "Uso de proxy requerido (obsoleto).",
            306: "Código reservado.",
            307: "Redirecionamento temporário.",
            308: "Redirecionamento permanente.",

            # 4xx - Erro do cliente
            400: "Requisição inválida.",
            401: "Autenticação necessária.",
            402: "Pagamento necessário.",
            403: "Acesso proibido.",
            404: "Recurso não encontrado.",
            405: "Método não permitido.",
            406: "Formato não aceito.",
            407: "Autenticação de proxy necessária.",
            408: "Tempo de requisição esgotado.",
            409: "Conflito na requisição.",
            410: "Recurso removido permanentemente.",
            411: "Tamanho da requisição não especificado.",
            412: "Pré-condição falhou.",
            413: "Conteúdo muito grande.",
            414: "URI muito longa.",
            415: "Tipo de mídia não suportado.",
            416: "Intervalo inválido.",
            417: "Expectativa falhou.",
            418: "Sou um bule de chá ☕ (erro experimental).",
            421: "Requisição direcionada ao servidor errado.",
            422: "Erro semântico na requisição.",
            423: "Recurso bloqueado.",
            424: "Falha devido a dependência anterior.",
            425: "Requisição muito cedo.",
            426: "Atualização de protocolo necessária.",
            428: "Pré-condição obrigatória.",
            429: "Muitas requisições (limite atingido).",
            431: "Cabeçalhos muito grandes.",
            451: "Indisponível por razões legais.",

            # 5xx - Erro do servidor
            500: "Erro interno no servidor.",
            501: "Funcionalidade não implementada.",
            502: "Resposta inválida de outro servidor.",
            503: "Serviço indisponível.",
            504: "Tempo de resposta do servidor excedido.",
            505: "Versão HTTP não suportada.",
            506: "Erro de negociação interna.",
            507: "Armazenamento insuficiente.",
            508: "Loop infinito detectado.",
            510: "Extensão não suportada.",
            511: "Autenticação de rede necessária."
        }

    def get_message(self, status_code: int) -> str:
        """
        Retorna a mensagem personalizada baseada no código HTTP.
        """
        return self.errors.get(status_code, "Erro HTTP desconhecido.")

    def build_response(self, status_code: int, extra: dict = None) -> dict:
        """
        Retorna um dicionário padrão para respostas da API.
        """
        response = {
            "status": status_code,
            "message": self.get_message(status_code)
        }

        if extra:
            response["data"] = extra

        return response