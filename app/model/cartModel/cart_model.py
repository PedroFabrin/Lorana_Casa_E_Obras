from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base


class CartModel(Base):
    __tablename__ = "cart"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("user.id"), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("UserModel")
    items = relationship("CartItemModel", back_populates="cart")

    def __init__(self, user_id):
        self.user_id = user_id
