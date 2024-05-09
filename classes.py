from aiogram.fsm.state import StatesGroup, State

class get_voice(StatesGroup):
    audio = State()

class delete_voice(StatesGroup):
    id = State()
    confirm = State()