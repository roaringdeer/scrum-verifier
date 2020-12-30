import pytest
from typing import List
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database
from app.db.repositories.teams import TeamsRepository
from app.models.teams import TeamCreate, TeamInDB, TeamPublic
from app.models.users import UserInDB

pytestmark = pytest.mark.asyncio

@pytest.fixture
def new_team():
    return TeamCreate(
        name='test team',
        description='test description of team'
    )

@pytest.fixture
async def test_teams_list(db: Database, test_user2: UserInDB):
    teams_repository = TeamsRepository(db)
    return [
        await teams_repository.create_team(
            new_team=TeamCreate(
                name=f'test team {i}',
                description='test description'
            ),
            requesting_user=test_user2,
        )
        for i in range(5)
    ]

class TestTeamsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        result = await client.post(app.url_path_for('teams:create-team'), json={})
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('teams:get-team-by-id', team_id=1))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('teams:update-team-by-id', team_id=1))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('teams:delete-team-by-id', team_id=0))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('teams:get-all-user-teams'))
        assert result.status_code != status.HTTP_404_NOT_FOUND

class TestCreateTeam:
    async def test_valid_input_creates_team_belonging_to_user(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user: UserInDB,
        new_team: TeamCreate
    ) -> None:
        result = await authorized_client.post(
            app.url_path_for('teams:create-team'),
            json={'new_team': new_team.dict()}
        )
        assert result.status_code == status.HTTP_201_CREATED
        created_team = TeamPublic(**result.json())
        assert created_team.name == new_team.name
        assert created_team.description == new_team.description
        assert created_team.owner_id == test_user.id

    async def test_unauthorized_user_unable_to_create_team(
        self,
        app: FastAPI,
        client: AsyncClient,
        new_team: TeamCreate
    ) -> None:
        result = await client.post(
            app.url_path_for('teams:create-team'), json={'new_team': new_team.dict()}
        )
        assert result.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        'invalid_payload, status_code',
        (
            (None, 422),
            ({}, 422)
        )
    )
    async def test_invalid_input_raises_error(
        self, app: FastAPI, authorized_client: AsyncClient, invalid_payload: dict, status_code: int, test_team: TeamCreate
    ) -> None:
        result = await authorized_client.post(
            app.url_path_for('teams:create-team'),
            json={'new_team':  invalid_payload}
        )
        assert result.status_code == status_code

class TestGetTeam:
    async def test_get_team_by_id(self, app: FastAPI, authorized_client: AsyncClient, test_team: TeamInDB):
        result = await authorized_client.get(app.url_path_for('teams:get-team-by-id', team_id=test_team.id))
        assert result.status_code == status.HTTP_200_OK
        team = TeamInDB(**result.json())
        assert team == test_team
    
    async def test_unauthorized_users_cant_access_teams(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_team: TeamInDB
    ) -> None:
        result = await client.get(
            app.url_path_for('teams:get-team-by-id', team_id=test_team.id)
        )
        assert result.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        'id, status_code',
        (
            (500, 404),
            (-1, 422),
            (None, 422)
        )
    )
    async def test_wrong_id_returns_error(
        self, app: FastAPI, authorized_client: AsyncClient, id: int, status_code: int
    ) -> None:
        result = await authorized_client.get(app.url_path_for('teams:get-team-by-id', team_id=id))
        assert result.status_code == status_code
    
    async def test_get_all_teams_returns_only_user_owned_teams(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_team: TeamInDB,
        test_teams_list: List[TeamInDB],
        test_user: UserInDB,
        db: Database
    ) -> None:
        result = await authorized_client.get(app.url_path_for('teams:get-all-user-teams'))
        assert result.status_code == status.HTTP_200_OK
        assert isinstance(result.json(), list)
        assert len(result.json()) > 0
        teams = [TeamInDB(**x) for x in result.json()]
        assert test_team in teams
        for team in teams:
            assert team.owner_id == test_user.id
        assert all(t not in teams for t in test_teams_list)

