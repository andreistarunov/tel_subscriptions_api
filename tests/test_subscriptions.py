from random import randint
import unittest

from sqlalchemy import select, delete

from src.auth.models import RegisterUserRequest
from src.database.core import get_db
from src.entities import Users, Subscriptions
from src.subscriptions.service import add_subscription, get_subscriptions_by_user, delete_subscription
from src.auth.service import register_user


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.db = get_db().__next__()
        register_user(
            db=self.db,
            register_user_request=RegisterUserRequest(
                login="test",
                password="test",
                name="test",
            )
        )

        self.user = self.db.execute(statement=select(Users).where(Users.login == "test", )).fetchall()[0][0]

    def tearDown(self):
        self.db.execute(statement=delete(Subscriptions).where(Users.id == self.user.id, ))
        self.db.execute(statement=delete(Users).where(Users.login == "test", ))
        self.db.commit()

    def test_add_subscription(self):
        prepared = {
            "title": "title test",
            'description': "description test",
            "price": randint(0, 10000) * 1.0,
            "days": randint(0, 10000),
            "user_id": self.user.id,
        }
        subscription = add_subscription(
            **prepared,
            db=self.db
        )

        subs = self.db.execute(statement=select(Subscriptions).where(Subscriptions.id == subscription.id, )).fetchall()

        self.assertEqual(
            first=1,
            second=len(subs),
        )
        self.assertEqual(
            first=1,
            second=len(subs[0]),
        )

        for key, value in subs[0][0].__dict__.items():
            if key not in ("_sa_instance_state", "id"):
                self.assertEqual(
                    first=prepared.get(key),
                    second=value
                )

    def test_get_subscriptions_by_user(self):
        # Arrange
        prepared = {
            "title": "title test",
            'description': "description test",
            "price": randint(0, 10000) * 1.0,
            "days": randint(0, 10000),
            "user_id": self.user.id,
        }
        add_subscription(
            **prepared,
            db=self.db
        )

        # Act
        subs = get_subscriptions_by_user(
            user_id=self.user.id,
            db=self.db
        )

        # Assert
        self.assertEqual(
            first=1,
            second=len(subs),
        )

        for key, value in subs[0].items():
            if key not in ("_sa_instance_state", "id"):
                self.assertEqual(
                    first=prepared.get(key),
                    second=value
                )

    def test_delete_subscription(self):
        prepared = {
            "title": "title test",
            'description': "description test",
            "price": randint(0, 10000) * 1.0,
            "days": randint(0, 10000),
            "user_id": self.user.id,
        }
        subscription = add_subscription(
            **prepared,
            db=self.db
        )

        # Act
        delete_subscription(
            id=subscription.id,
            user_id=self.user.id,
            db=self.db
        )
        subs = self.db.execute(statement=select(Subscriptions).where(Subscriptions.id == subscription.id, )).fetchall()

        # Assert
        self.assertEqual(
            first=0,
            second=len(subs),
        )
