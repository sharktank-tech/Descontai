from flask import render_template, Blueprint, flash, redirect, url_for, request, abort, Response
from flask_dance.contrib.google import  google
from web.modules.enviar_email import enviar_email
from web.modules.models import  Users, db
from sqlalchemy.exc import IntegrityError
from flask_login import  login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from config import Config
from web.modules.shopee.v3 import info_produtos
import json

main_blueprint = Blueprint('main', __name__)


# ================== Conteúdo Principal ==================

@main_blueprint.route('/')
def home():
    return render_template('main/index.html')

@main_blueprint.route("/ofertas")
@main_blueprint.route("/ofertas/<string:marketplace>")
#@login_required
#@admin_required
def ofertas(marketplace=None):
    try:
        resposta = info_produtos()  # retorna string JSON (ou dict)
        print("DEBUG: tipo de 'resposta' ->", type(resposta))

        # parse seguro para dict
        parsed = {}
        if isinstance(resposta, str):
            try:
                parsed = json.loads(resposta)
            except Exception as e:
                print("DEBUG: erro ao fazer json.loads(resposta):", e)
                parsed = {}
        elif isinstance(resposta, dict):
            parsed = resposta
        else:
            # tenta converter genérico para string/json
            try:
                parsed = json.loads(str(resposta))
            except Exception:
                parsed = {}

        # extrai nodes (fórmula padrão)
        nodes = parsed.get("data", {}).get("productOfferV2", {}).get("nodes", []) or []
        print("DEBUG: nodes tipo/len ->", type(nodes), len(nodes) if hasattr(nodes, "__len__") else "NA")

        # normaliza cada produto para facilitar o template
        produtos = []
        for n in nodes:
            # n pode ser dict; usar .get com fallback
            try:
                price_val = float(n.get("price", 0) or 0)
            except Exception:
                # se price vier em formato estranho
                try:
                    price_val = float(str(n.get("price", "0")).replace(",", "."))
                except Exception:
                    price_val = 0.0

            produtos.append({
                "productName": n.get("productName") or n.get("name") or "Produto sem nome",
                "imageUrl": n.get("imageUrl") or n.get("image") or "https://via.placeholder.com/400x400?text=Sem+imagem",
                "price": price_val,
                "productLink": n.get("productLink") or "#",
                "offerLink": n.get("offerLink") or n.get("affiliateLink") or "#",
                "shopName": n.get("shopName") or n.get("shopId") or "",
                "ratingStar": n.get("ratingStar") or 0,
                "sales": n.get("sales") or 0
            })

        print(f"DEBUG: total de produtos normalizados: {len(produtos)}")

        return render_template(
            "main/ofertas2.html",
            produtos=produtos,
            marketplace_selecionado=marketplace
        )

    except Exception as e:
        print(f"Erro ao carregar ofertas: {e}")
        abort(500)

# ============== Área de Conta ==================
@main_blueprint.route('/conta')
@login_required
def conta():
    """
    Rota principal da conta - Exibe dashboard com informações do usuário
    """
    try:

        return render_template('conta/conta.html')

    except Exception as e:
        flash(f"Erro ao carregar sua conta. Por favor, tente novamente.\nErro {e}", "danger")
        return redirect(url_for('main.home'))

# ================== Login local ==================

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash("Por favor, preencha todos os campos.", "danger")
            return redirect(url_for('main.login'))

        user = Users.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Credenciais inválidas. Tente novamente.", "danger")
            return redirect(url_for('main.login'))

        remember = 'remember' in request.form
        login_user(user, remember=remember)
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for('main.conta', marketplace='amazon'))

    return render_template('conta/login.html')

# ================== Login com Google ==================

@main_blueprint.route("/login/google")
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    return redirect(url_for("main.login_google_finish"))

