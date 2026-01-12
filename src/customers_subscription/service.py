from logging import error
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import func, select

from src.customers_subscription.models import (
    GetCustomersSubscriptionListByUserIdResponse,
    CustomersSubscription,
    CreateCustomersSubscriptionRequest, CreateCustomersSubscriptionResponse
)

from src.entities import (
    Customers,
    Subscriptions,
    CustomersSubscriptions
)


def get_customers_subscription_by_user_id(user_id: UUID, db: Session) -> GetCustomersSubscriptionListByUserIdResponse:
    subscriptions = db.execute(
        statement=select(
            func.json_build_object(
                "name", Customers.name,
                "telegram_id", Customers.telegram_id,
                "subscription", Subscriptions.title,
                "is_active", CustomersSubscriptions.is_active,
                "expired_at", CustomersSubscriptions.is_active,
                "created_at", CustomersSubscriptions.created_at,
            )
        ).select_from(CustomersSubscriptions)
        .join(Customers, CustomersSubscriptions.customer_id == Customers.id, )
        .join(Subscriptions, CustomersSubscriptions.subscription_id == Subscriptions.id, )
        .where(Subscriptions.user_id == user_id, )
    ).fetchall()

    return GetCustomersSubscriptionListByUserIdResponse(
        subscriptions=[CustomersSubscription(item[0].__dict__) for item in subscriptions]
    )


def add_customers_subscription(entity: CreateCustomersSubscriptionRequest, db: Session):
    try:
        cust_subs = CustomersSubscriptions(**entity.dict())
        db.add(cust_subs)
        db.commit()

        return cust_subs
    except Exception as e:
        error(e)


def unactive_customers_subscription(subs_id: UUID, db: Session):
    pass
