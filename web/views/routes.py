from flask import render_template, Blueprint, request, redirect

main_blueprint = Blueprint('main', __name__)
AFILIADO_TAG = 'ofertasflashh-20'


@main_blueprint.route('/')
def home():
    return render_template('index.html')


@main_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    termo = request.args.get("q", "")
    departamento = request.args.get("departamento", "")

    termo_formatado = termo.replace(" ", "+")
    url_amazon = f"https://www.amazon.com.br/s?k={termo_formatado}&i={departamento}&tag={AFILIADO_TAG}"

    return redirect(url_amazon)