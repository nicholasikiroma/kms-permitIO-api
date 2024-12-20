from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


from .base import Base


class Tenants(Base):
    __tablename__ = "tenants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    users = relationship("Users", back_populates="tenant", cascade="all, delete-orphan")
    knowledge_articles = relationship(
        "KnowledgeArticles", back_populates="tenant", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Tenant('{self.name}', {self.id})"
