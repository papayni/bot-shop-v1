from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format
from bot.states import MenuSG, StartSG

unregistred_users = Window(
    StaticMedia(url='https://i.imgur.com/Pg9s73B.jpg'),
    state=StartSG.registred,
)
registred_users = Window(
    StaticMedia(url='https://i.imgur.com/mv95wvN.jpg'),
    Start(text=Format('Main menu'), id='main_menu', state=MenuSG.main_menu),
    state=StartSG.unregistred,
)

StartDLG = Dialog(unregistred_users, registred_users)
