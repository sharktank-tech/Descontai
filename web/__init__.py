from flask import Flask, render_template
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_caching import Cache
from web.database import db
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import Config

# ========== Carregar variáveis de ambiente ==================
load_dotenv()
cache = Cache()

# ========== Instâncias globais ============
login_manager = LoginManager()

# =========== Função de criação do app =============
def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates"
    )

    # Carregar configurações
    app.config.from_object(Config)

    # Carregar o objeto de banco de dados
    db.init_app(app)

    # ======== Iniciar Cache =============
    cache.init_app(app, config={
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": 300
    })


    # ========== Inicializar extensões ==========
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "info"

    # ======== Registrar blueprints ==========
    from web.views.routes import main_blueprint
    from web.views.admin_routes import admin_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)


    # ======== Loader de usuário ==========
    from web.modules.models import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(
                int(user_id))
        except Exception:
            return None

    # ======== Tratamento de erros ==========
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("erros/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("erros/500.html"), 500

    return app


# =========== Função para envio de e-mails ===============
def enviar_email(destinatario, assunto, corpo):
    servidor_smtp = Config.EMAIL_SERVER
    porta_smtp = Config.EMAIL_PORT
    remetente = Config.EMAIL_SENDER
    senha = Config.EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "html"))

    try:
        with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
            server.starttls()
            server.login(remetente, senha)
            server.send_message(msg)
            print(f"E-mail enviado para {destinatario} com sucesso!")
    except Exception as e:
        raise RuntimeError(f"Erro ao enviar e-mail: {e}")
