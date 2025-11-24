from uuid import UUID

from pydantic import BaseModel

class SubscriptionsRequest(BaseModel):
    title: str
    description: str
    price: float
    days: int
    seller_id: UUID

class SubscriptionsResponse(BaseModel):
    id: UUID
    title: str
    description: str
    price: float
    days: int
    seller_id: UUID