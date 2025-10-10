from web import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship


# ---------------------
# Usuários
# ---------------------
class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)  # Evita duplicidade
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', admin={self.is_admin})>"


# ---------------------
# Categorias
# ---------------------
class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    ativa = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relacionamento
    produtos = relationship('Produto', back_populates='categoria_rel', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Categoria(id={self.id}, nome='{self.nome}', ativa={self.ativa})>"


# ---------------------
# Produtos
# ---------------------
class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(512), nullable=False)
    originalprice = db.Column(db.Numeric(10, 2), nullable=False)  # Melhor precisão que Float
    saleprice = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, nullable=False)  # Percentual inteiro
    detailurl = db.Column(db.String(512), nullable=False)

    rating = db.Column(db.Float, default=4.5)
    vendidos = db.Column(db.Integer, default=0)  # Número real, exibição formatada depois
    origem = db.Column(db.String(50), nullable=False)

    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    categoria_rel = relationship('Categoria', back_populates='produtos')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def categoria(self):
        return self.categoria_rel.nome if self.categoria_rel else 'Ofertas'

    def __repr__(self):
        return f"<Produto(id={self.id}, name='{self.name}', saleprice={self.saleprice}, origem='{self.origem}')>"

    def to_dict(self):
        """Converte para dicionário com formatação amigável"""
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'originalPrice': f"R$ {self.originalprice:.2f}".replace('.', ','),
            'salePrice': f"R$ {self.saleprice:.2f}".replace('.', ','),
            'discount': f"{self.discount}%",
            'detailUrl': self.detailurl,
            'rating': round(self.rating, 1),
            'vendidos': f"{self.vendidos:,}".replace(",", ".") if self.vendidos else "0",
            'origem': self.origem,
            'categoria': self.categoria
        }
