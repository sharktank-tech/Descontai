from web import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    email = db.Column(db.String(255),unique=True,nullable=False)
    password_hash = db.Column(db.Text,nullable=False)
    is_admin = db.Column(db.Boolean,default=False,nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    # Password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):return f"<User {self.username}>"

# ===== Tabela de categorias ======

class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.BigInteger,primary_key=True)
    nome = db.Column(db.String(120),unique=True,nullable=False)
    descricao = db.Column(db.Text)
    ativa = db.Column(db.Boolean,default=True,nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)