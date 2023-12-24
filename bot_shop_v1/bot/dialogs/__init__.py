from aiogram import Dispatcher
from bot.dialogs.windows.config import ConfigDLG
from bot.dialogs.windows.menu import MenuDLG
from bot.dialogs.windows.payment import PaymentDLG
from bot.dialogs.windows.shop import ShopDLG
from bot.dialogs.windows.start import StartDLG


def include_dialogs(dp: Dispatcher):
    dp.include_router(StartDLG)
    dp.include_router(MenuDLG)
    dp.include_router(ShopDLG)
    dp.include_router(ConfigDLG)
    dp.include_router(PaymentDLG)
