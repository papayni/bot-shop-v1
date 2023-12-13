from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    registred = State()
    unregistred = State()
