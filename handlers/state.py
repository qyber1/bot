from aiogram.filters.state import State, StatesGroupclass FSMHandler(StatesGroup):    '''Класс для добавления состояний'''    add_task = State()    delete_task = State()