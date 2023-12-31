import contextlib
from click import Abort
from aerich import Command
from tortoise import Tortoise
from settings import settings

all_models = [
    'aerich.models',
    'database.models.user'
]


def generate_config():
    connection = ''
    if settings().DB_PROTOCCOL == 'sqlite':
        connection = f'{settings().DB_PROTOCCOL}://{settings().SQLITE_DIR}'
    return {
        'connections': {'default': connection},
        'apps': {
            'models': {
                'models': all_models,
                'default_connection': 'default',
            }
        }
    }


async def create_models(tortoise_config: dict):
    command = Command(tortoise_config=tortoise_config, app='models')
    await command.init()


async def migrate_models(tortoise_config: dict):
    command = Command(tortoise_config=tortoise_config, app="models")
    await command.init()
    with contextlib.suppress(Abort):
        await command.migrate()
    await command.upgrade(True)


async def init_orm(tortoise_config: dict) -> None:
    await Tortoise.init(config=tortoise_config)


async def close_orm() -> None:
    await Tortoise.close_connections()
