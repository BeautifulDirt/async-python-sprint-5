import aioredis

from core.config import app_settings

# получение сессии подключения к Redis
redis = aioredis.from_url(url=app_settings.redis_dsn)
