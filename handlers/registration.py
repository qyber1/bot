import datetime

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import  CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup



from aiogram.fsm.context import FSMContext
from handlers.state import FSMHandler

from sqlalchemy.orm import sessionmaker

from utils.db import get_departaments, get_current_departament, add_employer
from utils.keyboard.keyboards import get_departament
from filters.registration_filter import DepartamentFilter


router = Router()

APPLY = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text='Подтвердить', callback_data='apply')
    ], [
        InlineKeyboardButton(text='Отмена', callback_data='cancel')
    ]
])

REG = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Регистрация', callback_data='registration')
        ]
    ]
)



WORK = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Начать', callback_data='go')
        ],
    ]
)


@router.message(Command(commands=['start']))
async def commands_start(message: Message, db_pool: sessionmaker):
    await message.answer(f"Добро пожаловать! Для дальнейшего пользования необходимо зарегистрироваться: ",
                         parse_mode='HTML',
                         reply_markup=REG)
    # user = await get_user(db_pool, message.from_user.id)
    # if user:
    #     await message.answer(f'<code>Приветствую, {user}</code>',
    #                          parse_mode='HTML',
    #                          reply_markup=WORK)
    #else:



@router.callback_query(F.data == 'registration')
async def registration_handler(call: CallbackQuery, db_pool: sessionmaker):
    args = await get_departaments(db_pool)
    await call.message.edit_text(f'Отлично, выберите отдел в котором Вы работаете: ',
                                 parse_mode='HTML',
                                 reply_markup=get_departament(args))


@router.callback_query(DepartamentFilter())
async def choice_departament(call: CallbackQuery,db_pool: sessionmaker, state: FSMContext):
    departament = await get_current_departament(db_pool, call.data)
    print(departament)
    await state.set_data({'departament': departament})
    await state.set_state(FSMHandler.get_name)
    await call.message.edit_text(f'Введите ФИО: ',
                                 parse_mode='HTML',
                                 )


@router.message(StateFilter(FSMHandler.get_name))
async def get_full_name(msg: Message, state: FSMContext):
    # await new_user(db_pool, msg.from_user.id, msg.text.title())
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
                     f'Отдел: {name["departament"][0][-1]}\n'
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
        await add_employer(db_pool, full_info)
        await call.message.edit_text('Данные сохранены!',
                                     reply_markup=WORK)

# @router.message(FSMHandler.add_task)
# async def echo(message: tpes.Message, state: FSMContext, db_pool: sessionmaker):
#     '''Функция для добавления задач на день. Если в условии есть слово "стоп" то выходит из функции,иначе повторный вызов функции'''
#     if message.text.lower() == 'стоп':
#         await state.clear()
#         await message.answer(f'<code>Задачи добавлены.\nВведите </code> /show <code> чтобы показать список дел </code>',
#                              parse_mode='HTML')
#     else:
#         await add_action(db_pool, message.text, message.from_user.id)
#         await message.answer('<code>Задача добавлена.\nВведи следующую...</code>', parse_mode='HTML')
#         return echo
#
#
# @router.message(Command(commands=['delete']))
# async def deletetask(message: types.Message, state: FSMContext, db_pool: sessionmaker):
#     '''Функция для перехода к функции удалению задач через состояние и команду delete'''
#     action = await delete_actions(db_pool, message.from_user.id)
#     if action:
#         await state.set_state(FSMHandler.delete_task)
#         await message.answer(
#             '<code>Введите выполненную задачу для удаления. \nДля остановки введите слово "стоп"</code>',
#             parse_mode='HTML')
#     else:
#         await message.answer('<code>Нет задач. Для добавления нажмите</code> /add', parse_mode='HTML')
#
#
# @router.message(FSMHandler.delete_task)
# async def edit(message: types.Message, state: FSMContext, db_pool: sessionmaker):
#     '''Функция для редактирования задач'''
#     if message.text.lower() == 'стоп':
#         await state.clear()
#         await message.answer(f'<code>Задачи отредактированы.</code>', parse_mode='HTML')
#
#     else:
#         action = await check_action(db_pool, message.text.lower(), message.from_user.id)
#         if isinstance(action, str):
#             await delete_action(db_pool, action, message.from_user.id)
#             action = await get_all_action(db_pool, message.from_user.id)
#             if isinstance(action, str):
#                 await message.answer('<code>Задача удалена!\nВведи следующую...</code>', parse_mode='HTML')
#                 return edit
#             else:
#                 await state.clear()
#                 await message.answer('<code>Задач больше нет. Поздравляю!</code>', parse_mode='HTML')
#         elif isinstance(action, type(None)):
#             await message.answer('<code>Такой задачи нет в списке. Введите ещё раз...</code>',
#                                          parse_mode='HTML')
#             return edit
#
#
# @router.message(Command(commands=['show']))
# async def show_task(message: types.Message, db_pool: sessionmaker):
#     '''Функия для показа текущих дел.'''
#     list_action = []
#     actions = await show_action(db_pool, message.from_user.id)
#     print(actions)
#     for action in actions:
#         list_action.append(action[0])
#         output_action = '\n'.join(list_action)
#     if list_action:
#         await message.answer(f'<code>Твои задачи на день:</code> \n\n{output_action}', parse_mode='HTML')
#     else:
#         await message.answer(f'<code>Задач нет!</code>', parse_mode='HTML')
#
#
# @router.message(Command(commands=['help']))
# async def help(message: types.Message):
#     await message.answer(
#         "<code>Этот бот помогает добавлять и уследить за своими задачами на день. Таким образом вы будете более эффективными\n\n"
#         "Для того, чтобы добавить задачу - нажмите</code> /add <code>\n\n"
#         "Для того, чтобы удалить выполненную задачу - нажмите</code> /delete <code>\n\n"
#         "Для того, чтобы показать список текущих дел - нажмите </code> /show <code>\n\n"
#         "Спасибо Андрюхе за помощь в разработке</code>", parse_mode='HTML')
#
#
# @router.message()
# async def repeat_msg(message: types.Message):
#     '''Функция повторюшка, если чел не ввел команду'''
#     await message.answer(f'Ты написал - {message.text}.\n Я не понимаю, что нужно делать.\n Введи /help',
#                          parse_mode='HTML')
