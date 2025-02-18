import pytest, jwt
from typing import List, Union, Type, Optional
from pydantic import ValidationError
from httpx import AsyncClient
from fastapi import FastAPI, HTTPException, status
from starlette.datastructures import Secret
from starlette.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST, 
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND, 
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from databases import Database
from app.core.config import SECRET_KEY, JWT_ALGORITHM, JWT_AUDIENCE, JWT_TOKEN_PREFIX, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.users import UserCreate, UserInDB, UserPublic
from app.models.token import JWTMeta, JWTCreds, JWTPayload
from app.db.repositories.users import UsersRepository
from app.services import auth_service

pytestmark = pytest.mark.asyncio

class TestUserRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        new_user = {'email': 'test@email.io', 'username': 'test_username', 'password': 'testpassword'}
        result = await client.post(app.url_path_for('users:register-new-user'), json={'new_user': new_user})
        assert result.status_code != HTTP_404_NOT_FOUND

class TestUserRegistration:
    async def test_users_can_register_successfully(
        self, 
        app: FastAPI, 
        client: AsyncClient,
        db: Database,
    ) -> None:
        user_repo = UsersRepository(db)
        new_user = {'email': 'shakira@shakira.io', 'username': 'shakirashakira', 'password': 'chantaje'}

        user_in_db = await user_repo.get_user_by_email(email=new_user['email'])
        assert user_in_db is None

        result = await client.post(app.url_path_for('users:register-new-user'), json={'new_user': new_user})
        assert result.status_code == HTTP_201_CREATED

        user_in_db = await user_repo.get_user_by_email(email=new_user['email'])
        assert user_in_db is not None
        assert user_in_db.email == new_user['email']
        assert user_in_db.username == new_user['username']

        created_user = UserPublic(**result.json()).dict(exclude={'access_token'})
        assert created_user == user_in_db.dict(exclude={'password', 'salt'})

    @pytest.mark.parametrize(
        'attr, value, status_code',
        (
            ('email', 'shakira@shakira.io', 400),            
            ('username', 'shakirashakira', 400),
            ('email', 'invalid_email@one@two.io', 422),
            ('password', 'short', 422),
            ('username', 'shakira@#$%^<>', 422),
            ('username', 'ab', 422),
        )
    )
    async def test_user_registration_fails_when_credentials_are_taken(
        self, 
        app: FastAPI, 
        client: AsyncClient,
        db: Database,
        attr: str,
        value: str,
        status_code: int,
    ) -> None: 
        new_user = {'email': 'nottaken@email.io', 'username': 'not_taken_username', 'password': 'freepassword'}
        new_user[attr] = value
        res = await client.post(app.url_path_for('users:register-new-user'), json={'new_user': new_user})
        assert res.status_code == status_code
    
    async def test_users_saved_password_is_hashed_and_has_salt(
        self,
        app: FastAPI,
        client: AsyncClient,
        db: Database
    ) -> None:
        user_repository = UsersRepository(db)
        new_user = {'email': 'beyonce@knowles.io', 'username': 'queenbey', 'password': 'destinyschild'}

        result = await client.post(app.url_path_for('users:register-new-user'), json={'new_user': new_user})
        assert result.status_code == HTTP_201_CREATED

        user_in_db = await user_repository.get_user_by_email(email=new_user['email'])
        assert user_in_db is not None
        assert user_in_db.salt is not None and user_in_db.salt != '123'
        assert user_in_db.password != new_user['password']
        assert auth_service.verify_password(
            password=new_user['password'],
            salt=user_in_db.salt,
            hashed_password=user_in_db.password
        )

