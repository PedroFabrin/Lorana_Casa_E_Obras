from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import BIGINT
from app.model.base import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    name = Column(VARCHAR(255), index=True, nullable=False)
    email = Column(VARCHAR(255), index=True, nullable=False)
    cpf = Column(VARCHAR(11), index=True, nullable=False)
    password = Column(VARCHAR(255), nullable=False)

    def __init__(self, name, email, cpf, password):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.password = password
