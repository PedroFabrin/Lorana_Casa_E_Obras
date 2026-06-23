from sqlalchemy import Column, VARCHAR, TEXT, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base
import enum


class CategoryStatus(enum.Enum):
    ativo = "ativo"
    inativo = "inativo"


class CategoryModel(Base):
    __tablename__ = "category"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    section_id = Column(BIGINT(unsigned=True), ForeignKey("section.id"), nullable=False, index=True)
    nome = Column(VARCHAR(255), nullable=False, index=True)
    descricao = Column(TEXT, nullable=True)
    status = Column(Enum(CategoryStatus), nullable=False, default=CategoryStatus.ativo)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    section = relationship("SectionModel", back_populates="categories")
    products = relationship("ProductModel", back_populates="category")

    def __init__(self, section_id, nome, descricao=None, status=CategoryStatus.ativo):
        self.section_id = section_id
        self.nome = nome
        self.descricao = descricao
        self.status = status
