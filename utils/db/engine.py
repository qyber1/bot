from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .models import BaseModel, UserAdmin


async def proseed_schemas(engine: AsyncEngine, metadata=BaseModel.metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

        async with AsyncSession(bind=conn) as session:
            async with session.begin():
                user_admin = UserAdmin()
                session.add(user_admin)


def session_maker(engine: AsyncEngine) -> sessionmaker:
    sessionmaker(engine, class_=AsyncSession)


class DBConnect:

     def __init__(self, url):
        self.engine = create_async_engine(url=url, echo=True, pool_pre_ping=True)


def get_engine(url):
    db = DBConnect(url)
    return db