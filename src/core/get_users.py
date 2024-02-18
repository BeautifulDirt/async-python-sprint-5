import logging

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from schemas.users import UserAuth
from db.redis import redis
from core.config import app_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> HTTPException | UserAuth:
    '''Получение текущего пользователя'''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authorization required",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = await redis.get(token)
        payload = jwt.decode(token,
                             app_settings.JWT_SECRET,
                             algorithms=[app_settings.JWT_ALGORITHM])
        id_user: str = payload.get("id")
        if username is None or id_user is None:
            raise credentials_exception
    except JWTError as e:
        logging.critical(str(e))
        raise credentials_exception

    return UserAuth(username=username, id_user=id_user)
