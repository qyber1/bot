from datetime import datetime

from sqlalchemy import select, delete, update
from sqlalchemy.orm import sessionmaker

from utils.db.models import User, Department, Worklog


async def get_user(db_pool: sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            user = await session.execute(select(User.id).where(User.id == user_id))
            if user.scalar():
                return True
            else:
                return False


async def get_full_info(db_pool:sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            user = await session.execute(select(User.username).where(User.id == user_id))
            return user.scalar()


async def get_departments(db_pool: sessionmaker):
    async with db_pool() as session:
        async with session.begin():
            user = await session.execute(select(Department.id, Department.title))
            print(f'{user=}')
            return user.fetchall()


async def get_current_departament(db_pool: sessionmaker, dep_id: int):
    async with db_pool() as session:
        async with session.begin():
            depo = await session.execute(select(Department.id, Department.title).where(Department.id == int(dep_id)))
            return depo.fetchall()


async def add_employer(db_pool: sessionmaker, data: dict, id: int):
    async with db_pool() as session:
        async with session.begin():
            user = User(id=id,
                        username=data['name'],
                        job_title=data['job_title'],
                        department_id=data['department'][0][0])
            return session.add(user)


async def start_work_day(db_pool: sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            worklog = Worklog(
                start_time=datetime.now().time(),
                date=datetime.now().date(),
                user_id=user_id
            )
            return session.add(worklog)



async def get_worklog_id(db_pool: sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            id = await session.execute(select(Worklog.id).where(Worklog.user_id == user_id).order_by(Worklog.date.desc()))
            return id.scalar()


async def finish_work_day(db_pool: sessionmaker, worklog_id, text: str):
    async with db_pool() as session:
        async with session.begin():
            stmt = update(Worklog).where(Worklog.id == worklog_id).values(
                end_time=datetime.now().time(),
                comment=text
            )
            await session.execute(stmt)


async def validate_work_day(db_pool: sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            current_date = await session.execute(select(Worklog.date, Worklog.end_time).where(Worklog.user_id == user_id).order_by(Worklog.date.desc()).limit(1))
            return current_date.all()