from logging import getLogger

import src.entities
from src.database.core import Base, engine


logger = getLogger(__name__)


def init_db():
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")


init_db()
