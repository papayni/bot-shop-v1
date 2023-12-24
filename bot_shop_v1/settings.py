from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')
    TOKEN: str
    WEBHOOK: str = ''
    WEBHOOK_PATH: str = ''
    DB_PROTOCCOL: str = 'sqlite'
    SQLITE_DIR: str = 'bot.db'


@lru_cache()
def settings():
    return Settings()
