from flask import Blueprint, render_template, request, redirect, url_for, flash
from web.modules.models import db, Users, Produto
from flask_login import login_required

admin_blueprint = Blueprint('admin', __name__, template_folder='templates/admin')

# =========== Rota principal do painel de administração =================
@admin_blueprint.route('/admin_dashboard')
@login_required
def admin_dashboard():
    users = Users.query.all()
    products = Produto.query.all()
    return render_template('admin/admin_dashboard.html', users=users, products=products)


# =========== Gerenciamento de produto =============
# Adicionar produto
@admin_blueprint.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form.get('image_url', '')

        new_product = Produto(name=name, description=description, price=price, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/product/add_product.html')

# Excluir produto
@admin_blueprint.route('/admin/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Produto.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

# Editar produto
@admin_blueprint.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Produto.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.image_url = request.form.get('image_url', '')

        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/product/edit_product.html', product=product)

# =================== Gerenciamento de usuario ==================

# Painel de usuarios
@admin_blueprint.route('/admin_user')
@login_required
def admin_user():
    users = Users.query.all()
    return render_template('admin/admin.html',users=users)

# Adicionar usuário
@admin_blueprint.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = Users(username=username, email=email)
        new_user.set_password(password)  # Ajuste para hash da senha
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário adicionado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/user/add_user.html')

# Excluir usuário
@admin_blueprint.route('/admin/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

# Editar usuário
@admin_blueprint.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = Users.query.get_or_404(id)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form.get('password')

        # Atualizar os campos do usuário
        user.username = username
        user.email = email
        if password:  # Atualizar a senha somente se fornecida
            user.set_password(password)

        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/user/edit_user.html', user=user)