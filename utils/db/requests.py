from sqlalchemy import select, delete
from sqlalchemy.orm import sessionmaker

from utils.db.models import User, Departament


async def get_user(db_pool: sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            user = await session.execute(select(User.tg_id).where(User.tg_id == user_id))
            if user.scalar():
                return True
            else:
                return False

async def get_full_info(db_pool:sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            user = await session.execute(select(User.username).where(User.tg_id == user_id))
            return user.scalar()
async def get_departaments(db_pool: sessionmaker):
    async with db_pool() as session:
        async with session.begin():
            user = await session.execute(select(Departament.id, Departament.title))
            return user.fetchall()


async def get_current_departament(db_pool: sessionmaker, id: int):
    async with db_pool() as session:
        async with session.begin():
            depo = await session.execute(select(Departament.id, Departament.title).where(Departament.id == int(id)))

            return depo.fetchall()


async def add_employer(db_pool: sessionmaker, data: dict, id: int):
    async with db_pool() as session:
        async with session.begin():
            user = User(tg_id=id,
                        username=data['name'],
                        job_title=data['job_title'],
                        departament_id=data['departament'][0][0])
            return session.add(user)

