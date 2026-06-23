from sqlalchemy import Column, VARCHAR, TEXT, Enum, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base
import enum


class SectionStatus(enum.Enum):
    ativo = "ativo"
    inativo = "inativo"


class SectionModel(Base):
    __tablename__ = "section"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(255), nullable=False, index=True)
    descricao = Column(TEXT, nullable=True)
    status = Column(Enum(SectionStatus), nullable=False, default=SectionStatus.ativo)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    categories = relationship("CategoryModel", back_populates="section")

    def __init__(self, nome, descricao=None, status=SectionStatus.ativo):
        self.nome = nome
        self.descricao = descricao
        self.status = status
