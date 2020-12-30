from typing import List
from fastapi import HTTPException, status
from fastapi.websockets import WebSocketDisconnect
from app.db.repositories.base import BaseRepository
from app.db.repositories.profiles import ProfilesRepository
from app.db.repositories.projects import ProjectsRepository
from app.models.tasks import TaskCreate, TaskUpdate, TaskInDB
from app.models.users import UserInDB
from app.models.projects import ProjectInDB

CREATE_TASK_QUERY = '''
    INSERT INTO tasks (name, description, cost, project_id, status, user_id, dependent_on, date_todo, date_done)
    VALUES (:name, :description, :cost, :project_id, :status, :user_id, :dependent_on, :date_todo, :date_done)
    RETURNING id, name, description, cost, project_id, status, user_id, dependent_on, date_todo, date_done, created_at, updated_at;
'''

GET_TASK_BY_ID_QUERY = '''
    SELECT id, name, description, cost, project_id, status, user_id, dependent_on, date_todo, date_done, created_at, updated_at
    FROM tasks
    WHERE id = :id;
'''

GET_ALL_TASKS_QUERY = '''
    SELECT id, name, description, cost, project_id, status, user_id, dependent_on, date_todo, date_done, created_at, updated_at
    FROM tasks;
'''

GET_ALL_USER_TASKS_QUERY = '''
    SELECT id, name, description, cost, project_id, status, user_id, dependent_on, date_todo, date_done, created_at, updated_at
    FROM tasks
    WHERE user_id = :user_id;
'''

GET_ALL_PROJECT_TASKS_QUERY ='''
    SELECT id, name, description, cost, project_id, status, user_id, dependent_on, date_todo, date_done, created_at, updated_at
    FROM tasks
    WHERE project_id = :project_id
'''

UPDATE_TASK_BY_ID_QUERY = '''
    UPDATE tasks
    SET 
        name         = :name,
        description  = :description,
        cost         = :cost,
        status       = :status,
        date_todo    = :date_todo,
        date_done    = :date_done,
        dependent_on = :dependent_on,
        user_id = :user_id
    WHERE id = :id
    RETURNING id, name, description, cost, project_id, status, user_id, dependent_on, date_done, created_at, updated_at
'''

UPDATE_TASK_USER_ID_QUERY = '''
    UPDATE tasks
    SET 
        user_id = :user_id
    WHERE id = :id
    RETURNING id, name, description, cost, project_id, status, user_id, dependent_on, date_done, created_at, updated_at
'''

DELETE_TASK_BY_ID_QUERY = '''
    DELETE FROM tasks
    WHERE id = :id
    RETURNING id;
'''

GET_LATEST_TASK_CHANGE_BY_PROJECT = '''
    SELECT MAX(updated_at) AS latest
    FROM tasks
    WHERE project_id = :project_id;
'''

class TasksRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db)
        self.profile_repo = ProfilesRepository(db=db)

    async def create_task(self, *, new_task: TaskCreate, requesting_user: UserInDB) -> TaskInDB:
        task = await self.db.fetch_one(
            query=CREATE_TASK_QUERY,
            values={
                **new_task.dict()
            }
        )
        return await self.populate_task(task=TaskInDB(**task))
    
    async def get_task_by_id(self, *, id: int) -> TaskInDB:
        task = await self.db.fetch_one(
            query=GET_TASK_BY_ID_QUERY,
            values={'id': id}
        )
        if not task:
            return None
        return await self.populate_task(task=TaskInDB(**task))
    
    async def get_all_user_tasks(self, requesting_user: UserInDB) -> List[TaskInDB]:
        task_records = await self.db.fetch_all(
            query=GET_ALL_USER_TASKS_QUERY,
            values={'user_id': requesting_user.id}
        )
        return [await self.populate_task(task=TaskInDB(**x)) for x in task_records]

    async def get_all_project_tasks(self, project: ProjectInDB) -> List[TaskInDB]:
        task_records = await self.db.fetch_all(
            query=GET_ALL_PROJECT_TASKS_QUERY,
            values={'project_id': project.id}
        )
        return [(await self.populate_task(task=TaskInDB(**x))) for x in task_records]
    
    async def get_all_project_todo_tasks(self, project: ProjectInDB) -> List[TaskInDB]:
        tasks = await self.get_all_project_tasks(project=project)
        return [x for x in tasks if x.status == 'to_do']
    
    async def get_all_project_ongoing_tasks(self, project: ProjectInDB) -> List[TaskInDB]:
        tasks = await self.get_all_project_tasks(project=project)
        return [x for x in tasks if x.status == 'ongoing']

    async def get_all_project_done_tasks(self, project: ProjectInDB) -> List[TaskInDB]:
        tasks = await self.get_all_project_tasks(project=project)
        return [x for x in tasks if x.status == 'done']

    async def update_task(
        self, *, task: TaskInDB, task_update: TaskUpdate
    ) -> TaskInDB:
        task_update_params = task.copy(update=task_update.dict(exclude_unset=True))
        if task_update_params.status is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid task type. Cannot be None.'
            )
        updated_task = await self.db.fetch_one(
            query=UPDATE_TASK_BY_ID_QUERY,
            values={
                **task_update_params.dict(exclude={'created_at', 'updated_at', 'project_id', 'user_id', 'blocked'})
            },
        )
        return await self.populate_task(task=TaskInDB(**updated_task))

    async def delete_task_by_id(self, *, task: TaskInDB) -> int:
        return await self.db.execute(query=DELETE_TASK_BY_ID_QUERY, values={'id': task.id})

    async def populate_task(self, *, task: TaskInDB):
        user_profile = await self.profile_repo.get_profile_by_user_id(user_id=task.user_id)
        is_blocked = await self.check_if_blocked(task=task)
        task.user_id = user_profile
        task.blocked = is_blocked
        return task

    async def check_if_blocked(self, *, task: TaskInDB) -> bool:
        QUERY = '''
            SELECT status
            FROM tasks
            WHERE id
            IN (
                SELECT unnest(dependent_on)
                FROM tasks
                WHERE id=:task_id
            )
        '''
        records = await self.db.fetch_all(query=QUERY, values={'task_id': task.id})
        for r in records:
            if dict(r)['status'] != 'done':
                return True
        return False

    async def get_latest_project_tasks_change(self, *, project_id: int):
        latest = await self.db.fetch_one(query=GET_LATEST_TASK_CHANGE_BY_PROJECT, values={'project_id': project_id})
        print(dict(latest)['latest'], type(dict(latest)['latest']))
        return dict(latest)['latest']

