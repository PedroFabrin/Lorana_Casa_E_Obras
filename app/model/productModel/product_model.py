from sqlalchemy import Column, VARCHAR, TEXT, DECIMAL, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
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
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    category = relationship("CategoryModel", back_populates="products")
    images = relationship("ProductImageModel", back_populates="product")

    def __init__(self, category_id, nome, preco, sku, quantidade_estoque, status=ProductStatus.ativo, descricao=None):
        self.category_id = category_id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.sku = sku
        self.quantidade_estoque = quantidade_estoque
        self.status = status
