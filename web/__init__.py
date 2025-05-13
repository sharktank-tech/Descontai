from flask import Flask, render_template

# Iniciar extensões (ex: db = SQLAlchemy(), login_manager = LoginManager()...)

# Instância do app
def create_app():
    app = Flask(__name__)

    # Carregar configurações
    # app.config.from_object('config.Config')

    # Registrar blueprints
    from web.views.routes import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    # Inicializar extensões
    # db.init_app(app)
    # login_manager.init_app(app)

    # Tratadores de erro
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('erros/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('erros/500.html'), 500

    return app