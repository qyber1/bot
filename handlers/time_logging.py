from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import sessionmaker

from utils.db import get_full_info
from utils.keyboard import CONTROL_MENU
from main import bot

router = Router()


@router.callback_query(F.data == 'go')
async def start_logging_time(call: CallbackQuery):
    await call.message.edit_text('Добро пожаловать в меню управления',
                                 reply_markup=CONTROL_MENU)


@router.callback_query(F.data == 'start_work')
async def counter_time(call:CallbackQuery, db_pool: sessionmaker):
    start_day = datetime.now().hour
    name = await get_full_info(db_pool, call.from_user.id)
    if start_day >= 22:
        await call.message.edit_text('Вы опоздали на работу!')
        await bot.send_message(chat_id=-1002059090185, text=f'Сотрудник - {name} опоздал на работу!\nПриступил к работе {datetime.now().strftime("%d.%m.%y в %H:%M")}!')
    else:
        await bot.send_message(chat_id=-1002059090185, text=f'Сотрудник - {name} приступил к работе {datetime.now().strftime("%d.%m.%y в %H:%M")}! ')
