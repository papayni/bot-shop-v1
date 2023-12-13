from aiogram import Dispatcher
from bot.handlers.start import handlers_router


def include_routers(dp: Dispatcher):
    dp.include_router(handlers_router)
