from flask import Blueprint, render_template, request, redirect, url_for, flash
from web.modules.models import db, Users, Produto, Categoria
from flask_login import login_required

admin_blueprint = Blueprint('admin', __name__, template_folder='templates/admin')


# =========== Rota principal do painel de administração =================
@admin_blueprint.route('/admin_dashboard')
@login_required
def admin_dashboard():
    users = Users.query.all()
    produtos = Produto.query.all()
    categorias = Categoria.query.all()
    return render_template('admin/admin_dashboard.html',
                           users=users,
                           products=produtos,
                           categories=categorias)


# =========== Gerenciamento de produto =============
@admin_blueprint.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    categorias = Categoria.query.filter_by(ativa=True).all()

    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        originalprice = float(request.form['originalprice'])
        saleprice = float(request.form['saleprice'])
        discount = float(request.form['discount'])
        detailurl = request.form['detailurl']
        rating = float(request.form.get('rating', 4.5))
        vendidos = request.form.get('vendidos', '1k+')
        categoria_id = int(request.form['categoria_id'])

        new_product = Produto(
            name=name,
            image=image,
            originalprice=originalprice,
            saleprice=saleprice,
            discount=discount,
            detailurl=detailurl,
            rating=rating,
            vendidos=vendidos,
            categoria_id=categoria_id
        )

        db.session.add(new_product)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/product/add_product.html', categories=categorias)


@admin_blueprint.route('/admin/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Produto.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('admin.admin_dashboard'))


@admin_blueprint.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Produto.query.get_or_404(id)
    categorias = Categoria.query.filter_by(ativa=True).all()

    if request.method == 'POST':
        product.name = request.form['name']
        product.image = request.form['image']
        product.originalprice = float(request.form['originalprice'])
        product.saleprice = float(request.form['saleprice'])
        product.discount = float(request.form['discount'])
        product.detailurl = request.form['detailurl']
        product.rating = float(request.form.get('rating', 4.5))
        product.vendidos = request.form.get('vendidos', '1k+')
        product.categoria_id = int(request.form['categoria_id'])

        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/product/edit_product.html',
                           product=product,
                           categories=categorias)


# =========== Gerenciamento de Categorias =============
@admin_blueprint.route('/admin/categorias')
@login_required
def manage_categories():
    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template('admin/product/categorias.html', categorias=categorias)


@admin_blueprint.route('/admin/categorias/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        descricao = request.form.get('descricao', '').strip()

        if not nome:
            flash('O nome da categoria não pode estar vazio!', 'error')
        else:
            try:
                nova_categoria = Categoria(nome=nome, descricao=descricao)
                db.session.add(nova_categoria)
                db.session.commit()
                flash('Categoria adicionada com sucesso!', 'success')
                return redirect(url_for('admin.manage_categories'))
            except:
                db.session.rollback()
                flash('Erro ao adicionar categoria. Nome já existe.', 'error')

    return render_template('admin/product/add_category.html')


@admin_blueprint.route('/admin/categorias/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':
        categoria.nome = request.form['nome']
        categoria.descricao = request.form.get('descricao', '')
        categoria.ativa = 'ativa' in request.form

        try:
            db.session.commit()
            flash('Categoria atualizada com sucesso!', 'success')
            return redirect(url_for('admin.manage_categories'))
        except:
            db.session.rollback()
            flash('Erro ao atualizar categoria. Nome já existe.', 'error')

    return render_template('admin/product/edit_category.html', categoria=categoria)


@admin_blueprint.route('/admin/categorias/delete/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    categoria = Categoria.query.get_or_404(id)
    categoria_padrao = Categoria.query.filter_by(nome='Ofertas').first()

    try:
        # Atualizar produtos para categoria padrão
        Produto.query.filter_by(categoria_id=id).update({'categoria_id': categoria_padrao.id})

        db.session.delete(categoria)
        db.session.commit()
        flash('Categoria removida com sucesso! Produtos movidos para categoria padrão.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao remover categoria: {str(e)}', 'error')

    return redirect(url_for('admin.manage_categories'))


@admin_blueprint.route('/admin/categorias/toggle/<int:id>', methods=['POST'])
@login_required
def toggle_category(id):
    categoria = Categoria.query.get_or_404(id)
    categoria.ativa = not categoria.ativa
    db.session.commit()

    status = "ativada" if categoria.ativa else "desativada"
    flash(f'Categoria {status} com sucesso!', 'success')
    return redirect(url_for('admin.manage_categories'))


# =========== Configurações =============
@admin_blueprint.route('/admin/configuracoes')
@login_required
def admin_settings():
    return render_template('admin/product/config.html')


# =================== Gerenciamento de usuario ==================
@admin_blueprint.route('/admin_user')
@login_required
def admin_user():
    users = Users.query.all()
    return render_template('admin/admin_user.html', users=users)


@admin_blueprint.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_admin = 'is_admin' in request.form

        new_user = Users(username=username, email=email, is_admin=is_admin)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash('Usuário adicionado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/user/add_user.html')


@admin_blueprint.route('/admin/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('admin.admin_dashboard'))


@admin_blueprint.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = Users.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.is_admin = 'is_admin' in request.form
        password = request.form.get('password')

        if password:
            user.set_password(password)

        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/user/edit_user.html', user=user)