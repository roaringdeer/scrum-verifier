from typing import List, Union
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status, File, UploadFile
from fastapi.responses import FileResponse
from app.models.users import UserInDB
from app.models.profiles import ProfileUpdate
from app.api.dependencies.authentication import get_current_active_user
from app.api.dependencies.users import get_repository
from app.db.repositories.profiles import ProfilesRepository
import os

router = APIRouter()

@router.post('/')
async def create_upload_file(
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_active_user)
):  
    if not os.path.isdir(f'/files/'):
        os.mkdir(f'/files/')
    if not os.path.isdir(f'/files/{current_user.id}/'):
        os.mkdir(f'/files/{current_user.id}/')
    file_location = f"/files/{current_user.id}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {'filename': file.filename}

@router.post('/avatar/')
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_active_user),
    profiles_repo: ProfilesRepository = Depends(get_repository(ProfilesRepository))
):  
    if not os.path.isdir(f'/files/'):
        os.mkdir(f'/files/')
    if not os.path.isdir(f'/files/avatar/'):
        os.mkdir(f'/files/avatar/')
    file_location = f"/files/avatar/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    await profiles_repo.update_profile(profile_update=ProfileUpdate(image=file.filename), requesting_user=current_user)
    return {'filename': file.filename}

@router.get('/')
async def get_user_filenames(
    current_user: UserInDB = Depends(get_current_active_user)
):
    listOfFiles = os.listdir(f'/files/{current_user.id}/')
    return listOfFiles

@router.get('/{filename}')
async def get_file(
    filename: str = Path(...),
):
    if filename in os.listdir(f'/files/avatar/'):
        return FileResponse(f'/files/avatar/{filename}')   
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Can\'t find this file.'
            )
        # raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail='Can\'t access other peoples files.'
        #     )
