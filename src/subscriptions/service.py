from uuid import UUID, uuid4

from sqlalchemy import insert, delete
from sqlalchemy.orm import Session

from ..entities.subscriptions import Subscriptions


def add_subscription(title: str, description: str, price: float, days: int, user_id: UUID, db: Session):
    s_id = uuid4()

    result = db.execute(
        insert(Subscriptions).values(
            id=s_id,
            title=title,
            description=description,
            price=price,
            days=days,
            user_id=user_id,
        )
    )
    db.commit()

    return s_id


def delete_subscription(id: UUID, db: Session):
    db.execute(delete(Subscriptions).where(Subscriptions.id == id, ))
    db.commit()

