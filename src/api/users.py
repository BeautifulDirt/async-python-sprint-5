import logging

from jose import jwt

from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import app_settings
from core.oauth_util import get_password_hash, verify_password
from schemas.users import UserCreate, UserSchemas, UserLogin
from services.users import user_rep
from db.db import get_session
from db.redis import redis
from models.user import User


router = APIRouter()


@router.post('/register',
             response_model=UserSchemas, tags=["users"],
             status_code=status.HTTP_201_CREATED)
async def register_user(
        data: UserCreate,
        db: AsyncSession = Depends(get_session),
) -> HTTPException | dict:
    '''Регистрация нового пользователя'''
    logging.info('Register new user %s', data.username)
    data.password = get_password_hash(data.password)
    user_db = await user_rep.get(db, User.username == data.username)
    if user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='User already exists')
    res = await user_rep.create(db, obj_in=data)
    return res


@router.post('/auth', tags=["users"],
             response_model=UserLogin, status_code=status.HTTP_201_CREATED)
async def auth_user(
        data: UserLogin,
        db: AsyncSession = Depends(get_session),
) -> HTTPException | str:
    '''Авторизация пользователя'''
    logging.info('User auth %s', data.username)
    user_db = await user_rep.get(
        db, (User.username == data.username)
    )
    if not user_db and verify_password(user_db.password, data.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Wrong username/password')

    token = jwt.encode(
        {
            'id': str(user_db.id_user)
        },
        app_settings.secret_key,
        app_settings.algorithm
    )

    await redis.setex(name=token, value=user_db.username)

    return token
