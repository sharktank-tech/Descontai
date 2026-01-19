from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from web.modules.is_admin import admin_required
from web.modules.supabase_client import (
    supabase_get, supabase_post, supabase_patch, supabase_delete
)

admin_blueprint = Blueprint(
    'admin', __name__, template_folder='templates/admin'
)

# ================= DASHBOARD =================
@admin_blueprint.route('/admin_dashboard')
@login_required
@admin_required
def admin_dashboard():
    users = supabase_get("users").json()
    produtos = supabase_get("produtos").json()
    categorias = supabase_get("categorias").json()

    return render_template(
        'admin/admin_dashboard.html',
        users=users,
        products=produtos,
        categories=categorias
    )


# ================= PRODUTOS =================
@admin_blueprint.route('/admin_products')
@login_required
@admin_required
def admin_products():
    search = request.args.get('q')

    params = {
        "select": "*,categorias(nome)"
    }

    if search:
        params["or"] = (
            f"name.ilike.*{search}*,"
            f"origem.ilike.*{search}*"
        )

    products = supabase_get("produtos", params).json()

    return render_template(
        'admin/product/admin_product.html',
        products=products
    )


@admin_blueprint.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    categorias = supabase_get(
        "categorias", {"ativa": "eq.true"}
    ).json()

    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "image": request.form['image'],
            "originalprice": float(request.form['originalprice']),
            "saleprice": float(request.form['saleprice']),
            "discount": float(request.form['discount']),
            "detailurl": request.form['detailurl'],
            "rating": float(request.form.get('rating', 4.5)),
            "vendidos": request.form.get('vendidos', '1k+'),
            "categoria_id": int(request.form['categoria_id'])
        }

        supabase_post("produtos", data)
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('admin.admin_products'))

    return render_template(
        'admin/product/add_product.html',
        categories=categorias
    )


@admin_blueprint.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = supabase_get("produtos", {"id": f"eq.{id}"}).json()[0]
    categorias = supabase_get("categorias").json()

    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "image": request.form['image'],
            "originalprice": float(request.form['originalprice']),
            "saleprice": float(request.form['saleprice']),
            "discount": float(request.form['discount']),
            "detailurl": request.form['detailurl'],
            "rating": float(request.form.get('rating', 4.5)),
            "vendidos": request.form.get('vendidos', '1k+'),
            "categoria_id": int(request.form['categoria_id'])
        }

        supabase_patch("produtos", id, data)
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template(
        'admin/product/edit_product.html',
        product=product,
        categories=categorias
    )


@admin_blueprint.route('/admin/products/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_product(id):
    supabase_delete("produtos", id)
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('admin.admin_dashboard'))


# ================= CATEGORIAS =================
@admin_blueprint.route('/admin/categorias')
@login_required
@admin_required
def manage_categories():
    categorias = supabase_get("categorias").json()
    return render_template(
        'admin/product/categorias.html',
        categorias=categorias
    )


@admin_blueprint.route('/admin/categorias/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    if request.method == 'POST':
        data = {
            "nome": request.form['nome'],
            "descricao": request.form.get('descricao', ''),
            "ativa": True
        }
        supabase_post("categorias", data)
        flash('Categoria adicionada com sucesso!', 'success')
        return redirect(url_for('admin.manage_categories'))

    return render_template('admin/product/add_category.html')


@admin_blueprint.route('/admin/categorias/toggle/<int:id>', methods=['POST'])
@login_required
@admin_required
def toggle_category(id):
    categoria = supabase_get(
        "categorias", {"id": f"eq.{id}"}
    ).json()[0]

    supabase_patch(
        "categorias",
        id,
        {"ativa": not categoria["ativa"]}
    )

    flash('Status da categoria atualizado!', 'success')
    return redirect(url_for('admin.manage_categories'))


# ================= USUÁRIOS =================
@admin_blueprint.route('/admin_user')
@login_required
@admin_required
def admin_user():
    users = supabase_get("users").json()
    return render_template(
        'admin/user/admin_user.html',
        users=users
    )


@admin_blueprint.route('/admin/users/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    supabase_delete("users", id)
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('admin.admin_dashboard'))