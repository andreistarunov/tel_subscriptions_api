import time
import unittest

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import (
    select,
    delete
)

from src.auth.models import RegisterUserRequest
from src.auth.service import register_user, login_for_access_token
from src.database.core import get_db
from src.entities import Users


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.db = get_db().__next__()
        self.prepared_user_data = RegisterUserRequest(
            name="test",
            login="test",
            password="test",
        )

    def tearDown(self):
        self.db.execute(statement=delete(Users).where(Users.login == "test", ))
        self.db.commit()

    def test_register_user(self):
        registered = register_user(
            register_user_request=self.prepared_user_data,
            db=self.db
        )

        time.sleep(0.3)

        actual = self.db.execute(statement=select(Users).where(Users.login == "test", )).scalar_one_or_none()

        self.assertIsNotNone(actual)

        for key, value in actual.__dict__.items():
            self.assertEqual(
                first=value,
                second=getattr(registered, key)
            )

    def test_login_for_access_token(self):
        register_user(
            register_user_request=self.prepared_user_data,
            db=self.db
        )
        time.sleep(0.3)

        token = login_for_access_token(
            form_data=OAuth2PasswordRequestForm(
                username=self.prepared_user_data.login,
                password=self.prepared_user_data.password,
                grant_type="password",
            ),
            db=self.db
        )

        self.assertIsNotNone(token)