from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..schemas import ArticleCreateSchema, ArticleUpdateSchema
from ..models import KnowledgeArticles


class ArticleService:

    @staticmethod
    def create_article(db: Session, article: ArticleCreateSchema):
        """Static method to create a new knowledge article in the database."""

        new_article = KnowledgeArticles(
            title=article.title,
            tenant_id=article.tenant_id,
            author_id=article.author_id,
            content=article.content,
            tags=article.tags,
        )
        new_article.add(db)
        new_article.save(db)

        return new_article

    @staticmethod
    def retrieve_tenant_articles(db: Session, tenant_id: str):
        articles = KnowledgeArticles.filter_by(session=db, tenant_id=tenant_id)
        return articles

    @staticmethod
    def get_article_by_id(db: Session, tenant_id: str, article_id: str):
        return KnowledgeArticles.get_by_id(
            session=db, obj_id=article_id, tenant_id=tenant_id
        )

    @staticmethod
    def update_article(
        db: Session, article_id: str, tenant_id: str, update_obj: ArticleUpdateSchema
    ):
        article = KnowledgeArticles.get_by_id(
            session=db, obj_id=article_id, tenant_id=tenant_id
        )
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "fail",
                    "data": {"id": f"Article '{article_id}' not found."},
                },
            )

        article.update(db, update_obj)

    @staticmethod
    def delete_article(db: Session, article_id: str, tenant_id: str):
        article = KnowledgeArticles.get_by_id(
            session=db, obj_id=article_id, tenant_id=tenant_id
        )
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Article not found."
            )
        article.delete(session=db)
        return article