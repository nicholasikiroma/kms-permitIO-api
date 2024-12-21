from typing import Optional, List
from fastapi import UploadFile
from pydantic import BaseModel
from datetime import datetime

from ..schemas.auth_token import AuthToken


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    tenant_id: str


class UserProfileUpdate(BaseModel):
    name: Optional[str]
    avatar: Optional[UploadFile]


class UserSchema(UserBase):
    id: str
    workspaces: List[str]
    active_workspace: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    name: Optional[str] = None


class LoginSchema(BaseModel):
    tokens: AuthToken
    user: UserSchema


class RegisterSchema(BaseModel):
    user: UserSchema
    tokens: AuthToken

    class Config:
        orm_mode = True
