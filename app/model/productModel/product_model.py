from sqlalchemy import Column, VARCHAR, TEXT, DECIMAL, Enum, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from app.model.base import Base
import enum


class ProductStatus(enum.Enum):
    ativo = "ativo"
    inativo = "inativo"


class ProductModel(Base):
    __tablename__ = "product"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    category_id = Column(BIGINT(unsigned=True), ForeignKey("category.id"), nullable=False, index=True)
    nome = Column(VARCHAR(255), nullable=False, index=True)
    descricao = Column(TEXT, nullable=True)
    preco = Column(DECIMAL(10, 2), nullable=False)
    sku = Column(VARCHAR(100), nullable=False, unique=True, index=True)
    quantidade_estoque = Column(BIGINT(unsigned=True), nullable=False, default=0)
    status = Column(Enum(ProductStatus), nullable=False, default=ProductStatus.ativo)

    category = relationship("CategoryModel", back_populates="products")

    def __init__(self, category_id, nome, preco, sku, quantidade_estoque, status=ProductStatus.ativo, descricao=None):
        self.category_id = category_id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.sku = sku
        self.quantidade_estoque = quantidade_estoque
        self.status = status
