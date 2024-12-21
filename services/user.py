from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.session import get_db
from ..schemas.users import UserCreate
from ..utils.auth import (
    get_password_hash,
    verify_access_token,
    verify_password,
    oauth2_scheme,
    optional_oauth2_scheme,
)
from ..models.users import Users


class UserService:

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> Users:
        """Static method to create a new user in the database."""
        hashed_password = get_password_hash(user.password)
        new_user = Users(
            email=user.email,
            hashed_password=hashed_password,
            active_workspace=user.tenant_id,
            workspaces=[user.tenant_id],
        )
        new_user.add(db)
        new_user.save(db)
        return new_user

    @staticmethod
    def get_user_by_id(db: Session, id: str, tenant_id: str) -> Users:
        user = Users.get_by_id(db, id, tenant_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Users:
        """Fetch a user by email."""
        return Users.filter_by(db, email=email)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Users:
        """Authenticate a user by email and password."""
        user = UserService.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_current_user(token: str, db: Session):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        username = verify_access_token(token, credentials_exception)
        user = UserService.get_user_by_email(db, username)
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    def update_user_password(
        db: Session, password: str, id: str, tenant_id: str
    ) -> Users:
        hashed_password = get_password_hash(password)
        user = UserService.get_user_by_id(db, id, tenant_id)
        user.update(db, password_hash=hashed_password)
        return user


# Wrapper for dependency injection
def get_current_user_dep(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    return UserService.get_current_user(token, db)


def get_current_user_optional(
    token: Optional[str] = Depends(optional_oauth2_scheme),
    db: Session = Depends(get_db),
):
    if token is None:
        return None

    return UserService.get_current_user(token, db)
