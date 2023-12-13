from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager


handlers_router = Router()


@handlers_router.message(CommandStart())
async def handle_start(message: Message, dialog_manager: DialogManager):
    ...
