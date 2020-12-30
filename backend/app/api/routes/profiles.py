import os
from fastapi import APIRouter, Path, Body, Depends, HTTPException, status, File, UploadFile
from app.api.dependencies.authentication import get_current_active_user
from fastapi.responses import FileResponse
from app.api.dependencies.database import get_repository
from app.db.repositories.profiles import ProfilesRepository
from app.models.users import UserInDB
from app.models.profiles import ProfileUpdate, ProfilePublic

router = APIRouter()

@router.get('/{username}/', response_model=ProfilePublic, name='profiles:get-profile-by-username')
async def get_profile_by_username(
    username: str = Path(..., min_length=3, regex='[a-zA-Z0-9_-]+$'),
    current_user: UserInDB = Depends(get_current_active_user),
    profiles_repository: ProfilesRepository = Depends(get_repository(ProfilesRepository))
) -> ProfilePublic:
    profile = await profiles_repository.get_profile_by_username(username=username)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No profile found with that username.'
        )
    return profile

@router.put('/me/', response_model=ProfilePublic, name='profiles:update-own-profile')
async def update_own_profile(
    profile_update: ProfileUpdate = Body(..., embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    profiles_repository: ProfilesRepository = Depends(get_repository(ProfilesRepository))
) -> ProfilePublic:
    updated_profile = await profiles_repository.update_profile(profile_update=profile_update, requesting_user=current_user)
    return updated_profile

@router.put('/me/avatar', name='profiles:update-own-avatar')
async def update_own_avatar(
    uploaded_image: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_active_user),
    profiles_repository: ProfilesRepository = Depends(get_repository(ProfilesRepository))
) -> ProfilePublic:
## ENFORCE DRY
    if uploaded_image.filename.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Upload JPG or PNG image.'
        )
    if not os.path.isdir(f'/files/'):
        os.mkdir(f'/files/')
    if not os.path.isdir(f'/files/avatars/'):
        os.mkdir(f'/files/avatars/')
    file_location = f"/files/avatars/{uploaded_image.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_image.file.read())
    updated_profile = await profiles_repository.update_profile(
        profile_update=ProfileUpdate(image=f'http://localhost:8000/api/files/{uploaded_image.filename}'),
        requesting_user=current_user
    )
    return updated_profile