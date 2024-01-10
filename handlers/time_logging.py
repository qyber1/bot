import time
from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.keyboard import CONTROL_MENU


router = Router()


@router.callback_query(F.data == 'go')
async def start_logging_time(call: CallbackQuery):
    await call.message.edit_text('Добро пожаловать в меню управления',
                                 reply_markup=CONTROL_MENU)


@router.callback_query(F.data.in_(['start_work', 'end_work']))
async def counter_time(call:CallbackQuery):
    if call.data == 'start_work':
        global start
        start = time.time()
        await call.message.edit_text('Вы начали рабочий день')
    elif call.data == "end_work":
        end = time.time()
        await call.message.edit_text(f'Вы закончили рабочий день. Вы проработал: {time.strftime("%H:%M:%S",time.gmtime(end - start))}')