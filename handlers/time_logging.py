from datetime import datetime
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from handlers.state import FinishDay

from utils.db import get_full_info, start_work_day,get_worklog_id, finish_work_day ,validate_work_day
from utils.keyboard import START_MENU, END_MENU
from main import bot

router = Router()

@router.callback_query(F.data == 'go')
async def start_logging_time(call: CallbackQuery, db_pool: sessionmaker):
    current_date = await validate_work_day(db_pool, call.from_user.id)
    print(current_date)
    if current_date:
        if current_date[0][0] == datetime.now().date():
            if current_date[0][1] is None:
                await call.message.edit_text(f'Добро пожаловать в меню управления. Рабочий день уже идет. Завершить рабочий день?',
                                 reply_markup=END_MENU)
            else:
                await call.message.edit_text(f'Рабочий день закончен! До завтра')
        else:
            await call.message.edit_text(
            f'Добро пожаловать в меню управления. Рабочий день ещё не начался. Начать рабочий день?',
            reply_markup=START_MENU)


@router.callback_query(F.data == 'start_work')
async def start_day(call: CallbackQuery, db_pool: sessionmaker):
    start_day = datetime.now().hour
    name = await get_full_info(db_pool, call.from_user.id)
    await start_work_day(db_pool, call.from_user.id)
    if start_day >= 11:
        await call.message.edit_text('Вы опоздали на работу!')
        await bot.send_message(chat_id=-1002059090185, text=f'Сотрудник - {name} опоздал на работу!\nПриступил к работе {datetime.now().strftime("%d.%m.%y в %H:%M")}!')
    else:
        await call.message.edit_text('Рабочий день начался!')
        await bot.send_message(chat_id=-1002059090185, text=f'Сотрудник - {name} приступил к работе {datetime.now().strftime("%d.%m.%y в %H:%M")}! ')


@router.callback_query(F.data == 'end_work')
async def get_info_about_day(call: CallbackQuery, db_pool: sessionmaker, state: FSMContext):
    id = await get_worklog_id(db_pool, call.from_user.id)
    name = await get_full_info(db_pool, call.from_user.id)
    await state.set_state(FinishDay.get_info)
    await state.set_data({"id": id,
                          "name": name})
    await call.message.edit_text('Введите комментарий о рабочем дне:')


@router.message(StateFilter(FinishDay.get_info))
async def finish_day(msg: Message, db_pool:sessionmaker, state: FSMContext):
    info = await state.get_data()
    await finish_work_day(db_pool, info["id"], msg.text)
    print(msg.text)
    await msg.answer('Рабочий день закончен!')
    await bot.send_message(chat_id=-1002059090185,
                           text=f'Сотрудник - {info["name"]} закончил рабочий день!')
    await state.clear()