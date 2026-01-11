from fastapi import APIRouter

from src.auth.service import AuthenticatedUser
from src.customers.models import CreateCustomerRequest
from src.customers.service import (
    get_customers_by_user_id,
    add_customer
)
from src.database.core import DbSession

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)


@router.get("/")
def get_users_customers(db: DbSession, current_user: AuthenticatedUser):
    return get_customers_by_user_id(
        db=db,
        user_id=current_user.user_id
    )


@router.post("/")
def create_customer(db: DbSession, customer: CreateCustomerRequest, current_user: AuthenticatedUser):
    return add_customer(
        entity=customer,
        db=db
    )
