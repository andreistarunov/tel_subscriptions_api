from datetime import datetime
import unittest
from random import randint

from sqlalchemy import (
    select,
    delete
)

from src.auth.models import RegisterUserRequest
from src.customers.models import CreateCustomerRequest
from src.customers.service import (
    add_customer,
    get_users_customers
)
from src.auth.service import register_user
from src.customers_subscription.models import CreateCustomersSubscriptionRequest
from src.customers_subscription.service import add_customers_subscription
from src.subscriptions.service import add_subscription
from src.database.core import get_db
from src.entities import (
    Customers,
    Subscriptions,
    CustomersSubscriptions,
    Users
)


class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.db = get_db().__next__()

    def tearDown(self):
        users = self.db.execute(statement=select(Users).where(Users.login == "test")).fetchall()

        for user in users:
            subscriptions = self.db.execute(
                statement=select(Subscriptions).where(Subscriptions.user_id == user[0].id, )
            )

            for sub in subscriptions:
                self.db.execute(
                    statement=delete(CustomersSubscriptions).where(
                        CustomersSubscriptions.subscription_id == sub[0].id, )
                )
                self.db.commit()

            self.db.execute(
                statement=delete(Subscriptions).where(Subscriptions.user_id == user[0].id, )
            )
            self.db.execute(
                statement=delete(Users).where(Users.id == user[0].id, )
            )
            self.db.commit()

        self.db.execute(
            statement=delete(Customers).where(Customers.name == "test", )
        )
        self.db.commit()

    def test_add_customer(self):
        created = add_customer(
            db=self.db,
            entity=CreateCustomerRequest(
                name="test",
                telegram_id=randint(0, 10000)
            )
        )

        actual = self.db.execute(
            statement=select(Customers).where(Customers.telegram_id == created.telegram_id)
        ).scalar_one_or_none()

        self.assertIsNotNone(actual)

    def test_get_users_customers(self):
        # Arrange
        user = register_user(
            db=self.db,
            register_user_request=RegisterUserRequest(
                name="test",
                login="test",
                password="test"
            )
        )
        customer = add_customer(
            db=self.db,
            entity=CreateCustomerRequest(
                name="test",
                telegram_id=randint(0, 10000)
            )
        )
        prepared = {
            "title": "title test",
            'description': "description test",
            "price": randint(0, 10000) * 1.0,
            "days": randint(0, 10000),
            "user_id": user.id,
        }
        subscription = add_subscription(**prepared, db=self.db)

        # Act
        add_customers_subscription(
            db=self.db,
            entity=CreateCustomersSubscriptionRequest(
                customer_id=customer.id,
                subscription_id=subscription.id,
                expired_at=datetime.now()
            )
        )

        # Assert
        customers = get_users_customers(
            user_id=user.id,
            db=self.db
        )

        self.assertEqual(
            first=1,
            second=len(customers),
        )
