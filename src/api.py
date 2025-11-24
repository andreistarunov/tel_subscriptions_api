from fastapi import FastAPI

from src.auth.contoller import router as auth_router
from src.user.controller import router as user_router
from src.subscriptions.controller import router as subscriptions_router
from src.ping.controller import router as ping_router


def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(subscriptions_router)
    app.include_router(ping_router)
