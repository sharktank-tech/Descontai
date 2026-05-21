from locale import currency

from flask import (render_template,request,redirect,url_for,flash,)
from flask_login import (login_user,current_user,)
from sqlalchemy.exc import (IntegrityError,SQLAlchemyError,)
from sqlalchemy import or_
from werkzeug.security import (generate_password_hash,)
from web.modules.models import User
from web import db
import re
import logging
from flask import (render_template, Blueprint, flash, redirect, url_for, request, abort, Response )
from flask_login import login_user, logout_user, login_required
from config import Config
from web.modules.enviar_email import enviar_email
from web.modules.models import User, Categoria
from web.modules.shopee.v3 import info_produtos
import json

main_blueprint = Blueprint("main", __name__)

# === Logge
logger = logging.getLogger(__name__)

# === Define a localidade do Brasil


# === Helpers
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
def is_valid_email(email: str) -> bool:return bool(EMAIL_REGEX.match(email))

# ================== Conteúdo Principal ==================

@main_blueprint.route("/")
def home():
    return render_template("main/index.html")


@main_blueprint.route("/ofertas")
@main_blueprint.route("/ofertas/<string:marketplace>")
def ofertas(marketplace=None):
    try:
        resposta = info_produtos()

        parsed = json.loads(resposta) if isinstance(resposta, str) else resposta
        nodes = parsed.get("data", {}).get("productOfferV2", {}).get("nodes", []) or []

        produtos = []
        for n in nodes:
            try:
                price = float(n.get("price", 0) or 0)

            except Exception:
                price = 0.0

            produtos.append({
                "productName": n.get("productName") or "Produto",
                "imageUrl": n.get("imageUrl") or "https://via.placeholder.com/400",
                "price": price,
                "productLink": n.get("productLink") or "#",
                "offerLink": n.get("offerLink") or "#",
                "shopName": n.get("shopName") or "",
                "ratingStar": n.get("ratingStar") or 0,
                "sales": n.get("sales") or 0
            })

        return render_template(
            "main/ofertas-v2.html",
            produtos=produtos
        )

    except Exception as e:
        print("Erro ofertas:", e)
        abort(500)


# ================== Categorias =============
@main_blueprint.route("/categoria/<slug>")
def categoria(slug):

    categoria = Categoria.query.filter_by(
        slug=slug
    ).first()

    if not categoria:
        flash("Categoria não encontrada.", "warning")
        return redirect(url_for("main.ofertas"))

    produtos = info_produtos(slug)

    return render_template(
        "categoria.html",
        categoria=categoria,
        produtos=produtos
    )

# ================== Conta ==================

@main_blueprint.route("/conta")
@login_required
def conta():
    return render_template("conta/conta.html")


@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email", "").strip().lower())
        password = (request.form.get("password", "").strip())

        if not email or not password:
            flash("Preencha todos os campos.","danger")
            return redirect(url_for("main.login"))

        try:
            user = User.query.filter_by(email=email).first()

        except Exception as e:
            print(f"Erro ao buscar usuário:{e}")

            flash(f"Erro interno no servidor. === {e}","danger")
            return redirect(url_for("main.login"))

        if not user:
            flash("Credenciais inválidas.","danger")
            return redirect(url_for("main.login"))

        if not user.check_password(password):
            flash("Credenciais inválidas.","danger")

            return redirect(url_for("main.login"))

        login_user(user,remember="remember" in request.form)
        flash("Login realizado com sucesso!","success")
        return redirect(url_for("main.conta"))

    return render_template("conta/login.html")

# ================== Registro ==================

@main_blueprint.route("/register",methods=["GET", "POST"])

def register():
    if request.method == "POST":
        username = (request.form.get("username", "").strip())
        email = (request.form.get("email", "").strip().lower())
        password = request.form.get("password","")

        # Validação
        if not username or not email or not password:
            flash("Todos os campos são obrigatórios.","danger"
            )
            return redirect(
                url_for("main.register")
            )
        try:
            # Verifica usuário existente
            existing_user = User.query.filter((User.email == email) | (User.username == username)).first()

            if existing_user:
                flash(
                    "Usuário ou e-mail já cadastrado.",
                    "danger"
                )
                return redirect(url_for("main.register")
                )

            # Cria usuário
            new_user = User(
                username=username,
                email=email,
                is_admin=False
            )

            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            flash("Cadastro realizado com sucesso!","success")
            print("Cadastro realizado com sucesso")

            return redirect(url_for("main.login"))

        except IntegrityError as e:

            db.session.rollback()

            print("Erro IntegrityError:")

            print(e)

            flash(
                "Usuário ou e-mail já cadastrado.",
                "danger"
            )

            return redirect(
                url_for("main.register")
            )

        except Exception as e:
            db.session.rollback()
            print("❌ ERRO AO CRIAR USUÁRIO")
            print(e)
            flash(
                "Erro interno no servidor.",
                "danger"
            )
            return redirect(url_for("main.register"))

    return render_template(
        "conta/register.html"
    )

# ================== Google Login ==================





# ================== Logout ==================

@main_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for("main.login"))


# ================== Institucional ==================

@main_blueprint.route("/sobre")
def sobre():
    return render_template("institucional/sobre.html")


@main_blueprint.route("/privacidade")
def privacidade():
    return render_template("institucional/privacidade.html")


@main_blueprint.route("/termos")
def termos():
    return render_template("institucional/termos.html")


# ================== Contato ==================

@main_blueprint.route("/contato", methods=["GET", "POST"])
#@login_required
def contato():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        assunto = request.form.get("assunto")
        mensagem = request.form.get("mensagem")

        if not all([nome, email, assunto, mensagem]):
            flash("Preencha todos os campos.", "warning.ensure")
            return redirect(url_for("main.contato"))

        conteudo_assunto = f"""
        Nome: {nome}
        - Assunto: {assunto}
        """.strip()

        enviar_email(
            Config.EMAIL_DESTINE,
            conteudo_assunto,
            mensagem.strip()
        )

        flash("Mensagem enviada com sucesso!", "success")
        return redirect(url_for("main.sobre"))

    return render_template("institucional/contato.html")


# ================== Robots ==================

@main_blueprint.route("/robots.txt")
def robots():
    return Response(
        """User-agent: *\nDisallow: 
        /conta/\n
        /admin_dashboard/\n
        /admin_products/\n
        /admin/products/add/\n
        /admin/products/edit/<int:id>\n
        /admin/products/delete/<int:id>\n
        /admin/categorias/add/\n
        /admin/users/delete/<int:id>/""",
        mimetype="text/plain")

