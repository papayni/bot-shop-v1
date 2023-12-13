import asyncio
from aiogram import Bot
from coloredlogs import logging


async def print_info(bot: Bot, settings, tortoise_config: dict):
    bot_info = await bot.get_me()
    logging.info(f'''
    [AIOGRAM BOT]
    name: {bot_info.full_name}
    username: @{bot_info.username}
    id: {bot_info.id}
    [WEBHOOK]
    url: {settings().WEBHOOK}/{settings().WEBHOOK_PATH}
    [DATABASE]
    models: {tortoise_config['apps']['models']['models']}
    db_protocol: {settings().DB_PROTOCCOL}
    sqlite directory: {settings().SQLITE_DIR}
    [EVENTLOOP]
    {asyncio.get_event_loop()}
    ''')
