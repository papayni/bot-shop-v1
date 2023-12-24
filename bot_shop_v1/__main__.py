import asyncio
import logging

import coloredlogs
import uvloop
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler,
                                            setup_application)
from aiogram_dialog import setup_dialogs
from aiohttp import web
from bot.dialogs import include_dialogs
from bot.handlers import include_routers
from database import (close_orm, create_models, generate_config, init_orm,
                      migrate_models)
from settings import settings
from utils.print_info import print_info


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logging.warning('Starting bot...')
    tortoise_config = generate_config()
    try:
        await create_models(tortoise_config)
    except FileExistsError:
        await migrate_models(tortoise_config)
    include_routers(dispatcher)
    include_dialogs(dispatcher)
    await init_orm(tortoise_config)
    await bot.set_webhook(f'{settings().WEBHOOK}/{settings().WEBHOOK_PATH}')
    await print_info(bot=bot, settings=settings, tortoise_config=tortoise_config)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.warning('Stopping bot...')
    await dispatcher.fsm.storage.close()
    await bot.session.close()
    await close_orm()


def main():
    coloredlogs.install(level=logging.INFO)
    bot = Bot(token=settings().TOKEN, parse_mode='HTML')
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    app = web.Application()
    webhooh_request_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhooh_request_handler.register(app, path=settings().WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    setup_dialogs(dp)
    web.run_app(app, host='127.0.0.1', port=8000)


if __name__ == "__main__":
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
