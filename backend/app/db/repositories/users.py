from pydantic import EmailStr
from typing import Optional
from fastapi import HTTPException, status
from databases import Database
from app.db.repositories.base import BaseRepository
from app.db.repositories.profiles import ProfilesRepository
from app.models.users import UserCreate, UserUpdate, UserInDB
from app.models.profiles import ProfileCreate, ProfilePublic
from app.services import auth_service

GET_USER_BY_ID_QUERY = '''
    SELECT id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE id = :id;
'''

GET_USER_BY_EMAIL_QUERY = '''
    SELECT id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE email = :email;
'''

GET_USER_BY_USERNAME_QUERY = '''
    SELECT id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE username = :username;
'''

REGISTER_NEW_USER_QUERY = '''
    INSERT INTO users (username, email, password, salt)
    VALUES (:username, :email, :password, :salt)
    RETURNING id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at;
'''

UPDATE_USER_USERNAME_QUERY = '''
    UPDATE users
    SET username = :username
    WHERE id = :id;
'''

UPDATE_USER_EMAIL_QUERY = '''
    UPDATE users
    SET email = :email
    WHERE id = :id;
'''

DEACTIVATE_USER_QUERY = '''
    UPDATE users
    SET is_active = 'f'
    WHERE user_id = :user_id
    RETURNING id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at;
'''

class UsersRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db)
        self.auth_service = auth_service
        self.profiles_repository = ProfilesRepository(db)

    async def get_user_by_email(self, *, email: EmailStr, populate: bool = True) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_EMAIL_QUERY, values={'email': email})
        if not user_record:
            return None
        if populate:
            return await self.populate_user(user=UserInDB(**user_record))
        else:
            return UserInDB(**user_record)
    
    async def get_user_by_id(self, *, user_id: int, populate: bool = True) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_ID_QUERY, values={'id': user_id})
        if not user_record:
            return None
        if populate:
            return await self.populate_user(user=UserInDB(**user_record))
        else:
            return UserInDB(**user_record)

    async def get_user_by_username(self, *, username: str, populate: bool = True) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_USERNAME_QUERY, values={'username': username})
        if not user_record:
            return None
        if populate:
            return await self.populate_user(user=UserInDB(**user_record))
        else:
            return UserInDB(**user_record)

    async def register_new_user(self, *, new_user: UserCreate) -> UserInDB:
        if await self.get_user_by_email(email=new_user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='That email is already taken. Login with that email or register with another one.'
            )
        
        if await self.get_user_by_username(username=new_user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='That username is already taken. Please try another one.'                
            )

        user_password_update = self.auth_service.create_salt_and_hashed_password(plaintext_password=new_user.password)
        new_user_params = new_user.copy(update=user_password_update.dict())
        created_user = await self.db.fetch_one(query=REGISTER_NEW_USER_QUERY, values=new_user_params.dict())
        profile = await self.profiles_repository.create_profile_for_user(profile_create=ProfileCreate(user_id=created_user['id']))

        return UserInDB(**created_user, profile=profile)
    
    async def authenticate_user(self, *, email: EmailStr, password: str) -> Optional[UserInDB]:
        user = await self.get_user_by_email(email=email)

        if not user:
            return None
        if not self.auth_service.verify_password(password=password, salt=user.salt, hashed_password=user.password):
            return None
        
        return user
    
    async def populate_user(self, *, user: UserInDB) -> UserInDB:
        user_profile = await self.profiles_repository.get_profile_by_user_id(user_id=user.id)
        user.profile = ProfilePublic(**user_profile.dict())
        return user
    
    async def update_user(self, *, user_update: UserUpdate, requesting_user: UserInDB) -> UserInDB:
        # if requesting_user.username != user_update.username:
            # if await self.get_user_by_username(username=user_update.username):
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail='That username is already taken. Please choose another one.'                
            #     )
            # else:
            #     await self.update_user_username(username=user_update.username, requesting_user=requesting_user)
        if  requesting_user.email != user_update.email:
            if await self.get_user_by_email(email=user_update.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='That email is already taken. Please choose another one.'
                )
            else:
                await self.update_user_email(email=user_update.email, requesting_user=requesting_user)
        
        return await self.get_user_by_id(user_id=requesting_user.id)

    async def deactivate_user(self, *, requesting_user: UserInDB) -> UserInDB:
        if not await self.get_user_by_email(email=requesting_user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='There is no user with that username. Something went wrong.'
            )
        return await self.db.fetch_one(
            query=DEACTIVATE_USER_QUERY,
            values={
                'user_id': requesting_user.id
            }
        )

    # async def update_user_username(self, *, username: str, requesting_user: UserInDB) -> None:
    #     await self.db.fetch_one(
    #         query=UPDATE_USER_USERNAME_QUERY,
    #         values={
    #             'username': username,
    #             'id': requesting_user.id
    #         }
    #     )

    async def update_user_email(self, *, email: str, requesting_user: UserInDB) -> None:
        await self.db.fetch_one(
            query=UPDATE_USER_EMAIL_QUERY,
            values={
                'email': email,
                'id': requesting_user.id
            }
        )


