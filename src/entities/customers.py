from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, UUID, Column, Integer, String

from ..database.core import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID, primary_key=True, default=uuid4())
    name = Column(String, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())

