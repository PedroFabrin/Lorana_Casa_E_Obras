from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base


class CartItemModel(Base):
    __tablename__ = "cart_item"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    cart_id = Column(BIGINT(unsigned=True), ForeignKey("cart.id"), nullable=False, index=True)
    product_id = Column(BIGINT(unsigned=True), ForeignKey("product.id"), nullable=False, index=True)
    quantidade = Column(BIGINT(unsigned=True), nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    cart = relationship("CartModel", back_populates="items")
    product = relationship("ProductModel")

    def __init__(self, cart_id, product_id, quantidade):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantidade = quantidade
