from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_departament(items: list[list[str]]):
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(InlineKeyboardButton(
            text=f"{item[-1]}",
            callback_data=f"{item[0]}"
        ))
    return builder.adjust(1).as_markup()


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


START_MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Начать рабочий день', callback_data='start_work')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='not_start_day')
        ]
    ]
)


END_MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Закончить рабочий день', callback_data='end_work')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='not_finish_day')
        ]
    ]
)