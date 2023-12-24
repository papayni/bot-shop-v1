import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import ErrorEvent, Message
from aiogram_dialog import DialogManager
from bot.states import StartSG
from database.models.user import User

handlers_router = Router()


@handlers_router.message(CommandStart())
async def handle_start(message: Message, dialog_manager: DialogManager):
    if message.from_user:
        user = await User.get_or_create(telegram_id=message.from_user.id)
        if user[1]:
            await dialog_manager.start(state=StartSG.registred)
        else:
            await dialog_manager.start(state=StartSG.unregistred)

        # u = await User.filter(telegram_id=message.from_user.id).prefetch_related('orders')
        # p = await Product.get(id=1)
        # o = await Order(user_id=u[0].id)
        # await o.save()
        # await o.products.add(p)
        # print(u[0].orders)


@handlers_router.error()
async def handle_errors(event: ErrorEvent):
    logging.critical("Critical error caused by %s",
                     event.exception, exc_info=True)
