from logging import getLogger

from sqlalchemy.exc import SQLAlchemyError

from src.database.core import Base, engine

logger = getLogger(__name__)


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except SQLAlchemyError as e:
        logger.exception("Database initialization failed")


init_db()
