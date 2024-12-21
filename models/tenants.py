from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from .base import BaseModel


class Tenants(BaseModel):
    __tablename__ = "tenants"

    name = Column(String, unique=True, nullable=False)
    users = relationship("Users", back_populates="tenant", cascade="all, delete-orphan")
    knowledge_articles = relationship(
        "KnowledgeArticles", back_populates="tenant", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Tenant('{self.name}', {self.id})"
