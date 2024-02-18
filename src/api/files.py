import logging
import os
import uuid
from pathlib import Path

from fastapi import Depends, APIRouter, UploadFile, status, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles

from schemas.files import FileCreate, FileSchemas, FileBase
from schemas.users import UserAuth
from services.files import file_rep
from db.db import get_session
from core.get_users import get_current_user
from models.file import File
from core.config import app_settings


router = APIRouter(prefix='/files')


@router.post('/upload', tags=["files"],
             response_model=FileSchemas,
             status_code=status.HTTP_201_CREATED)
async def upload_file(
        path: str,
        file: UploadFile,
        db: AsyncSession = Depends(get_session),
        user: UserAuth = Depends(get_current_user),
) -> HTTPException | dict:
    '''Загрузка файла в файловое хранище'''

    logging.info('Uploading file by user %s, path %s', user.username, path)

    if file.size > app_settings.max_file_size:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='File is too big')

    p = Path('.')
    path = path.strip('/')
    local_path = os.path.join(app_settings.upload_folder,
                              str(user.id_user),
                              path)

    is_file = '.' in path.split('/')[-1]
    name = file.filename
    if is_file:
        name = path.split('/')[-1]
        p = p / local_path[: path.rfind('/')]
    else:
        p = p / path
        path = os.path.join(path, name)

    p.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)

    obj_in = FileCreate(
        id_user=user.id_user,
        name=name,
        size=file.size,
        path=path
    )

    res = await file_rep.create(db, obj_in=obj_in)
    return res


@router.get('/download/{path_or_id_file:path}', tags=["files"],
            response_model=FileBase)
async def download_file(
    path_or_id_file: str,
    db: AsyncSession = Depends(get_session),
    user: UserAuth = Depends(get_current_user),
) -> HTTPException | FileResponse:
    '''Выгрузка файла из файловое хранище'''

    logging.info('Accessing to file by path %s', path_or_id_file)
    file_not_found_exc = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                       detail='File not found')

    p = Path('.') / app_settings.upload_folder \
        / str(user.id_user) / path_or_id_file
    if p.exists():
        return FileResponse(str(p))

    id_file = path_or_id_file
    logging.info('Accessing to file by id %s', id_file)
    try:
        file_uuid = uuid.UUID(id_file)
    except ValueError:
        raise file_not_found_exc

    file_path = await file_rep.get_file_path(db, file_uuid)

    return FileResponse(file_path)


@router.get('/list', tags=["files"], response_model=list[FileSchemas])
async def get_files(
        db: AsyncSession = Depends(get_session),
        user: UserAuth = Depends(get_current_user),
) -> list:
    '''Выгрузка информации о файлах пользователя'''
    logging.info('Retrieve file info for user %s', user.username)
    return await file_rep.get_multi(db, File.id_user == user.id_user)
