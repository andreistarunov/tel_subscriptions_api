from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    name: str
    login: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
