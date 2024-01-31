import datetime

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message



from aiogram.fsm.context import FSMContext
from handlers.state import FSMHandler

from sqlalchemy.orm import sessionmaker

from utils.db import get_user, get_departments, get_current_departament, add_employer
from utils.keyboard import get_departament, REG, WORK, APPLY
from filters.registration_filter import DepartamentFilter


router = Router()


@router.message(Command(commands=['start']))
async def commands_start(message: Message, db_pool: sessionmaker):
    if await get_user(db_pool, message.from_user.id):
        await message.answer('Добро пожаловать', reply_markup=WORK)
    else:
        await message.answer(f"Добро пожаловать! Для дальнейшего пользования необходимо зарегистрироваться: ",
                         parse_mode='HTML',
                         reply_markup=REG)


@router.callback_query(F.data.in_(['not_start_day', 'not_finish_day']))
async def main_menu(call: CallbackQuery):
    await call.message.edit_text('Добро пожаловать', reply_markup=WORK)



@router.callback_query(F.data == 'registration')
async def registration_handler(call: CallbackQuery, db_pool: sessionmaker):
    args = await get_departments(db_pool)
    await call.message.edit_text(f'Отлично, выберите отдел в котором Вы работаете: ',
                                 parse_mode='HTML',
                                 reply_markup=get_departament(args))


@router.callback_query(DepartamentFilter())
async def choice_departament(call: CallbackQuery, db_pool: sessionmaker, state: FSMContext):
    department = await get_current_departament(db_pool, call.data)
    print(department)
    await state.set_data({'department': department})
    await state.set_state(FSMHandler.get_name)
    await call.message.edit_text(f'Введите ФИО: ',
                                 parse_mode='HTML',
                                 )


@router.message(StateFilter(FSMHandler.get_name))
async def get_full_name(msg: Message, state: FSMContext):
    name = msg.text.title()
    await state.update_data({'name': name})
    await state.set_state(FSMHandler.get_job_title)
    await msg.answer(f'Рады видеть Вас в команде, {" ".join(name.split()[1:])}! Теперь введите должность: ')


@router.message(StateFilter(FSMHandler.get_job_title))
async def get_job_title(msg: Message, state: FSMContext):
    name = await state.get_data()
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    await state.update_data({'date': date,
                             'job_title': msg.text.capitalize()})
    await msg.answer('Карточка сотрудника:\n'
                     f'ФИО: {"".join(name["name"])}\n'
                     f'Отдел: {name["department"][0][-1]}\n'
                     f'Должность: {msg.text.capitalize()}\n'
                     f'Дата приема на работу: {date}',
                     reply_markup=APPLY)

@router.callback_query(F.data.in_(['apply', 'cancel']))
async def switch(call: CallbackQuery, state: FSMContext, db_pool: sessionmaker):
    if call.data == "cancel":
        await call.message.edit_text('Отмена... Начинаем регистрацию заново', reply_markup=REG)
        await state.clear()
    else:
        full_info = await state.get_data()
        await add_employer(db_pool, full_info, call.from_user.id)
        await call.message.edit_text('Данные сохранены!',
                                     reply_markup=WORK)