class TestAuthTokens:
    async def test_can_create_access_token_successfully(
        self, app: FastAPI, client: AsyncClient, test_user: UserInDB
    ) -> None:
        access_token = auth_service.create_access_token_for_user(
            user=test_user,
            secret_key=str(SECRET_KEY),
            audience=JWT_AUDIENCE,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        creds = jwt.decode(access_token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
        assert creds.get('username') is not None
        assert creds['username'] == test_user.username
        assert creds['aud'] == JWT_AUDIENCE
    
    async def test_token_missing_user_is_invalid(
        self, app: FastAPI, client:AsyncClient
    ) -> None:
        access_token = auth_service.create_access_token_for_user(
            user=None,
            secret_key=str(SECRET_KEY),
            audience=JWT_AUDIENCE,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        with pytest.raises(jwt.PyJWTError):
            jwt.decode(access_token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
    
    @pytest.mark.parametrize(
        'secret_key, jwt_audience, exception',
        (
            ('wrong-secret', JWT_AUDIENCE, jwt.InvalidTokenError),
            (None, JWT_AUDIENCE, jwt.InvalidTokenError),
            (SECRET_KEY, 'othersite:auth', jwt.InvalidAudienceError),
            (SECRET_KEY, None, ValidationError)
        )
    )
    async def test_invalid_token_content_raises_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_user: UserInDB,
        secret_key: Union[str, Secret],
        jwt_audience: str,
        exception: Type[BaseException]
    ) -> None:
        with pytest.raises(exception):
            access_token = auth_service.create_access_token_for_user(
                user=test_user,
                secret_key=str(secret_key),
                audience=jwt_audience,
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
            )

            jwt.decode(access_token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
    
    async def test_can_retrieve_username_from_token(
        self, app: FastAPI, client: AsyncClient, test_user: UserInDB
    ) -> None:
        token = auth_service.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
        username = auth_service.get_username_from_token(token=token, secret_key=str(SECRET_KEY))
        assert username == test_user.username
    
    @pytest.mark.parametrize(
        'secret, wrong_token',
        (
            (SECRET_KEY, 'asdf'),
            (SECRET_KEY, ''),
            (SECRET_KEY, None),
            ('ABC123', 'use correct token')
        )
    )
    async def test_error_when_token_or_secret_is_wrong(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_user: UserInDB,
        secret: Union[Secret, str],
        wrong_token: Optional[str]
    ) -> None:
        token = auth_service.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))

        if wrong_token == 'use correct token':
            wrong_token = token
        
        with pytest.raises(HTTPException):
            username = auth_service.get_username_from_token(token=wrong_token, secret_key=str(secret))

class TestUserLogin:
    async def test_user_can_login_successfully_and_receives_valid_token(
        self, app: FastAPI, client: AsyncClient, test_user: UserInDB
    ) -> None:
        client.headers['content-type'] = 'application/x-www-form-urlencoded'
        login_data = {
            'username': test_user.email,
            'password': 'heatcavslakers'
        }
        result = await client.post(app.url_path_for('users:login-email-and-password'), data=login_data)
        assert result.status_code == HTTP_200_OK

        token = result.json().get('access_token')
        creds = jwt.decode(token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
        assert 'username' in creds
        assert creds['username'] == test_user.username
        assert 'sub' in creds
        assert creds['sub'] == test_user.email

        assert 'token_type' in result.json()
        assert result.json().get('token_type') == 'bearer'
    
    @pytest.mark.parametrize(
        'credential, wrong_value, status_code',
        (
            ('email', 'wrong@email.com', 401),
            ('email', None, 401),
            ('email', 'noteemail', 401),
            ('password', 'wrongpassword', 401),
            ('password', None, 401)
        )
    )
    async def test_user_with_wrong_creds_doesnt_receive_token(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_user: UserInDB,
        credential: str,
        wrong_value: str,
        status_code: int
    ) -> None:
        client.headers['content-type'] = 'application/x-www-form-urlencoded'
        user_data = test_user.dict()
        user_data['password'] = 'heatcavslakers'
        user_data[credential] = wrong_value
        login_data = {
            'username': user_data['email'],
            'password': user_data['password']
        }

        result = await client.post(app.url_path_for('users:login-email-and-password'), data=login_data)
        assert result.status_code == status_code
        assert 'access_token' not in result.json()

class TestUserMe:
    async def test_authenticated_user_can_retrieve_own_data(
        self, app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB
    ) -> None:
        result = await authorized_client.get(app.url_path_for('users:get-current-user'))
        assert result.status_code == HTTP_200_OK
        user = UserPublic(**result.json())
        assert user.email == test_user.email
        assert user.username == test_user.username
        assert user.id == test_user.id
    
    async def test_user_cannot_access_own_data_if_not_authenticated(
        self, app: FastAPI, client: AsyncClient, test_user: UserInDB
    ) -> None:
        result = await client.get(app.url_path_for('users:get-current-user'))
        assert result.status_code == HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        'jwt_prefix',
        (
            ('',),
            ('value',),
            ('JWT',),
            ('Token',),
            ('Swearer',)
        )
    )
    async def test_user_cannot_access_own_data_with_incorrect_jwt_prefix(
        self, app:FastAPI, client: AsyncClient, test_user: UserInDB, jwt_prefix: str
    ) -> None:
        token = auth_service.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
        result = await client.get(
            app.url_path_for('users:get-current-user'),
            headers={'Authorization': f'{jwt_prefix} {token}'}
        )
        assert result.status_code == HTTP_401_UNAUTHORIZED