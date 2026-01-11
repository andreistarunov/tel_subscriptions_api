from fastapi import APIRouter

from src.auth.service import AuthenticatedUser
from src.customers_subscription.models import (
    CreateCustomersSubscriptionResponse,
    GetCustomersSubscriptionListByUserIdResponse,
    CreateCustomersSubscriptionRequest
)
from src.customers_subscription.service import (
    get_customers_subscription_by_user_id,
    add_customers_subscription
)
from src.database.core import DbSession

router = APIRouter(
    prefix="/customers_subscriptions",
    tags=["customers_subscriptions"]
)


@router.get("/")
def get_customers_subscription(
        db: DbSession,
        current_user: AuthenticatedUser
) -> GetCustomersSubscriptionListByUserIdResponse:
    return get_customers_subscription_by_user_id(user_id=current_user.user_id, db=db)


@router.post("/")
def create_customers_subscription(
        customers_subscription: CreateCustomersSubscriptionRequest,
        db: DbSession,
        current_user: AuthenticatedUser
):
    return add_customers_subscription(db=db, entity=customers_subscription)


@router.patch("/{subs_id}")
def unactive_subscription(db: DbSession, current_user: AuthenticatedUser):
    pass
