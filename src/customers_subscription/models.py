from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class CreateCustomersSubscriptionRequest(BaseModel):
    user_id: UUID
    subscription_id: UUID
    expired_at: datetime


class CreateCustomersSubscriptionResponse(BaseModel):
    success: bool
    data: CreateCustomersSubscriptionRequest


class CustomersSubscription(BaseModel):
    name: str
    telegram_id: str
    subscription: str
    is_active: bool
    expired_at: datetime
    created_at: datetime


class GetCustomersSubscriptionListByUserIdResponse(BaseModel):
    subscriptions: list[CustomersSubscription]
