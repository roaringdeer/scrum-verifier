from fastapi import Depends, APIRouter, HTTPException, Path, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST, 
    HTTP_401_UNAUTHORIZED, 
    HTTP_404_NOT_FOUND, 
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user
from app.models.users import UserCreate, UserPublic, UserInDB, UserUpdate
from app.models.token import AccessToken
from app.db.repositories.users import UsersRepository
from app.services import auth_service

router = APIRouter()

@router.post('/', response_model=UserPublic, name='users:register-new-user', status_code=HTTP_201_CREATED)
async def register_new_user(
    new_user: UserCreate = Body(..., embed=True),
    user_repository: UsersRepository = Depends(get_repository(UsersRepository))
) -> UserPublic:
    created_user = await user_repository.register_new_user(new_user=new_user)

    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=created_user),
        token_type='bearer'
    )
    
    return UserPublic(**created_user.dict(), access_token=access_token)

@router.post('/login/token/', response_model=AccessToken, name='users:login-email-and-password')
async def user_login_with_email_password(
    user_repository: UsersRepository = Depends(get_repository(UsersRepository)),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
) -> AccessToken:
    user = await user_repository.authenticate_user(email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Authentication wasn\'t successful.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=user),
        token_type='bearer'
    )

    return access_token

@router.get('/me/', response_model=UserPublic, name='users:get-current-user')
async def get_currently_authenticated_user(current_user: UserInDB = Depends(get_current_active_user)) -> UserPublic:
    return current_user

@router.put('/me/', response_model=UserPublic, name='users:update-current-user')
async def update_currently_authenticated_user(
    user_repository: UsersRepository = Depends(get_repository(UsersRepository)),
    current_user: UserInDB = Depends(get_current_active_user),
    user_update: UserUpdate = Body(..., embed=True)
) -> UserPublic:
    return await user_repository.update_user(user_update=user_update, requesting_user=current_user)

@router.delete('/me/', response_model=UserPublic, name='users:update-current-user')
async def deactivate_currently_authenticated_user(
    user_repository: UsersRepository = Depends(get_repository(UsersRepository)),
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserPublic:
    return await user_repository.deactivate_user(requesting_user=current_user)