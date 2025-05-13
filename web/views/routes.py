from flask import render_template, Blueprint

main_blueprint = Blueprint('main', __name__)
AFILIADO_TAG = 'ofertasflashh-20'

# ================== Conteúdo Principal ==================

@main_blueprint.route('/')
def home():
    return render_template('main/index.html')

@main_blueprint.route('/post')
def post():
    produtos = [
        {
            "nome": "Fone Bluetooth XYZ",
            "imagem": "https://m.media-amazon.com/images/I/519bjoeFBTL.__AC_SX300_SY300_QL70_ML2_.jpg",
            "preco_original": 199.90,
            "preco_desconto": 99.90,
            "desconto": 50,
            "link_base": "https://a.co/d/7vTrsic"
        },
        {
            "nome": "Relógio Smart ABC",
            "imagem": "https://m.media-amazon.com/images/I/61G-6e9mRwL.__AC_SX300_SY300_QL70_ML2_.jpg",
            "preco_original": 299.90,
            "preco_desconto": 179.90,
            "desconto": 40,
            "link_base": "https://www.amazon.com.br/dp/B0D4HV9Z3L"
        }
    ]

    # Geração do link com tag de afiliado
    for produto in produtos:
        produto['link_afiliado'] = f"{produto['link_base']}?tag={AFILIADO_TAG}"
        del produto['link_base']

    return render_template('main/post.html', produtos=produtos)

# ============= Institucional ==============

@main_blueprint.route("/contato")
def contato():
    return ("<h1>Página de Contato em construção</h1>"
            "<p>Em breve")


@main_blueprint.route('/sobre')
def sobre():
    return render_template('main/sobre.html')

# ================== Tratamento de Erros ==================

@main_blueprint.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('erros/404.html'), 404

@main_blueprint.errorhandler(500)
def erro_interno(e):
    return render_template('erros/500.html'), 500