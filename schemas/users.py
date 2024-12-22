from typing import Optional, List, Union
from fastapi import UploadFile
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from ..models import UserRoles
from ..schemas.auth_token import AuthToken


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    role: UserRoles


class UserProfileUpdate(BaseModel):
    name: Optional[str]
    avatar: Optional[UploadFile]


class UserSchema(UserBase):
    id: UUID
    workspaces: List[UUID]
    active_workspace: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    role: str
    name: Optional[str] = None

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    tokens: AuthToken
    user: UserSchema


class RegisterSchema(BaseModel):
    user: UserSchema
    tokens: AuthToken

    class Config:
        from_attributes = True
