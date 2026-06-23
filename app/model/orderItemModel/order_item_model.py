from sqlalchemy import Column, DECIMAL, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base


class OrderItemModel(Base):
    __tablename__ = "order_item"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    order_id = Column(BIGINT(unsigned=True), ForeignKey("customer_order.id"), nullable=False, index=True)
    product_id = Column(BIGINT(unsigned=True), ForeignKey("product.id"), nullable=False, index=True)
    quantidade = Column(BIGINT(unsigned=True), nullable=False)
    preco_unitario = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    order = relationship("OrderModel", back_populates="items")
    product = relationship("ProductModel")

    def __init__(self, order_id, product_id, quantidade, preco_unitario, subtotal):
        self.order_id = order_id
        self.product_id = product_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.subtotal = subtotal
