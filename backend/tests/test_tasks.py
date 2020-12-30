import pytest
from typing import List
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database
from datetime import datetime
from app.db.repositories.tasks import TasksRepository
from app.models.tasks import TaskCreate, TaskInDB, TaskPublic
from app.models.users import UserInDB
from app.models.projects import ProjectInDB

pytestmark = pytest.mark.asyncio

@pytest.fixture
def new_task(test_project: ProjectInDB):
    return TaskCreate(
        name='test task',
        description='test description of task',
        cost=1,
        project_id=test_project.id
    )

@pytest.fixture
async def test_tasks_list(db: Database, test_user2: UserInDB, test_project2: ProjectInDB):
    tasks_repository = TasksRepository(db)
    return [
        await tasks_repository.create_task(
            new_task=TaskCreate(
                name=f'test task {i}',
                description='test description',
                cost=1,
                project_id=test_project2.id
            ),
            requesting_user=test_user2
        )
        for i in range(5)
    ]

class TestTasksRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        result = await client.post(app.url_path_for('tasks:create-task'), json={})
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('tasks:get-task-by-id', task_id=1))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('tasks:update-task-by-id', task_id=1))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('tasks:delete-task-by-id', task_id=0))
        assert result.status_code != status.HTTP_404_NOT_FOUND
        result = await client.post(app.url_path_for('tasks:get-all-user-tasks'))
        assert result.status_code != status.HTTP_404_NOT_FOUND

class TestCreateTask:
    async def test_valid_input_creates_task_belonging_to_project(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user: UserInDB,
        test_project: ProjectInDB,
        new_task: TaskCreate
    ) -> None:
        result = await authorized_client.post(
            app.url_path_for('tasks:create-task'),
            json={'new_task': new_task.dict()}
        )
        print(result.json(), app.url_path_for('tasks:create-task'))
        assert result.status_code == status.HTTP_201_CREATED
        created_task = TaskPublic(**result.json())
        assert created_task.name == new_task.name
        assert created_task.description == new_task.description
        assert created_task.project_id == test_project.id

    async def test_unauthorized_user_unable_to_create_task(
        self,
        app: FastAPI,
        client: AsyncClient,
        new_task: TaskCreate,
        test_project: ProjectInDB
    ) -> None:
        result = await client.post(
            app.url_path_for('tasks:create-task'),
            json={'new_task': new_task.dict()}
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
        test_project: ProjectInDB,
        new_task: TaskCreate
    ) -> None:
        result = await authorized_client.post(
            app.url_path_for('tasks:create-task'),
            json={'new_task':  invalid_payload}
        )
        assert result.status_code == status_code

