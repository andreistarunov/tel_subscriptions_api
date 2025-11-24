from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, UUID, Column, String
from sqlalchemy.orm import foreign, relationship

from ..database.core import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid4())
    name = Column(String, nullable=False)
    login = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())

    subscriptions = relationship("Subscriptions", back_populates="user")
    tokens = relationship("Token", back_populates="user")