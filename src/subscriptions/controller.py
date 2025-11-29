from uuid import UUID

from fastapi import APIRouter

from src.auth.service import AuthenticatedUser
from src.subscriptions.models import SubscriptionsRequest
from src.subscriptions.service import (
    add_subscription,
    delete_subscription,
    get_subscriptions_by_user
)
from src.database.core import DbSession

router = APIRouter(
    prefix='/subscriptions',
    tags=['subscriptions']
)


@router.get('/{user_id}')
def get_subscriptions_by_user_id(user_id: UUID, db: DbSession):
    return get_subscriptions_by_user(user_id=user_id, db=db)


@router.post('/')
def create_subscription(subscription: SubscriptionsRequest, db: DbSession, current_user: AuthenticatedUser):
    return add_subscription(
        title=subscription.title,
        description=subscription.description,
        price=subscription.price,
        days=subscription.days,
        user_id=subscription.seller_id,
        db=db
    )


@router.delete('/')
def remove_subscription(id: UUID, db: DbSession, current_user: AuthenticatedUser):
    return delete_subscription(
        id=id,
        db=db
    )
