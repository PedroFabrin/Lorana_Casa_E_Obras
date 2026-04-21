from sqlalchemy import Column, VARCHAR, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    name = Column(VARCHAR(255), index=True, nullable=False)
    email = Column(VARCHAR(255), index=True, nullable=False)
    cpf = Column(VARCHAR(11), index=True, nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    adresses = relationship("AdressModel", back_populates="user")

    def __init__(self, name, email, cpf, password):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.password = password
