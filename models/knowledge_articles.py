from sqlalchemy import Column, String, DateTime, func, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from uuid import uuid4


from ..models.tenants import Tenants
from ..models.users import Users
from .base import Base


class KnowledgeArticles(Base):
    __tablename__ = "knowledge_articles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey(Tenants.id), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    tenant = relationship("Tenants", back_populates="knowledge_articles")
    author = relationship("Users", back_populates="knowledge_articles")

    def __repr__(self):
        return f"KnowledgeArticle('{self.title}', {self.id})"
