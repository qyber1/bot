import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .base import metadata


def create_asyncengine(url) -> AsyncEngine:
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


async def proseed_schemas(engine: AsyncEngine, metadata=metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


def session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)
