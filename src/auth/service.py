from datetime import datetime, timedelta
from os import environ
from typing import Annotated
from uuid import UUID, uuid4

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.entities.users import Users
from src.entities.tokens import Token as SavedToken

from ..exceptions import AuthenticationError, UserNotFoundError
from .models import RegisterUserRequest, Token, TokenData

SECRET_KEY = environ.get("SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(secret=plain_password, hash=hashed_password)


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(secret=password)


def authenticate_user(login: str, password: str, db: Session) -> Users | bool:
    user = db.query(Users).filter(Users.login == login, ).first()

    if not user:
        raise UserNotFoundError(login=login)

    if not verify_password(
            plain_password=password,
            hashed_password=user.password_hash
    ):
        return False

    return user


def create_access_token(login: str, user_id: UUID, expires_delta: timedelta) -> str:
    encode = {
        "sub": login,
        "id": str(user_id),
        "ex": (datetime.now() + expires_delta).isoformat()
    }

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")

        return TokenData(user_id=user_id)
    except PyJWTError as e:
        raise AuthenticationError()


def register_user(db: Session, register_user_request: RegisterUserRequest) -> Users:
    try:
        create_user_model = Users(
            id=uuid4(),
            login=register_user_request.login,
            password_hash=bcrypt_context.hash(register_user_request.password),
            name=register_user_request.name
        )
        db.add(create_user_model)
        db.commit()
    except Exception as e:
        print(e)
        raise Exception(f"Failed to register user {register_user_request.model_dump()}")


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    return verify_token(token)


AuthenticatedUser = Annotated[TokenData, Depends(get_current_user)]


def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session) -> Token:
    user = authenticate_user(
        login=form_data.username,
        password=form_data.password,
        db=db
    )

    if not user:
        print(form_data)
        raise AuthenticationError()

    # TODO: make check existing token

    token = create_access_token(
        login=form_data.username,
        user_id=user.id,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    saved_token = SavedToken(
        token=token,
        user_id=user.id
    )

    db.add(saved_token)
    db.commit()

    return Token(
        access_token=token,
        token_type="bearer"
    )
