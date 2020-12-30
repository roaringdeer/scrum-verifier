import pytest
from databases import Database
from fastapi import FastAPI, status
from httpx import AsyncClient
from app.db.repositories.profiles import ProfilesRepository
from app.models.users import UserInDB, UserPublic
from app.models.profiles import ProfileInDB, ProfilePublic


pytestmark = pytest.mark.asyncio

class TestProfilesRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient, test_user: UserInDB) -> None:
        result = await client.get(app.url_path_for('profiles:get-profile-by-username', username=test_user.username))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.put(app.url_path_for('profiles:update-own-profile'), json={'profile_update': {}})
        assert result.status_code != status.HTTP_404_NOT_FOUND

class TestProfileCreate:
    async def test_profile_created_for_new_users(
        self,
        app: FastAPI,
        client: AsyncClient,
        db: Database
    ) -> None:
        profile_repository = ProfilesRepository(db)

        new_user = {'email': 'dwayne@johnson.io', 'username': 'therock', 'password': 'dwaynetherockjohnson'}
        result = await client.post(app.url_path_for('users:register-new-user'), json={'new_user': new_user})
        assert result.status_code == status.HTTP_201_CREATED

        created_user = UserPublic(**result.json())
        user_profile = await profile_repository.get_profile_by_user_id(user_id=created_user.id)
        assert user_profile is not None
        assert isinstance(user_profile, ProfileInDB)

class TestProfileView:
    async def test_authenticated_user_can_view_other_users_profile(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user: UserInDB,
        test_user2: UserInDB
    ) -> None:
        result = await authorized_client.get(
            app.url_path_for(
                'profiles:get-profile-by-username',
                username=test_user2.username
            )
        )
        assert result.status_code == status.HTTP_200_OK
        profile = ProfilePublic(**result.json())
        assert profile.username == test_user2.username
    
    async def test_unregistered_users_cannot_access_other_users_profile(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_user2: UserInDB
    ) -> None:
        result = await client.get(
            app.url_path_for(
                'profiles:get-profile-by-username',
                username=test_user2.username
            )
        )
        assert result.status_code == status.HTTP_401_UNAUTHORIZED
    
    async def test_no_profile_is_returned_whet_username_matches_no_user(
        self,
        app: FastAPI,
        authorized_client: AsyncClient
    ) -> None:
        result = await authorized_client.get(
            app.url_path_for(
                'profiles:get-profile-by-username',
                username='username_doesnt_match'
            )
        )
        assert result.status_code == status.HTTP_404_NOT_FOUND

class TestProfileManagement:
    @pytest.mark.parametrize(
        'key, value',
        (
            ('full_name','Lebron James'),
            ('phone_number','555-333-100'),
            ('bio','This is a test bio'),
            ('image','http://testimages.com/testimage')
        )
    )
    async def test_user_can_update_own_profile(
        self, app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB, key: str, value: str
    ) -> None:
        assert getattr(test_user.profile, key) != value
        result = await authorized_client.put(
            app.url_path_for('profiles:update-own-profile'),
            json={'profile_update': {key: value}}
        )
        assert result.status_code == status.HTTP_200_OK
        profile = ProfilePublic(**result.json())
        assert getattr(profile, key) == value

    @pytest.mark.parametrize(
        'key, value, status_code',
        (
            ('full_name', [], 422),
            ('phone_number', '123123-123132-32132', 422),
            ('phone_number', 'wrong number', 422),
            ('bio', {}, 422),
            ('image', './image-string.png', 422),
            ('image', 5, 422)
        )
    )
    async def test_user_recieves_error_for_invalid_update_params(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user: UserInDB,
        key: str,
        value: str,
        status_code: int
    ) -> None:
        result = await authorized_client.put(
            app.url_path_for('profiles:update-own-profile'),
            json={'profile_update': {key: value}}
        )
        assert result.status_code == status_code