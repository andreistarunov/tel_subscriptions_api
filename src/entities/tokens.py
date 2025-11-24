from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    ForeignKey,
    UUID
)
from sqlalchemy.orm import relationship

from src.database.core import Base
from src.entities.users import Users


class Token(Base):
    __tablename__ = "tokens"

    id = Column(UUID, primary_key=True, default=uuid4())
    token = Column(String)
    user_id = Column(UUID, ForeignKey(Users.id))
    created_at = Column(TIMESTAMP, default=datetime.now())

    user = relationship("Users", back_populates="tokens")
