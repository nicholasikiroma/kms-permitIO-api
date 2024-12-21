from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, List
from datetime import datetime

from ..models import ArticleStatus


class ArticleCreateSchema(BaseModel):
    title: str
    tenant_id: str
    author_id: str
    content: str
    tags: Optional[List[str]]


class ArticleUpdateSchema(BaseModel):
    title: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]


class ArticleCreateResponseSchema(BaseModel):
    id: uuid4
    title: str
    tenant_id: str
    author_id: str
    content: str
    status: ArticleStatus
    created_at: datetime
    updated_at: datetime
    tags: Optional[List[str]]
