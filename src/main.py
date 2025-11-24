from fastapi import FastAPI

from src.api import register_routes
from src.logging import configure_logging, LogLevels

configure_logging(log_level=LogLevels.INFO)

app = FastAPI()

register_routes(app)