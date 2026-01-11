from uuid import UUID, uuid4

from sqlalchemy import insert, delete, select
from sqlalchemy.orm import Session

from src.entities.subscriptions import Subscriptions


def add_subscription(title: str, description: str, price: float, days: int, user_id: UUID, db: Session):
    s_id = uuid4()

    subs = Subscriptions(
        id=s_id,
        title=title,
        description=description,
        price=price,
        days=days,
        user_id=user_id,
    )
    db.add(subs)
    db.commit()

    return subs


def delete_subscription(id: UUID, user_id: UUID, db: Session):
    db.execute(delete(Subscriptions).where(Subscriptions.id == id, Subscriptions.user_id == user_id, ))
    db.commit()


def get_subscriptions_by_user(user_id: UUID, db: Session):
    """Function for get subscriptions from table by user_id

    Args:
        user_id: user UUID
        db: db instance
    """
    return [
        item[0].__dict__
        for item in db.execute(statement=select(Subscriptions).filter(Subscriptions.user_id == user_id, )).fetchall()
    ]
