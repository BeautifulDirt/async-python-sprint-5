import logging
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

from .logger import LOGGING

# настройка логгера
logging.config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    # настройка проекта
    project_name: str
    project_host: str
    project_port: int
    project_description: str
    project_summary: str
    project_version: str
    secret_key: str
    algorithm: str

    database_dsn: PostgresDsn
    database_user: str
    database_password: str
    database_name: str
    database_port: int
    database_host: str
    echo: bool

    redis_dsn: str
    redis_host: str
    redis_port: int
    redis_password: str

    upload_folder: str
    max_file_size: int

    class Config:
        env_file = '.env'


app_settings = AppSettings()
