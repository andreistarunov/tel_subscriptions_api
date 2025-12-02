from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import register_routes
from src.logging import configure_logging, LogLevels

configure_logging(log_level=LogLevels.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_routes(app)
