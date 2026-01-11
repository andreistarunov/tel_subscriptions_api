from fastapi import APIRouter, status

from src.user import models, service
from src.auth.service import AuthenticatedUser
from src.database.core import DbSession

router = APIRouter(
    prefix="/password",
    tags=["password"]
)

@router.get("/me", response_model=models.UserResponse)
async def current_user(current_user: AuthenticatedUser, db: DbSession):
    return service.get_user_by_uuid(
        user_uuid=current_user.user_id,
        db=db
    )

@router.put("change")
async def change_password(
        password_change: models.PasswordChange,
        db: DbSession,
        current_user: AuthenticatedUser
):
    service.change_password(
        db=db,
        change_password_request=password_change,
        user_uuid=current_user.get_uuid()
    )