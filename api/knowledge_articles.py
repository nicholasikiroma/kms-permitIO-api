from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import session

from ..services import (
    get_current_user_dep,
    check_user_permission,
    Actions,
    ArticleService,
)
from ..schemas import (
    StandardResponse,
    ArticleCreateSchema,
    ArticleCreateResponseSchema,
    ArticleUpdateSchema,
)
from ..models import Users
from ..utils import session

articlesRouter = APIRouter(prefix="/knowledge-articles", tags=["Knowledge Articles"])


@articlesRouter.post("/", response_model=StandardResponse[ArticleCreateResponseSchema])
async def create_article(
    article: ArticleCreateSchema,
    db=Depends(session.get_db),
    current_user: Users = Depends(get_current_user_dep),
):
    """Creates a new article resource"""
    permitted = await check_user_permission(
        user_id=current_user.id,
        action=Actions.CREATE.value,
        tenant_id=current_user.tenant_id,
    )
    if not permitted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    new_article = ArticleService.create_article(db=db, article=article)

    return JSONResponse(
        {"data": new_article, "status": "success"}, status_code=status.HTTP_201_CREATED
    )


@articlesRouter.get(
    "/", response_model=StandardResponse[List[ArticleCreateResponseSchema]]
)
async def fetch_tenant_articles(
    db=Depends(session.get_db), current_user: Users = Depends(get_current_user_dep)
):
    """Fetch all knowledge resources in a tenant"""
    permitted = await check_user_permission(
        user_id=current_user.id,
        action=Actions.READ.value,
        tenant_id=current_user.tenant_id,
    )
    if not permitted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this resources",
        )
    articles = ArticleService.retrieve_tenant_articles(
        db=db, tenant_id=current_user.tenant_id
    )
    return JSONResponse(
        {"data": articles, "status": "success"}, status_code=status.HTTP_200_OK
    )


@articlesRouter.get(
    "/{article_id}", response_model=StandardResponse[ArticleCreateSchema]
)
async def fetch_article_by_id(
    article_id: str,
    db=Depends(session.get_db),
    current_user: Users = Depends(get_current_user_dep),
):
    """Fetch knowledge resource by ID"""
    permitted = await check_user_permission(
        user_id=current_user.id,
        action=Actions.READ.value,
        tenant_id=current_user.tenant_id,
    )
    if not permitted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this resources",
        )

    article = ArticleService.get_article_by_id(
        db=db, tenant_id=current_user.tenant_id, article_id=article_id
    )
    return JSONResponse(
        {"data": article, "status": "success"}, status_code=status.HTTP_200_OK
    )


@articlesRouter.patch(
    "/{article_id}", response_model=StandardResponse[ArticleCreateSchema]
)
async def update_by_id(
    article_id: str,
    update_obj: ArticleUpdateSchema,
    db=Depends(session.get_db),
    current_user: Users = Depends(get_current_user_dep),
):
    """Fetch knowledge resource by ID"""
    permitted = await check_user_permission(
        user_id=current_user.id,
        action=Actions.UPDATE.value,
        tenant_id=current_user.tenant_id,
    )
    if not permitted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this resources",
        )

    article = ArticleService.update_article(
        db=db,
        tenant_id=current_user.tenant_id,
        article_id=article_id,
        update_obj=update_obj,
    )
    return JSONResponse(
        {"data": article, "status": "success"}, status_code=status.HTTP_200_OK
    )


@articlesRouter.delete(
    "/{article_id}", response_model=StandardResponse[ArticleCreateSchema]
)
async def delete_by_id(
    article_id: str,
    db=Depends(session.get_db),
    current_user: Users = Depends(get_current_user_dep),
):
    """Fetch knowledge resource by ID"""
    permitted = await check_user_permission(
        user_id=current_user.id,
        action=Actions.DELETE.value,
        tenant_id=current_user.tenant_id,
    )
    if not permitted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this resources",
        )

    article = ArticleService.delete_article(
        db=db,
        tenant_id=current_user.tenant_id,
        article_id=article_id,
    )
    return JSONResponse(
        {"data": article, "status": "success"}, status_code=status.HTTP_200_OK
    )
