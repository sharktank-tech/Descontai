from flask import Flask

# Iniciar as extensôes

# Instancia do app
def create_app():
    app = Flask(__name__)

    # Carregar as configurações

    # Registrar as blueprints
    from web.views.routes import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    # Inicializar as extenssôes

    return app