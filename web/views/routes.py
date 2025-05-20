from flask import render_template, Blueprint
# from web.modules.aliexpress import buscar_detalhes_produto
import os
import json

main_blueprint = Blueprint('main', __name__)

# ================== Conteúdo Principal ==================

@main_blueprint.route('/')
def home():
    return render_template('main/index.html')


@main_blueprint.route("/ofertas")
def ofertas():
    caminho = os.path.join("data", "produtos.json")
    with open(caminho, "r", encoding="utf-8") as f:
        produtos = json.load(f)
    return render_template("main/post.html", produtos=produtos)


# ============= Páginas Institucionais ==============

@main_blueprint.route("/sobre")
def sobre():
    return render_template('institucional/sobre.html')

@main_blueprint.route("/privacidade")
def privacidade():
    return render_template("institucional/privacidade.html")

@main_blueprint.route("/contato")
def contato():
    return ("<h1>Página de Contato em construção</h1>"
            "<p>Em breve")

# ================== Tratamento de Erros ==================

@main_blueprint.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('erros/404.html'), 404

@main_blueprint.errorhandler(500)
def erro_interno(e):
    return render_template('erros/500.html'), 500