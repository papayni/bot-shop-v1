from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    registred = State()
    unregistred = State()


class MenuSG(StatesGroup):
    main_menu = State()
    rules = State()
    profile = State()


class ShopSG(StatesGroup):
    shop = State()
