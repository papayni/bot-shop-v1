from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    registred = State()
    unregistred = State()


class MenuSG(StatesGroup):
    main_menu = State()
    rules = State()
    profile = State()


class ShopSG(StatesGroup):
    category = State()
    sub_category = State()
    product = State()
    description = State()


class ConfigurationSG(StatesGroup):
    fields = State()
    config = State()
