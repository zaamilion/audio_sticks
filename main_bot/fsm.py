from aiogram.fsm.state import StatesGroup, State

class creating_bot(StatesGroup):
    tarif = State()
    token = State()