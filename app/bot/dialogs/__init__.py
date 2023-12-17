from aiogram import Dispatcher
from bot.dialogs.windows.menu import MenuDLG

from bot.dialogs.windows.start import StartDLG


def include_dialogs(dp: Dispatcher):
    dp.include_router(StartDLG)
    dp.include_router(MenuDLG)
