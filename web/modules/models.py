from web import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship


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


# Tabela de Categorias
class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    ativa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relacionamento com produtos
    produtos = relationship('Produto', back_populates='categoria_rel')

    def __repr__(self):
        return f"<Categoria(id={self.id}, nome='{self.nome}')>"

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(512), nullable=False)
    originalprice = db.Column(db.Float, nullable=False)
    saleprice = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    detailurl = db.Column(db.String(512), nullable=False)

    # Campos adicionais
    rating = db.Column(db.Float, default=4.5)
    vendidos = db.Column(db.String(20), default='1k+')
    origem = db.Column(db.String(50), nullable=False)  # Nova coluna para site de origem

    # Relacionamento com categoria
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    categoria_rel = relationship('Categoria', back_populates='produtos')

    # Campos de timestamp
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Propriedade para compatibilidade com código existente
    @property
    def categoria(self):
        return self.categoria_rel.nome if self.categoria_rel else 'Ofertas'

    def __repr__(self):
        return f"<Produto(id={self.id}, name='{self.name}', saleprice={self.saleprice}, origem='{self.origem}')>"

    def to_dict(self):
        """Converte o objeto Produto para um dicionário com os formatos desejados"""
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'originalPrice': f"R$ {self.originalprice:.2f}".replace('.', ','),
            'salePrice': f"R$ {self.saleprice:.2f}".replace('.', ','),
            'discount': int(self.discount),
            'detailUrl': self.detailurl,
            'rating': self.rating,
            'vendidos': self.vendidos,
            'origem': self.origem,  # Novo campo adicionado
            'categoria': self.categoria
        }