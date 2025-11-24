from uuid import uuid4

from sqlalchemy import UUID, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database.core import Base
from .users import Users


class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID, primary_key=True, default=uuid4())
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    days = Column(Integer, nullable=False)
    user_id = Column(UUID, ForeignKey(Users.id))

    user = relationship("Users", back_populates="subscriptions")
