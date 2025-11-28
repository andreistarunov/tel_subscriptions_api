from uuid import UUID

from fastapi import APIRouter

from src.auth.service import AuthenticatedUser
from .models import SubscriptionsRequest
from .service import add_subscription, delete_subscription
from ..database.core import DbSession

router = APIRouter(
    prefix='/subscriptions',
    tags=['subscriptions']
)

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
def remove_subscription(id: UUID, db: DbSession):
    return delete_subscription(
        id=id,
        db=db
    )