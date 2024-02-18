import uuid
from datetime import datetime

from sqlalchemy import (Column, Integer,
                        String, DateTime,
                        Boolean, ForeignKey)
from sqlalchemy.types import UUID

from .base import Base


class File(Base):
    '''Модель таблицы для хранения информации о загруженных файлах'''
    __tablename__ = 'file'

    id = Column(UUID, primary_key=True, default=uuid.uuid1)
    name = Column(String(50))
    created_ad = Column(DateTime, index=True, default=datetime.utcnow)
    path = Column(String(100), unique=True, nullable=False)
    size = Column(Integer)
    is_downloadable = Column(Boolean, default=True)
    owner = Column(ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "File(name='%s')" % (self.name,)
