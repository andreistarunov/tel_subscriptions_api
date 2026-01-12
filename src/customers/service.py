from uuid import UUID

from sqlalchemy import select

from src.customers.models import (
    CreateCustomerRequest,
    CreateCustomerResponse,
    GetCustomersByUserIdResponse,
    GetCustomersByUserIdRequest
)
from src.database.core import DbSession
from src.entities import Customers, CustomersSubscriptions, Subscriptions


def add_customer(entity: CreateCustomerRequest, db: DbSession) -> CreateCustomerResponse:
    try:
        customer = Customers(**entity.dict())
        db.add(customer)
        db.commit()

        return customer
    except Exception as e:
        raise


def get_customers_by_user_id(user_id: UUID, db: DbSession):
    try:
        customers = db.execute(
            statement=select(Customers)
            .join(CustomersSubscriptions, Customers.id == CustomersSubscriptions.customer_id,)
            .join(Subscriptions, Subscriptions.id == CustomersSubscriptions.subscription_id, )
            .where(Subscriptions.user_id == user_id, )
        ).fetchall()

        return [
            cust[0].__dict__
            for cust in customers
        ]
    except Exception as e:
        raise
