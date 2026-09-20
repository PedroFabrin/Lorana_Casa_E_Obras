from sqlalchemy import Column, VARCHAR, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.sql import func
from app.model.base import Base


class RevokedTokenModel(Base):
    __tablename__ = "revoked_token"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    jti = Column(VARCHAR(64), nullable=False, unique=True, index=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("user.id"), nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    def __init__(self, jti, user_id, expires_at):
        self.jti = jti
        self.user_id = user_id
        self.expires_at = expires_at
