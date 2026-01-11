from uuid import UUID

from pydantic import BaseModel


class CreateCustomerRequest(BaseModel):
    name: str
    telegram_id: int


class CreateCustomerResponse(CreateCustomerRequest):
    pass


class GetCustomersByUserIdRequest(BaseModel):
    user_id: UUID


class GetCustomersByUserIdResponse(BaseModel):
    customers: list[CreateCustomerRequest]