class TestGetTask:
    async def test_get_task_by_id(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_task: TaskInDB
    ) -> None:
        result = await authorized_client.get(
            app.url_path_for(
                'tasks:get-task-by-id',
                task_id=test_task.id,
            )
        )
        assert result.status_code == status.HTTP_200_OK
        task = TaskInDB(**result.json())
        assert task == test_task
    
    async def test_unauthorized_users_cant_access_tasks(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_task: TaskInDB,
    ) -> None:
        result = await client.get(
            app.url_path_for(
                'tasks:get-task-by-id',
                task_id=test_task.id,
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
    async def test_wrong_task_id_returns_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        id: int,
        status_code: int
    ) -> None:
        result = await authorized_client.get(
            app.url_path_for(
                'tasks:get-task-by-id',
                task_id=id,
            )
        )
        assert result.status_code == status_code
    
    async def test_get_all_tasks_returns_only_user_owned_tasks(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_task: TaskInDB,
        test_tasks_list: List[TaskInDB],
        test_user: UserInDB,
        test_project: ProjectInDB,
        db: Database
    ) -> None:
        result = await authorized_client.get(
            app.url_path_for('tasks:get-all-user-tasks')
        )
        print(result.json())
        assert result.status_code == status.HTTP_200_OK
        assert isinstance(result.json(), list)
        assert len(result.json()) > 0
        tasks = [TaskInDB(**x) for x in result.json()]
        assert test_task in tasks
        assert any(p.project_id == test_project.id for p in tasks)
        assert all(p not in tasks for p in test_tasks_list)

class TestUpdateTask:
    @pytest.mark.parametrize(
        'keys, values',
        (
            (['name'], ['new fake task name']),
            (['description'], ['new fake task description']),
            (['cost'], [19]),
            (['date_done'], [datetime.now()]),
            (['name', 'description'], ['new new fake task name', 'new new fake task description'])

        )
    )
    async def test_update_task_with_valid_input(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_task: TaskInDB,
        keys: List[str],
        values: List[str]
    ) -> None:
        task_update = {'task_update': {keys[i]: values[i] for i in range(len(keys))}}
        if 'date_done' in task_update['task_update']:
            task_update['task_update']['date_done']=task_update['task_update']['date_done'].isoformat()
        result = await authorized_client.put(
            app.url_path_for(
                'tasks:update-task-by-id',
                task_id=test_task.id
            ),
            json=task_update
        )
        assert result.status_code == status.HTTP_200_OK
        updated_task = TaskInDB(**result.json())
        assert updated_task.id == test_task.id

        for i in range(len(keys)):
            assert getattr(updated_task, keys[i]) != getattr(test_task, keys[i])
            assert getattr(updated_task, keys[i]) == values[i]

        for key, value in updated_task.dict().items():
            if key not in keys and key != 'updated_at':
                assert getattr(test_task, key) == value
    
    #TODO
    async def test_user_recieves_error_if_updating_task_they_dont_own(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_tasks_list: List[TaskInDB],
    ) -> None:
        result = await authorized_client.put(
            app.url_path_for(
                'tasks:update-task-by-id',
                task_id=test_tasks_list[0].id,
            ),
            json={'task_update': {'name': 'other user modified name'}}
        )
        assert result.status_code == status.HTTP_403_FORBIDDEN
    
    async def test_user_cant_change_tasks_project(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_task: TaskInDB,
        test_project: ProjectInDB,
        test_project2: ProjectInDB
    ) -> None:
        result = await authorized_client.put(
            app.url_path_for(
                'tasks:update-task-by-id',
                task_id=test_task.id
            ),
            json={'task_update': {'project_id': test_project2.id}}
        )
        assert result.status_code == status.HTTP_200_OK
        task = TaskPublic(**result.json())
        assert task.project_id == test_project.id

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
    async def test_update_task_with_invalid_input_throws_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_task: TaskInDB,
        id: int,
        payload: dict,
        status_code: int
    ) -> None:
        task_update = {'task_update': payload}
        result = await authorized_client.put(
            app.url_path_for(
                'tasks:update-task-by-id',
                task_id=id
            ),
            json=task_update
        )
        assert result.status_code == status_code

class TestDeleteTask:
    async def test_can_delete_task_successfully(
        self, app: FastAPI, authorized_client: AsyncClient, test_task: TaskInDB
    ) -> None:
        result = await authorized_client.delete(
            app.url_path_for(
                'tasks:delete-task-by-id',
                task_id=test_task.id
            )
        )
        assert result.status_code == status.HTTP_200_OK
        result = await authorized_client.get(
            app.url_path_for(
                'tasks:get-task-by-id',
                task_id=test_task.id
            )
        )
        assert result.status_code == status.HTTP_404_NOT_FOUND

    async def test_user_cant_delete_other_teams_task(
        self, app: FastAPI, authorized_client: AsyncClient, test_tasks_list: List[TaskInDB]
    ) -> None:
        result = await authorized_client.delete(
            app.url_path_for(
                'tasks:delete-task-by-id',
                task_id=test_tasks_list[0].id
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
        self, app: FastAPI, authorized_client: AsyncClient, test_task: TaskInDB, id: int, status_code: int
    ) -> None:
        result = await authorized_client.delete(
            app.url_path_for(
                'tasks:delete-task-by-id',
                task_id=id
            )
        )
        assert result.status_code == status_code
