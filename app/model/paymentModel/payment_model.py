from sqlalchemy import Column, VARCHAR, DECIMAL, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base
import enum


class PaymentGatewayEnum(enum.Enum):
    mock = "mock"
    mercadopago = "mercadopago"


class PaymentStatus(enum.Enum):
    pendente = "pendente"
    aprovado = "aprovado"
    recusado = "recusado"


class PaymentModel(Base):
    __tablename__ = "payment"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    order_id = Column(BIGINT(unsigned=True), ForeignKey("customer_order.id"), nullable=False, unique=True, index=True)
    gateway = Column(Enum(PaymentGatewayEnum), nullable=False, default=PaymentGatewayEnum.mock)
    forma_pagamento = Column(VARCHAR(20), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.pendente, index=True)
    transaction_id = Column(VARCHAR(100), nullable=True)
    valor = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    order = relationship("OrderModel", back_populates="payment")

    def __init__(self, order_id, forma_pagamento, valor, gateway=PaymentGatewayEnum.mock, status=PaymentStatus.pendente, transaction_id=None):
        self.order_id = order_id
        self.forma_pagamento = forma_pagamento
        self.valor = valor
        self.gateway = gateway
        self.status = status
        self.transaction_id = transaction_id