class TasksRepositoryWS(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db)
        self.profile_repo = ProfilesRepository(db=db)

    async def create_task(self, *, new_task: TaskCreate) -> TaskInDB:
        task = await self.db.fetch_one(
            query=CREATE_TASK_QUERY,
            values={
                **new_task.dict()
            }
        )
        return await self.populate_task(task=TaskInDB(**task))
    
    async def get_task_by_id(self, *, task_id: int, populate: bool = True) -> TaskInDB:
        task = await self.db.fetch_one(
            query=GET_TASK_BY_ID_QUERY,
            values={'id': task_id}
        )
        if not task:
            return None
        if populate:
            return await self.populate_task(task=TaskInDB(**task))
        else:
            return TaskInDB(**task)
    
    async def get_all_project_tasks(self, project_id: int) -> List[TaskInDB]:
        task_records = await self.db.fetch_all(
            query=GET_ALL_PROJECT_TASKS_QUERY,
            values={'project_id': project_id}
        )
        return [(await self.populate_task(task=TaskInDB(**x))) for x in task_records]
    
    async def update_task(
        self, *, task_id: int, task_update: TaskUpdate
    ) -> TaskInDB:
        # print(task_update)
        task = await self.get_task_by_id(task_id=task_id, populate=False)
        task_update_params = task.copy(update=task_update.dict(exclude_unset=True))
        # user_id_task = await self.db.fetch_one(
        #     query=UPDATE_TASK_USER_ID_QUERY,
        #     values={
        #         'id': task.id,
        #         'user_id': task_update.user_id
        #     },
        # )    
        updated_task = await self.db.fetch_one(
            query=UPDATE_TASK_BY_ID_QUERY,
            values={
                **task_update_params.dict(exclude={'created_at', 'updated_at', 'project_id', 'blocked'})
            },
        )
        return await self.populate_task(task=TaskInDB(**updated_task))

    async def delete_task_by_id(self, *, task_id: int) -> int:
        return await self.db.execute(query=DELETE_TASK_BY_ID_QUERY, values={'id': task_id})
    
    async def populate_task(self, *, task: TaskInDB):
        user_profile = await self.profile_repo.get_profile_by_user_id(user_id=task.user_id)
        # print(user_profile)
        is_blocked = await self.check_if_blocked(task=task)
        task.user_id = user_profile
        task.blocked = is_blocked
        return task
    
    async def check_if_blocked(self, *, task: TaskInDB) -> bool:
        QUERY = '''
            SELECT status
            FROM tasks
            WHERE id
            IN (
                SELECT unnest(dependent_on)
                FROM tasks
                WHERE id=:task_id
            )
        '''
        records = await self.db.fetch_all(query=QUERY, values={'task_id': task.id})
        for r in records:
            if dict(r)['status'] != 'done':
                return True
        return False
    
    async def is_user_allowed(self, *, user_id: int, project_id: int) -> bool:
        QUERY = '''
            SELECT m.user_id
            FROM members m
            WHERE m.team_id
            IN (
                SELECT p.team_id
                FROM projects p
                WHERE p.id = :project_id
                )
        '''
        users = await self.db.fetch_all(
            query=QUERY,
            values={
                'project_id': project_id
            }
        )
        if user_id in [y['user_id'] for y in [dict(x) for x in users]]:
            return True
        return False