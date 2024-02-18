import uuid

from sqlalchemy import Column, String
from sqlalchemy.types import UUID

from .base import Base


class User(Base):
    '''Модель таблицы для хранения информации о пользователях'''
    __tablename__ = 'user'

    id = Column(UUID, primary_key=True, default=uuid.uuid1)
    username = Column(String(100), unique=True)
    password = Column(String(100), nullable=False)

    def __repr__(self):
        return "User(username='%s')" % (self.username,)
