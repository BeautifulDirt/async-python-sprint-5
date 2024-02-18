from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class FileBase(BaseModel):
    name: str


class FileCreate(FileBase):
    owner: UUID
    path: str
    size: int


class FileUpdate(FileCreate):
    pass


class FileInDBBase(FileBase):
    id: UUID
    name: str
    created_ad: datetime
    path: str
    size: int
    is_downloadable: bool

    class Config:
        from_attributes = True


class FileSchemas(FileInDBBase):
    pass