@main_blueprint.route("/login/google/finish")
def login_google_finish():
    if not google.authorized:
        flash("Erro ao autenticar com Google", "danger")
        return redirect(url_for("main.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Erro ao obter dados do Google", "danger")
        return redirect(url_for("main.login"))

    user_info = resp.json()
    email = user_info.get("email")
    username = user_info.get("name", email.split('@')[0])

    user = Users.query.filter_by(email=email).first()
    if not user:
        user = Users(username=username, email=email, is_admin=False)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Erro ao criar conta com Google.", "danger")
            return redirect(url_for("main.login"))

    login_user(user)
    flash(f"Bem-vindo, {username}!", "success")
    return redirect(url_for("main.ofertas", marketplace='amazon'))

# ================== Logout ==================

@main_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for('main.login'))

# ================== Registro ==================

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash("Todos os campos são obrigatórios.", "danger")
            return redirect(url_for('main.register'))

        existing_user = Users.query.filter((Users.username==username)|(Users.email==email)).first()
        if existing_user:
            flash("Usuário ou e-mail já existe.", "danger")
            return redirect(url_for('main.register'))

        try:
            new_user = Users(username=username, email=email, is_admin=False)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Cadastro realizado com sucesso! Faça login para continuar.", "success")
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao salvar usuário: {str(e)}", "danger")

    return render_template('conta/register.html')


# ============= Páginas Institucionais ==============

@main_blueprint.route("/sobre")
def sobre():
    return render_template('institucional/sobre.html')

@main_blueprint.route("/privacidade")
def privacidade():
    return render_template("institucional/privacidade.html")

# Página dos termos de uso
@main_blueprint.route("/termos")
def termos():
    return render_template("institucional/termos.html")

# Enviar email de contato
@main_blueprint.route('/contato', methods=['GET', 'POST'])
@login_required
def contato():
    try:
        if request.method == 'POST':
            nome = request.form.get('nome')
            email_usuario = request.form.get('email')
            assunto = request.form.get('assunto')
            mensagem = request.form.get('mensagem')

            if not all([nome, email_usuario, assunto, mensagem]):
                flash("Por favor, preencha todos os campos.", "warning")
                return redirect(url_for('main.contato'))

            destinatario = Config.EMAIL_DESTINE
            if not destinatario:
                flash("E-mail do usuário não encontrado.", "danger")
                return redirect(url_for('main.home'))

            assunto_email = f"Contato de {nome}: {assunto}"

            corpo_email = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #333333; text-align: center; margin-bottom: 20px;">📩 Nova Mensagem de Contato</h2>

                        <p><strong style="color: #555;">Nome:</strong> {nome}</p>
                        <p><strong style="color: #555;">E-mail:</strong> {email_usuario}</p>
                        <p><strong style="color: #555;">Assunto:</strong> {assunto}</p>
                        <p><strong style="color: #555;">Mensagem:</strong></p>
                        <p style="background-color: #f1f1f1; padding: 15px; border-radius: 5px;">{mensagem}</p>

                        <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                        <p style="font-size: 12px; color: #999999; text-align: center;">Esta mensagem foi enviada através do formulário de contato do site.</p>
                    </div>
                </body>
            </html>
            """

            # Enviar o e-mail
            enviar_email(destinatario, assunto_email, corpo_email)
            flash("Mensagem enviada com sucesso!", "success")
            return redirect(url_for('main.sobre'))

        # Se for GET, apenas renderiza a página normalmente
        return render_template('institucional/contato.html')

    except Exception as e:
        flash(f"Erro ao enviar mensagem: {str(e)}", "danger")
        print(f"Erro ao enviar e-mail: {e}")
        return redirect(url_for('main.sobre'))

@main_blueprint.route('/robots.txt')
def robots():
    content = """User-agent: *
Disallow: /termos/
Disallow: /privacidade/
Disallow: /password/redefine
Disallow: /contato/
Disallow: /conta/
    
    """
    return Response(content, mimetype='text/plain')


# ================== Tratamento de Erros ==================

@main_blueprint.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('erros/404.html'), 404

@main_blueprint.errorhandler(500)
def erro_interno(e):
    return render_template('erros/500.html'), 500