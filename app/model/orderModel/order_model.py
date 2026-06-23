from sqlalchemy import Column, DECIMAL, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base
import enum


class OrderStatus(enum.Enum):
    pendente = "pendente"
    pago = "pago"
    em_separacao = "em_separacao"
    enviado = "enviado"
    entregue = "entregue"
    cancelado = "cancelado"
    nao_aprovado = "nao_aprovado"


class OrderModel(Base):
    __tablename__ = "customer_order"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("user.id"), nullable=False, index=True)
    adress_id = Column(BIGINT(unsigned=True), ForeignKey("adress.id"), nullable=False, index=True)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.pendente, index=True)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    desconto = Column(DECIMAL(10, 2), nullable=False, default=0)
    total = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("UserModel")
    adress = relationship("AdressModel")
    items = relationship("OrderItemModel", back_populates="order")
    payment = relationship("PaymentModel", back_populates="order", uselist=False)

    def __init__(self, user_id, adress_id, subtotal, total, desconto=0, status=OrderStatus.pendente):
        self.user_id = user_id
        self.adress_id = adress_id
        self.subtotal = subtotal
        self.desconto = desconto
        self.total = total
        self.status = status
