from web import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Tabela de Usuários
class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(512), nullable=False)
    originalprice = db.Column(db.Float, nullable=False)
    saleprice = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    detailurl = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return f"<Produto(name='{self.name}', salePrice={self.salePrice})>"
