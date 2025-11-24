from src.database.core import engine

from src.entities.users import Users
from src.entities.customers import Customer
from src.entities.subscriptions import Subscriptions
from src.entities.tokens import Token


Users.__table__.create(engine)
Customer.__table__.create(engine)
Subscriptions.__table__.create(engine)
Token.__table__.create(engine)

# test string 2
