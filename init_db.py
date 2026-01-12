from logging import getLogger

from sqlalchemy import text

import src.entities
from src.database.core import Base, engine, get_db


logger = getLogger(__name__)


def init_db():
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")

    get_db().__next__().execute(statement=text("select 1;"))


init_db()
