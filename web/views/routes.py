from flask import render_template, Blueprint, request, redirect

main_blueprint = Blueprint('main', __name__)
AFILIADO_TAG = 'ofertasflashh-20'


@main_blueprint.route('/')
def home():
    return render_template('index.html')

