from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, close_all_sessions

from app.core.config import settings


async def open_postgres_database_connection(app: FastAPI) -> None:
    engine = create_async_engine(settings.SQLALCHEMY_POSTGRES_URI, echo=True)
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    try:
        print("You have connected to the database")
        app.state._db = async_session
    except Exception as err:
        print(f"ERROR OCCURRED WHILE CONNECTING TO THE DATABASE: {err}")


async def close_postgres_database_connection(app: FastAPI) -> None:
    try:
        close_all_sessions()
        print("DB connection closed")
    except Exception as err:
        print(f"ERROR OCCURRED WHILE CLOSING ALL THE SESSIONS: {err}")
