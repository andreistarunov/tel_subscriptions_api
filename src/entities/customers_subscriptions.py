from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from ..database.core import Base


class CustomersSubscriptions(Base):
    __tablename__ = "customers_subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False,
    )

    subscription_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subscriptions.id"),
        nullable=False,
    )

    is_active = Column(Boolean, default=True, nullable=False)
    expired_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    customer = relationship(
        "Customers",
        back_populates="customers_subscriptions",
        foreign_keys=[customer_id],
    )

    subscription = relationship(
        "Subscriptions",
        back_populates="customers_subscriptions",
        foreign_keys=[subscription_id],
    )
