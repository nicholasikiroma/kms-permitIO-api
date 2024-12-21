from sqlalchemy import Column, String, DateTime, func, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from uuid import uuid4
from enum import Enum as PyEnum

from ..models.tenants import Tenants
from ..models.users import Users
from .base import Base, BaseModel


class ArticleStatus(PyEnum):
    PUBLISHED = "published"
    DRAFT = "draft"


class KnowledgeArticles(BaseModel):
    __tablename__ = "knowledge_articles"

    tenant_id = Column(UUID(as_uuid=True), ForeignKey(Tenants.id), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    status = Column(
        Enum(ArticleStatus), name="article_status", default=ArticleStatus.DRAFT
    )

    tenant = relationship("Tenants", back_populates="knowledge_articles")
    author = relationship("Users", back_populates="knowledge_articles")

    def __repr__(self):
        return f"KnowledgeArticle('{self.title}', {self.id})"
