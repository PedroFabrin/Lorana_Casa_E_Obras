from sqlalchemy import Column, VARCHAR, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from app.model.base import Base


class AdressModel(Base):
    __tablename__ = "adress"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("user.id"), nullable=False, index=True)
    rua = Column(VARCHAR(255), nullable=False)
    numero = Column(VARCHAR(10), nullable=False)
    cep = Column(VARCHAR(8), nullable=False)
    cidade = Column(VARCHAR(255), nullable=False)
    uf = Column(VARCHAR(2), nullable=False)

    user = relationship("UserModel", back_populates="adresses")

    def __init__(self, user_id, rua, numero, cep, cidade, uf):
        self.user_id = user_id
        self.rua = rua
        self.numero = numero
        self.cep = cep
        self.cidade = cidade
        self.uf = uf
