from flask import (render_template, Blueprint, flash, redirect, url_for, request, abort, Response )
from werkzeug.security import generate_password_hash
from flask_dance.contrib.google import google
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from config import Config
from web.modules.enviar_email import enviar_email
from web.modules.models import User
from web.modules.shopee.v3 import info_produtos
import requests
import json

main_blueprint = Blueprint("main", __name__)

SUPABASE_HEADERS = {
    "apikey": Config.SUPABASE_KEY,
    "Authorization": f"Bearer {Config.SUPABASE_SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
}

SUPABASE_USERS_URL = f"{Config.SUPABASE_URL}/rest/v1/users"


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
            "main/ofertas2.html",
            produtos=produtos,
            marketplace_selecionado=marketplace
        )

    except Exception as e:
        print("Erro ofertas:", e)
        abort(500)


# ================== Conta ==================

@main_blueprint.route("/conta")
@login_required
def conta():
    return render_template("conta/conta.html")


# ================== Login Local ==================

@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("main.login"))

        r = requests.get(
            SUPABASE_USERS_URL,
            headers=SUPABASE_HEADERS,
            params={
                "email": f"eq.{email}",
                "select": "id,username,email,password_hash,is_admin"}
        )

        if r.status_code != 200:
            flash("Erro no servidor. Tente novamente.", "danger")
            print(r.text)
            return redirect(url_for("main.login"))

        data = r.json()[0]
        user = User.from_dict(data)

        if not user.check_password(password):
            flash("Credenciais inválidas.", "danger")
            return redirect(url_for("main.login"))

        login_user(user, remember="remember" in request.form)
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("main.conta"))

    return render_template("conta/login.html")


# ================== Registro ==================

@main_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")

        if not username or not email or not password:
            flash("Todos os campos são obrigatórios.", "danger")
            return redirect(url_for("main.register"))

        password_hash = generate_password_hash(password)

        payload = {
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "is_admin": False
        }

        r = requests.post(
            SUPABASE_USERS_URL,
            headers=SUPABASE_HEADERS,
            json=payload
        )

        # Verifica de o usuário está cadastrado
        if r.status_code == 409:
            flash("Usuário ou e-mail já cadastrado.", "danger")
            print(f"Erro: {r.status_code}", "\nUsuário ou e-mail já cadastrado.", "danger")
            return redirect(url_for("main.register"))


        # Tratamento de erro de indisponibidade
        if r.status_code == 503:
            flash("Servidor indisponível. Tente novamente.", "warning")

            # Tenta extrair erro detalhado da API
            try:
                error_data = r.json()
                api_error = (
                        error_data.get("message")
                        or error_data.get("error")
                        or error_data.get("details")
                        or str(error_data)
                )
            except ValueError:
                api_error = r.text  # Resposta não é JSON

            # Mensagem para o usuário
            flash(error_data, "danger")

            # Log detalhado para debug
            print("❌ ERRO AO CRIAR USUÁRIO")
            print(f"Status Code: {r.status_code}")
            print(f"URL: {r.url}")
            print(f"Payload enviado: {payload}")
            print(f"Resposta da API: {api_error}")
            print("-" * 50)

            return redirect(url_for("main.register"))

        flash("Cadastro realizado com sucesso!", "success")
        print("Cadastro realizado com sucesso")
        return redirect(url_for("main.login"))

    return render_template("conta/register.html")
# ================== Google Login ==================

@main_blueprint.route("/login/google")
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    return redirect(url_for("main.login_google_finish"))


@main_blueprint.route("/login/google/finish")
def login_google_finish():
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Erro ao autenticar com Google.", "danger")
        return redirect(url_for("main.login"))

    info = resp.json()
    email = info.get("email")
    username = info.get("name", email.split("@")[0])

    r = requests.get(
        SUPABASE_USERS_URL,
        headers=SUPABASE_HEADERS,
        params={"email": f"eq.{email}", "select": "*"}
    )

    if r.json():
        user = User.from_dict(r.json()[0])
    else:
        payload = {
            "username": username,
            "email": email,
            "is_admin": False
        }
        created = requests.post(
            SUPABASE_USERS_URL,
            headers=SUPABASE_HEADERS,
            json=payload
        )
        user = User.from_dict(created.json()[0])

    login_user(user)
    flash(f"Bem-vindo, {username}!", "success")
    return redirect(url_for("main.conta"))


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

        enviar_email(
            Config.EMAIL_DESTINE,
            f"Contato: {assunto}",
            mensagem
        )

        flash("Mensagem enviada com sucesso!", "success")
        return redirect(url_for("main.sobre"))

    return render_template("institucional/contato.html")


# ================== Robots ==================

@main_blueprint.route("/robots.txt")
def robots():
    return Response(
        "User-agent: *\nDisallow: /conta/\n",
        mimetype="text/plain")
