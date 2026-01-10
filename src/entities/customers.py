from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, UUID, Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.core import Base


class Customers(Base):
    __tablename__ = "customers"

    id = Column(UUID, primary_key=True, default=uuid4())
    name = Column(String, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())

    customers_subscriptions = relationship(
        "CustomersSubscriptions",
        back_populates="customer",
        foreign_keys="CustomersSubscriptions.customer_id",
        cascade="all, delete-orphan",
    )