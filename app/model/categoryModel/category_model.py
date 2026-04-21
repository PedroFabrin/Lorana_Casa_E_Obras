from sqlalchemy import Column, VARCHAR, TEXT
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from app.model.base import Base


class CategoryModel(Base):
    __tablename__ = "category"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(255), nullable=False, index=True)
    descricao = Column(TEXT, nullable=True)

    products = relationship("ProductModel", back_populates="category")

    def __init__(self, nome, descricao=None):
        self.nome = nome
        self.descricao = descricao
