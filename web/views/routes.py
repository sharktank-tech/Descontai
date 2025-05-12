from flask import render_template, Blueprint, url_for

main_blueprint = Blueprint('main', __name__)
AFILIADO_TAG = 'ofertasflashh-20'


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
            "link_base": "https://a.co/d/7vTrsic"  # Link sem a tag de afiliado
        },
        {
            "nome": "Relógio Smart ABC",
            "imagem": "https://m.media-amazon.com/images/I/61G-6e9mRwL.__AC_SX300_SY300_QL70_ML2_.jpg",
            "preco_original": 299.90,
            "preco_desconto": 179.90,
            "desconto": 40,
            "link_base": "https://www.amazon.com.br/dp/EXEMPLO2"  # Link sem a tag de afiliado
        }
    ]

    # Adiciona a tag de afiliado a cada link
    for produto in produtos:
        produto['link_afiliado'] = produto['link_base'] + "?tag=ofertasflashh-20"
        del produto['link_base']  # Opcional: removendo o link base para não expô-lo no template

    return render_template('main/post.html', produtos=produtos)


@main_blueprint.route('/sobre')
def sobre():
    return render_template('main/sobre.html')