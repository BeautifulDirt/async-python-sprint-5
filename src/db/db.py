from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.config import app_settings


# создание движка и настройка подключения к БД
engine = create_async_engine(app_settings.database_dsn.unicode_string(),
                             echo=app_settings.echo,
                             future=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# получение сессии подключения к БД
async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
