from sqlalchemy import Column, VARCHAR, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base


class ProductImageModel(Base):
    __tablename__ = "product_image"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    product_id = Column(BIGINT(unsigned=True), ForeignKey("product.id"), nullable=False, index=True)
    url = Column(VARCHAR(500), nullable=False)
    principal = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    product = relationship("ProductModel", back_populates="images")

    def __init__(self, product_id, url, principal=False):
        self.product_id = product_id
        self.url = url
        self.principal = principal
