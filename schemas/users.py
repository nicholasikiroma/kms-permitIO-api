from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from datetime import datetime

from ..schemas.auth_token import AuthToken


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserProfileUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[UploadFile]


class UserSchema(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    is_admin: Optional[bool]
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None


class LoginSchema(BaseModel):
    tokens: AuthToken
    user: UserSchema


class RegisterSchema(BaseModel):
    user: UserSchema
    tokens: AuthToken

    class Config:
        orm_mode = True
