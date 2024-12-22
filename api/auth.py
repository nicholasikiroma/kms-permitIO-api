from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..services import UserService, TenantService
from ..utils.auth import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    oauth2_scheme,
    blacklisted_tokens,
)
from ..schemas.users import LoginSchema, RegisterSchema, UserCreate, UserSchema
from ..schemas.auth_token import RefreshTokenResponse
from ..utils.session import get_db
from ..schemas import StandardResponse

authRouter = APIRouter(prefix="/auth", tags=["Auth"])


@authRouter.post("/register", response_model=StandardResponse[RegisterSchema])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new user account if the email doesn't already exist
    """
    existing_user = UserService.get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists.",
        )

    tenant_data = {
        "name": "test-0",
        "description": "Default organisation",
        "owner": None,
    }
    # create tenant
    new_tenant = await TenantService.create_tenant(db, tenant_data)

    # Create the new user
    new_user = await UserService.create_user(db, user, new_tenant.id)
    new_tenant.update(db, owner=new_user.id)

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    user_schema = UserSchema.model_validate(new_user)
    user_dict = user_schema.model_dump()

    # Convert UUIDs to strings
    user_dict["id"] = str(user_dict["id"])
    user_dict["workspaces"] = [
        str(workspace_id) for workspace_id in user_dict["workspaces"]
    ]
    user_dict["active_workspace"] = str(user_dict["active_workspace"])

    # Return the newly created user with standard response
    return JSONResponse(
        {
            "data": {
                "user": user_dict,
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            },
            "status": "success",
        },
        status_code=status.HTTP_201_CREATED,
    )


@authRouter.post("/login", response_model=StandardResponse[LoginSchema])
async def login_user(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "data": {
            "user": user,
            "tokens": {"access_token": access_token, "refresh_token": refresh_token},
        },
        "message": "Login successful",
        "status_code": status.HTTP_200_OK,
    }


@authRouter.get("/refresh", response_model=StandardResponse[RefreshTokenResponse])
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "data": {},
            "message": "Could not validate credentials",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(refresh_token, credentials_exception)
    new_access_token = create_access_token(data={"sub": email})

    return {
        "data": {"access_token": new_access_token},
        "message": "Token refreshed successfully",
        "status_code": status.HTTP_200_OK,
    }


@authRouter.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=StandardResponse[dict],
)
async def logout(token: str = Depends(oauth2_scheme)):
    """
    Revoke the token by blacklisting it.
    """
    blacklisted_tokens[token] = datetime.now()
    return {
        "message": "Logged out successfully.",
        "status_code": status.HTTP_200_OK,
        "data": {},
    }
