from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from utils.db.engine import get_engine, session_maker
from utils.db.requests import get_departments
from utils.config import DBConfig


class DepartamentFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        args = await get_departments(session_maker(get_engine(DBConfig.url).engine))
        d = callback.data
        if d in [str(item[0]) for item in args]:
            return True
        else:
            return False
