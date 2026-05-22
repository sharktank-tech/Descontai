from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from web.modules.is_admin import admin_required
from web.database import db
from web.modules.models import User
from web.modules.models import Categoria
import logging

# === login
logger = logging.getLogger(__name__)

admin_blueprint = Blueprint(
    "admin",
    __name__,
    template_folder="templates/admin")

# ==========================================
# DASHBOARD
# ==========================================
@admin_blueprint.route("/admin_dashboard")
@login_required
@admin_required
def admin_dashboard():
    try:
        users = User.query.all()
        categorias = Categoria.query.all()

        return render_template("admin/admin_dashboard.html",users=users,categories=categorias)

    except Exception as e:
        logger.exception("Erro no dashboard admin.")
        flash("Erro ao carregar dashboard.","danger")
        return redirect(url_for("main.index"))


# ==========================================
# CATEGORIAS
# ==========================================
@admin_blueprint.route("/admin/categorias")
@login_required
@admin_required
def manage_categories():
    try:
        categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
        return render_template("admin/product/categoria.html",categorias=categorias)

    except Exception as e:
        logger.exception("Erro ao carregar categorias." )
        flash("Erro ao carregar categorias.",
            "danger")

        return redirect(url_for("admin.admin_dashboard"))

# =============== ADICIONAR CATEGORIA ==============

@admin_blueprint.route("/admin/categorias/add",methods=["GET", "POST"])
@login_required
@admin_required
def add_category():
    if request.method == "GET":
        return render_template("admin/product/add_category.html")

    try:
        categoria = Categoria(
            nome=request.form["nome"],
            descricao=request.form.get("descricao",""),ativa=True)
        db.session.add(categoria)
        db.session.commit()
        flash("Categoria adicionada ""com sucesso!","success")

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception("Erro ao adicionar categoria.")
        flash( "Erro ao adicionar categoria.","danger")

    return redirect(
        url_for("admin.manage_categories"))

# ================= TOGGLE CATEGORIA =============
@admin_blueprint.route("/admin/categorias/toggle/<int:id>", methods=["POST"])
@login_required
@admin_required
def toggle_category(id):
    try:
        categoria = (Categoria.query.get_or_404(id))
        categoria.ativa = (not categoria.ativa)
        db.session.commit()
        flash("Status da categoria " "atualizado!","success")

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception("Erro ao atualizar categoria.")
        flash("Erro ao atualizar categoria.","danger")

    return redirect(url_for("admin.manage_categories"))


# ==========================================
# USUÁRIOS
# ==========================================
@admin_blueprint.route("/admin_user")
@login_required
@admin_required
def admin_user():
    try:
        users = User.query.order_by(User.id.desc()).all()
        return render_template("admin/user/admin_user.html",users=users)

    except Exception as e:
        logger.exception("Erro ao listar usuários.")
        flash("Erro ao carregar usuários.","danger")

        return redirect(url_for("admin.admin_dashboard"))

# ============ ADD USUARIO ==============
@admin_blueprint.route("/admin/users/add/<int:id>",methods=["POST"])
@login_required
@admin_required
def add_user(id):
    try:
        user = User.query.get_or_404(id)
        db.session.add(user)
        db.session.commit()
        flash("Usuário adicionado ""com sucesso!","success")

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception("Erro ao adicionar usuário.")
        flash("Erro ao adicionar usuário.","danger")

    return redirect(url_for("admin.admin_dashboard"))

# =========== DELETAR USUÁRIO ===============
@admin_blueprint.route("/admin/users/delete/<int:id>",methods=["POST"])
@login_required
@admin_required
def delete_user(id):
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash("Usuário excluído ""com sucesso!","success")

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception("Erro ao excluir usuário.")
        flash("Erro ao excluir usuário.","danger")

    return redirect(url_for("admin.admin_dashboard"))