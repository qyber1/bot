from sqlalchemy import select, delete
from sqlalchemy.orm import sessionmaker

from db.models import User, Todo


async def get_user(db_pool: sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            user = await session.execute(select(User).where(User.id == user_id))
            return user.scalar()


async def new_user(db_pool: sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            new_user = User(id=user_id)
            return session.add(new_user)


async def add_action(db_pool: sessionmaker, action: str, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            action = Todo(action=action.lower(), parent_id=user_id)
            return session.add(action)


async def delete_actions(db_pool: sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            actions = await session.execute(
                select(Todo.action).join(User).where(Todo.parent_id == user_id))
            return actions.scalar()


async def show_action(db_pool: sessionmaker, user_id: int):
    async with db_pool() as session:
        async with session.begin():
            actions = await session.execute(select(Todo.action).where(Todo.parent_id == user_id))
            return actions.fetchall()


async def check_action(db_pool:sessionmaker, action: str, user_id: int) -> str:
    async with db_pool() as session:
        async with session.begin():
            actions = await session.execute(select(Todo.action).join(User).where(
                Todo.action == action.lower()).where(
                Todo.parent_id == user_id))
            action = actions.scalar()
            return action

async def delete_action(db_pool: sessionmaker, action: str,user_id: int) -> None:
    async with db_pool() as session:
        async with session.begin():
            await session.execute(delete(Todo).where(Todo.action == action).where(Todo.parent_id == user_id))
            await session.commit()

async def get_all_action(db_pool: sessionmaker, user_id: int) -> str:
    async with db_pool() as session:
        async with session.begin():
            actions = await session.execute(select(Todo.action).join(User).where(
                Todo.parent_id == user_id))
            action = actions.scalar()
            return action