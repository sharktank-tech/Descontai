from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# =====================
# Usuários
# =====================
class User(UserMixin):
    def __init__(
        self,
        id: int,
        username: str,
        email: str,
        password_hash: str = None,
        is_admin: bool = False,
        created_at: str = None,
        updated_at: str = None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.created_at = self._parse_date(created_at)
        self.updated_at = self._parse_date(updated_at)

    # -------- Password --------
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    # -------- Helpers --------
    @staticmethod
    def _parse_date(value):
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", ""))
        except Exception:
            return None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            email=data.get("email"),
            password_hash=data.get("password_hash"),
            is_admin=data.get("is_admin", False),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
        }

    def __repr__(self):
        return f"<User id={self.id} username={self.username} admin={self.is_admin}>"



##=====================
# Categorias
# =====================
class Categoria:
    def __init__(
        self,
        id: int,
        nome: str,
        descricao: str = None,
        ativa: bool = True,
        created_at: str = None,
        updated_at: str = None,
    ):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.ativa = ativa
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            nome=data.get("nome"),
            descricao=data.get("descricao"),
            ativa=data.get("ativa", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "ativa": self.ativa,
        }

    def __repr__(self):
        return f"<Categoria id={self.id} nome={self.nome} ativa={self.ativa}>"


# =====================
# Produtos
# =====================
class Produto:
    def __init__(
        self,
        id: int,
        name: str,
        image: str,
        originalprice: float,
        saleprice: float,
        discount: int,
        detailurl: str,
        rating: float = 4.5,
        vendidos: int = 0,
        origem: str = None,
        categoria: str = "Ofertas",
        created_at: str = None,
        updated_at: str = None,
    ):
        self.id = id
        self.name = name
        self.image = image
        self.originalprice = float(originalprice)
        self.saleprice = float(saleprice)
        self.discount = discount
        self.detailurl = detailurl
        self.rating = rating
        self.vendidos = vendidos
        self.origem = origem
        self.categoria = categoria
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            image=data.get("image"),
            originalprice=data.get("originalprice"),
            saleprice=data.get("saleprice"),
            discount=data.get("discount"),
            detailurl=data.get("detailurl"),
            rating=data.get("rating", 4.5),
            vendidos=data.get("vendidos", 0),
            origem=data.get("origem"),
            categoria=data.get("categoria", "Ofertas"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "originalPrice": f"R$ {self.originalprice:.2f}".replace(".", ","),
            "salePrice": f"R$ {self.saleprice:.2f}".replace(".", ","),
            "discount": f"{self.discount}%",
            "detailUrl": self.detailurl,
            "rating": round(self.rating, 1),
            "vendidos": f"{self.vendidos:,}".replace(",", "."),
            "origem": self.origem,
            "categoria": self.categoria,
        }

    def __repr__(self):
        return f"<Produto id={self.id} name={self.name} saleprice={self.saleprice}>"
""'"'