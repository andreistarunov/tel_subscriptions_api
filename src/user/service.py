from uuid import UUID

from sqlalchemy.orm import Session

from ..entities.users import Users
from .models import UserResponse, PasswordChange
from ..exceptions import UserNotFoundError, InvalidPasswordError, PasswordMismatchError
from ..auth.service import verify_password, get_password_hash


def get_user_by_uuid(user_uuid: UUID, db: Session) -> UserResponse:
    user = db.query(Users).filter(Users.id == user_uuid, ).first()

    if not user:
        raise UserNotFoundError()

    return user


def change_password(db: Session, user_uuid: UUID, change_password_request: PasswordChange):
    try:
        user = db.query(Users).filter(Users.id == user_uuid, ).first()

        if not verify_password(
                plain_password=change_password_request.current_password,
                hashed_password=user.hashed_password
        ):
            raise InvalidPasswordError()

        if change_password_request.new_password != change_password_request.new_password_confirm:
            raise PasswordMismatchError()

        user.hashed_password = get_password_hash(password=change_password_request.new_password)
        db.commit()
    except Exception as e:
        raise
