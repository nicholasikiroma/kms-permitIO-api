from sqlalchemy import Boolean, Column, String, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from enum import Enum as PyEnum

from ..models.tenants import Tenants
from .base import Base


class UserRoles(PyEnum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey(Tenants.id), nullable=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRoles), name="user_roles", default=UserRoles.VIEWER)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    knowledge_articles = relationship(
        "KnowledgeArticles", back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User('{self.email}', {self.is_active})"
