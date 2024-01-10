import os
import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .base import metadata



async def proseed_schemas(engine: AsyncEngine, metadata=metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


def session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)


class DBConnect:

     def __init__(self, url):
        self.engine = create_async_engine(url=url, echo=True, pool_pre_ping=True)



def get_engine(url):
    db = DBConnect(url)
    return db