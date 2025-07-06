from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager
import os
from dotenv import load_dotenv
load_dotenv()


# = Instância global do banco =
db = SQLAlchemy()
login_manager = LoginManager()

# ======== Função de criação do app =================
def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Carregar configurações do config.py
    app.config.from_object(Config)

    # Permitir OAuth inseguro em ambiente de desenvolvimento
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Remova em produção

    # Blueprint do Google OAuth
    google_bp = make_google_blueprint(
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        redirect_to="main.login_google_finish",  # agora aponta para login_google_finish
        scope=["profile", "email"]
    )

    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # Registrar Blueprints
    from web.views.routes import main_blueprint
    from web.views.admin_routes import admin_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(google_bp, url_prefix="/login")

    # Carregar o usuário do banco
    from web.modules.models import Users

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return Users.query.get(int(user_id))
        except (ValueError, TypeError):
            return None

    # Tratamento de erros
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('erros/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('erros/500.html'), 500

    return app

# Função para envio de e-mails
def enviar_email(destinatario, assunto, corpo):
    servidor_smtp = Config.SERVIDOR
    porta_smtp = Config.PORTA_SMPT
    remetente = Config.REMETENTE
    senha = Config.PASWD

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'html'))

    try:
        with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
            server.starttls()
            server.login(remetente, senha)
            server.send_message(msg)
            print(f"E-mail enviado para {destinatario} com sucesso!")
    except Exception as e:
        raise RuntimeError(f"Erro ao enviar e-mail: {e}")