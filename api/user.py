from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, status, HTTPException

from ..services.user import get_current_user_dep
from ..models.users import Users
from ..utils import session
from ..schemas.response import StandardResponse
from ..schemas.users import UserProfileUpdate, UserSchema


userRouter = APIRouter(prefix="/users", tags=["Users"])


@userRouter.patch(
    "/profile",
    response_model=StandardResponse[UserSchema],
    description="This endpoints updates the name and avatar properties of the user model",
)
def update_user_profile(
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = File(None),
    db: session = Depends(session.get_db),
    current_user: Users = Depends(get_current_user_dep),
):
    """Update user profile"""
    if first_name:
        current_user.first_name = first_name

    if last_name:
        current_user.last_name = last_name

    db.commit()
    db.refresh(current_user)

    return {
        "data": current_user,
        "message": "Profile updated successfully",
        "status_code": status.HTTP_200_OK,
    }
