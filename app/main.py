import uvicorn
from typing import Callable
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.api_v1.api import api_router

from app.db.session import init_db
from app.db.connections import close_postgres_database_connection

from app.models import User


def start_app_handler(app: FastAPI) -> Callable:
    async def init() -> None:
        await init_db()
    return init


def stop_app_handler(app: FastAPI) -> Callable:
    async def stop_db() -> None:
        await close_postgres_database_connection(app)

    return stop_db


def get_app() -> FastAPI:
    server = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
    if settings.BACKEND_CORS_ORIGINS:
        server.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    server.add_event_handler("startup", start_app_handler(server))
    server.add_event_handler("shutdown", stop_app_handler(server))

    server.include_router(api_router, prefix=settings.API_V1_STR)
    return server


app = get_app()
