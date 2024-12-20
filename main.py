from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .utils.auth import verify_token_blacklist
from .database import engine
from .api import (
    authRouter,
    userRouter,
)
from . import models

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(BaseHTTPMiddleware, dispatch=verify_token_blacklist)

# register api modules
app.include_router(authRouter)
app.include_router(userRouter)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
