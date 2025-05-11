from flask import render_template, Blueprint, url_for

main_blueprint = Blueprint('main', __name__)
AFILIADO_TAG = 'ofertasflashh-20'


@main_blueprint.route('/')
def home():
    return render_template('index.html')

