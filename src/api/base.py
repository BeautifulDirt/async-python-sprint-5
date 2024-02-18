import time
from typing import Annotated
from fastapi import APIRouter, Depends

from db.redis import redis
from db.db import get_session, AsyncSession
from core.config import logging
from schemas import ping as schema_ping


router = APIRouter()


@router.get('/ping', tags=["ping"], response_model=schema_ping.PingDb)
async def ping(
    *,
    db: Annotated[AsyncSession, Depends(get_session)],
) -> dict:
    '''Проверка доступности БД'''

    redis_ping = db_ping = 'No access'

    try:
        start = time.time()
        conn_redis = await redis.ping()
        finish_time = time.time() - start
        if conn_redis:
            logging.info('Redis coonection has access!')
            redis_ping = '{:.5f}'.format(finish_time)
    except Exception:
        logging.warning('Redis coonection has no access!')

    try:
        start = time.time()
        conn_db = await db.connection()
        finish_time = time.time() - start
        if conn_db:
            logging.info('Postgres access established!')
            db_ping = '{:.2f}'.format(finish_time)
    except Exception:
        logging.info('Postgres access no established!')

    logging.warning('Postgres - %s, Redis - %s', db_ping, redis_ping)
    return {
        'postgres': db_ping,
        'redis': redis_ping
    }
