from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format

from bot.states import MenuSG, StartSG


unregistred_users = Window(
    # StaticMedia(),
    Format('Welcome'),
    state=StartSG.registred,
)
registred_users = Window(
    # StaticMedia(),
    Format('Welcome back'),
    Start(text=Format('Main menu'), id='main_menu', state=MenuSG.main_menu),
    state=StartSG.unregistred,
)

StartDLG = Dialog(unregistred_users, registred_users)
