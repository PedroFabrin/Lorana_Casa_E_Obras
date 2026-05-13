from sqlalchemy import Column, VARCHAR, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base


class UserModel(Base):
    __tablename__ = "users_types"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    type =  Column(VARCHAR(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("UserModel", back_populates="user_type")

    def __init__(self, name, email, cpf, password):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.password = password
