from fastapi.exceptions import HTTPException

class AuthenticationError(HTTPException):
    def __init__(self, user_id=None):
        super().__init__(status_code=401, detail=f"User {user_id} cannot authenticate")

class UserNotFoundError(HTTPException):
    def __init__(self, user_id=None, login=None):
        super().__init__(status_code=401, detail=f"User {user_id} / {login} cannot authenticate")

class InvalidPasswordError(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail=f"Invalid password")

class PasswordMismatchError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=f"Passwords mismatch")