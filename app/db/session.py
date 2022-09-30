from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import settings


engine = create_async_engine(
    url=settings.SQLALCHEMY_POSTGRES_URI,
    echo=True,
    future=True,
    pool_pre_ping=True,
)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


SessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
