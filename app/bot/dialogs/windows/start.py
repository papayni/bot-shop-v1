from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format

from app.bot.states import StartSG


unregistred_users = Window(
    Format('Welcome'),
    state=StartSG.registred,
)
registred_users = Window(
    Format('Welcome back'),
    state=StartSG.unregistred,
)

StartDLG = Dialog(unregistred_users, registred_users)
