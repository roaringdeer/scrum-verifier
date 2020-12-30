import pytest
from typing import List
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database
from app.db.repositories.projects import ProjectsRepository
from app.models.projects import ProjectCreate, ProjectInDB, ProjectPublic
from app.models.users import UserInDB
from app.models.teams import TeamInDB

pytestmark = pytest.mark.asyncio

@pytest.fixture
def new_project(test_team: TeamInDB):
    return ProjectCreate(
        name='test project',
        description='test description of project',
        team_id=test_team.id
    )

@pytest.fixture
async def test_projects_list(db: Database, test_user2: UserInDB, test_team_with_members: TeamInDB):
    projects_repository = ProjectsRepository(db)
    return [
        await projects_repository.create_project(
            new_project=ProjectCreate(
                name=f'test project {i}',
                description='test description',
                team_id=test_team_with_members.id
            )
        )
        for i in range(5)
    ]

class TestProjectsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        result = await client.post(app.url_path_for('projects:create-project'), json={})
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('projects:get-project-by-id', project_id=1))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('projects:update-project-by-id', project_id=1))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('projects:delete-project-by-id', project_id=0))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        # result = await client.post(app.url_path_for('projects:get-all-user-projects'))
        # assert result.status_code != status.HTTP_404_NOT_FOUND

class TestCreateProject:
    async def test_valid_input_creates_project_belonging_to_team(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user: UserInDB,
        test_team: TeamInDB,
        new_project: ProjectCreate
    ) -> None:
        result = await authorized_client.post(
            app.url_path_for('projects:create-project'),
            json={'new_project': new_project.dict()}
        )
        assert result.status_code == status.HTTP_201_CREATED
        created_project = ProjectPublic(**result.json())
        assert created_project.name == new_project.name
        assert created_project.description == new_project.description
        assert created_project.team_id == test_team.id

    async def test_unauthorized_user_unable_to_create_project(
        self,
        app: FastAPI,
        client: AsyncClient,
        new_project: ProjectCreate,
        test_team: TeamInDB
    ) -> None:
        result = await client.post(
            app.url_path_for('projects:create-project'),
            json={'new_project': new_project.dict()}
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
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        invalid_payload: dict,
        status_code: int,
        test_team: TeamInDB,
        new_project: ProjectCreate
    ) -> None:
        result = await authorized_client.post(
            app.url_path_for('projects:create-project'),
            json={'new_project':  invalid_payload}
        )
        assert result.status_code == status_code

class TestGetProject:
    async def test_get_project_by_id(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_project: ProjectInDB
    ) -> None:
        result = await authorized_client.get(
            app.url_path_for(
                'projects:get-project-by-id',
                project_id=test_project.id,
            )
        )
        assert result.status_code == status.HTTP_200_OK
        project = ProjectInDB(**result.json())
        assert project == test_project
    
    async def test_unauthorized_users_cant_access_projects(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_project: ProjectInDB,
    ) -> None:
        result = await client.get(
            app.url_path_for(
                'projects:get-project-by-id',
                project_id=test_project.id,
            )
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
    async def test_wrong_project_id_returns_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        id: int,
        status_code: int
    ) -> None:
        result = await authorized_client.get(
            app.url_path_for(
                'projects:get-project-by-id',
                project_id=id,
            )
        )
        assert result.status_code == status_code
    
    #TODO
    async def test_get_all_projects_returns_only_user_owned_projects(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_project: ProjectInDB,
        test_projects_list: List[ProjectInDB],
        test_user: UserInDB,
        test_team: TeamInDB,
        db: Database
    ) -> None:
        result = await authorized_client.get(
            app.url_path_for('projects:get-all-user-projects')
        )
        assert result.status_code == status.HTTP_200_OK
        assert isinstance(result.json(), list)
        assert len(result.json()) > 0
        projects = [ProjectInDB(**x) for x in result.json()]
        assert test_project in projects
        assert any(p.team_id == test_team.id for p in projects)
        assert all(p not in projects for p in test_projects_list)

class TestUpdateProject:
    @pytest.mark.parametrize(
        'keys, values',
        (
            (['name'], ['new fake project name']),
            (['description'], ['new fake project description']),
            (['is_archived'], [True]),
            (['name', 'description'], ['new new fake project name', 'new new fake project description'])

        )
    )
    async def test_update_project_with_valid_input(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_project: ProjectInDB,
        keys: List[str],
        values: List[str]
    ) -> None:
        project_update = {'project_update': {keys[i]: values[i] for i in range(len(keys))}}
        result = await authorized_client.put(
            app.url_path_for(
                'projects:update-project-by-id',
                project_id=test_project.id
            ),
            json=project_update
        )
        assert result.status_code == status.HTTP_200_OK
        updated_project = ProjectInDB(**result.json())
        assert updated_project.id == test_project.id

        for i in range(len(keys)):
            assert getattr(updated_project, keys[i]) != getattr(test_project, keys[i])
            assert getattr(updated_project, keys[i]) == values[i]

        for key, value in updated_project.dict().items():
            if key not in keys and key != 'updated_at':
                assert getattr(test_project, key) == value
    
    #TODO
    async def test_user_recieves_error_if_updating_project_they_dont_own(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_projects_list: List[ProjectInDB],
    ) -> None:
        result = await authorized_client.put(
            app.url_path_for(
                'projects:update-project-by-id',
                project_id=test_projects_list[0].id,
            ),
            json={'project_update': {'name': 'other user modified name'}}
        )
        assert result.status_code == status.HTTP_403_FORBIDDEN
    
    async def test_user_cant_change_projects_team(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_project: ProjectInDB,
        test_team: TeamInDB,
        test_team_with_members: TeamInDB
    ) -> None:
        result = await authorized_client.put(
            app.url_path_for(
                'projects:update-project-by-id',
                project_id=test_project.id
            ),
            json={'project_update': {'team_id': test_team_with_members.id}}
        )
        assert result.status_code == status.HTTP_200_OK
        project = ProjectPublic(**result.json())
        assert project.team_id == test_team.id

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
    async def test_update_project_with_invalid_input_throws_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_project: ProjectInDB,
        id: int,
        payload: dict,
        status_code: int
    ) -> None:
        project_update = {'project_update': payload}
        result = await authorized_client.put(
            app.url_path_for(
                'projects:update-project-by-id',
                project_id=id
            ),
            json=project_update
        )
        assert result.status_code == status_code

class TestDeleteProject:
    async def test_can_delete_project_successfully(
        self, app: FastAPI, authorized_client: AsyncClient, test_project: ProjectInDB
    ) -> None:
        result = await authorized_client.delete(
            app.url_path_for(
                'projects:delete-project-by-id',
                project_id=test_project.id
            )
        )
        assert result.status_code == status.HTTP_200_OK
        result = await authorized_client.get(
            app.url_path_for(
                'projects:get-project-by-id',
                project_id=test_project.id
            )
        )
        assert result.status_code == status.HTTP_404_NOT_FOUND

    #TODO
    async def test_user_cant_delete_other_users_project(
        self, app: FastAPI, authorized_client: AsyncClient, test_projects_list: List[ProjectInDB]
    ) -> None:
        result = await authorized_client.delete(
            app.url_path_for(
                'projects:delete-project-by-id',
                project_id=test_projects_list[0].id
            )
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
        self, app: FastAPI, authorized_client: AsyncClient, test_project: ProjectInDB, id: int, status_code: int
    ) -> None:
        result = await authorized_client.delete(
            app.url_path_for(
                'projects:delete-project-by-id',
                project_id=id
            )
        )
        assert result.status_code == status_code