class TestUpdateTeam:
    @pytest.mark.parametrize(
        'keys, values',
        (
            (['name'], ['new fake team name']),
            (['description'], ['new fake team description']),
            (['name', 'description'], ['new new fake team name', 'new new fake team description'])
        )
    )
    async def test_update_team_with_valid_input(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_team: TeamInDB,
        keys: List[str],
        values: List[str]
    ) -> None:
        team_update = {'team_update': {keys[i]: values[i] for i in range(len(keys))}}
        result = await authorized_client.put(
            app.url_path_for('teams:update-team-by-id', team_id=test_team.id),
            json=team_update
        )
        assert result.status_code == status.HTTP_200_OK
        updated_team = TeamInDB(**result.json())
        assert updated_team.id == test_team.id

        for i in range(len(keys)):
            assert getattr(updated_team, keys[i]) != getattr(test_team, keys[i])
            assert getattr(updated_team, keys[i]) == values[i]

        for key, value in updated_team.dict().items():
            if key not in keys and key != 'updated_at':
                assert getattr(test_team, key) == value
    
    async def test_user_recieves_error_if_updating_other_users_team(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_teams_list: List[TeamInDB]
    ) -> None:
        result = await authorized_client.put(
            app.url_path_for('teams:update-team-by-id', team_id=test_teams_list[0].id),
            json={'team_update': {'name': 'other user modified name'}}
        )
        assert result.status_code == status.HTTP_403_FORBIDDEN
    
    async def test_user_cant_change_ownership_of_team(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_team: TeamInDB,
        test_user: UserInDB,
        test_user2: UserInDB
    ) -> None:
        result = await authorized_client.put(
            app.url_path_for('teams:update-team-by-id', team_id=test_team.id),
            json={'team_update': {'owner_id': test_user2.id}}
        )
        assert result.status_code == status.HTTP_200_OK
        team = TeamPublic(**result.json())
        assert team.owner_id == test_user.id

    @pytest.mark.parametrize(
        'id, payload, status_code',
        (
            (
                (-1, {'name': 'test'}, 422),
                (0, {'name': 'test2'}, 422),
                (500, {'name': 'test3'}, 404),
                (1, None, 422),
            )
        )
    )
    async def test_update_team_with_invalid_input_throws_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_team: TeamInDB,
        id: int,
        payload: dict,
        status_code: int
    ) -> None:
        team_update = {'team_update': payload}
        result = await authorized_client.put(
            app.url_path_for('teams:update-team-by-id', team_id=id),
            json=team_update
        )
        assert result.status_code == status_code

class TestDeleteTeam:
    async def test_can_delete_team_successfully(
        self, app: FastAPI, authorized_client: AsyncClient, test_team: TeamInDB
    ) -> None:
        result = await authorized_client.delete(app.url_path_for('teams:delete-team-by-id', team_id=test_team.id))
        assert result.status_code == status.HTTP_200_OK
        result = await authorized_client.get(app.url_path_for('teams:get-team-by-id', team_id=test_team.id))
        assert result.status_code == status.HTTP_404_NOT_FOUND

    async def test_user_cant_delete_other_users_team(
        self, app: FastAPI, authorized_client: AsyncClient, test_teams_list: List[TeamInDB]
    ) -> None:
        result = await authorized_client.delete(
            app.url_path_for('teams:delete-team-by-id', team_id=test_teams_list[0].id)
        )
        assert result.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        'id, status_code',
        (
            (500, 404),
            (0, 422),
            (-1, 422),
            (None, 422)
        )
    )
    async def test_wrong_id_throws_error(
        self, app: FastAPI, authorized_client: AsyncClient, test_team: TeamInDB, id: int, status_code: int
    ) -> None:
        result = await authorized_client.delete(app.url_path_for('teams:delete-team-by-id', team_id=id))
        assert result.status_code == status_code
