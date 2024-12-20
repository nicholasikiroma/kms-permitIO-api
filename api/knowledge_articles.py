from fastapi import APIRouter, Response, status, HTTPException

tenantsRouter = APIRouter(
    prefix="/knowledge-articles",
)
