from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from .db import RepositoryDB
from models.file import File
from schemas.files import FileCreate, FileUpdate


class RepositoryFile(RepositoryDB[File, FileCreate, FileUpdate]):

    async def get_file_path(
            self,
            db: AsyncSession,
            id_file: UUID
    ) -> str | None:
        statement = select(self._model).where(File.id_file == id_file)
        result = (await db.execute(statement=statement)).scalar_one_or_none()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='File not found')
        return result.path


file_rep = RepositoryFile(File)
