from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from app.models.tasks import TaskCreate, TaskPublic, TaskUpdate, TaskInDB
from app.models.users import UserInDB
from app.db.repositories.tasks import TasksRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user
from app.api.dependencies.tasks import get_task_by_id_from_path, check_task_general_permissions

router = APIRouter()

@router.post(
    '/',
    response_model=TaskPublic,
    name='tasks:create-task',
    status_code=status.HTTP_201_CREATED
)
async def create_new_task(
    new_task: TaskCreate = Body(...,embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    tasks_repository: TasksRepository = Depends(get_repository(TasksRepository))
) -> TaskPublic:
    return await tasks_repository.create_task(new_task=new_task, requesting_user=current_user)

@router.get(
    '/', 
    response_model=List[TaskPublic], 
    name='tasks:get-all-user-tasks', 
)
async def get_all_user_tasks(
    current_user: UserInDB = Depends(get_current_active_user),
    tasks_repository: TasksRepository = Depends(get_repository(TasksRepository))
) -> List[TaskPublic]:
    return await tasks_repository.get_all_user_tasks(requesting_user=current_user)

@router.get(
    '/{task_id}/',
    response_model=TaskPublic, 
    name='tasks:get-task-by-id', 
    dependencies=[Depends(check_task_general_permissions)]
)
async def get_task_by_id(task: TaskInDB = Depends(get_task_by_id_from_path)) -> TaskPublic:
    return task

@router.put(
    '/{task_id}/', 
    response_model=TaskPublic, 
    name='tasks:update-task-by-id', 
    dependencies=[Depends(check_task_general_permissions)]
)
async def update_task_by_id(
    task: TaskInDB = Depends(get_task_by_id_from_path),
    task_update: TaskUpdate = Body(..., embed=True),
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository)),
) -> TaskPublic:
    return await tasks_repo.update_task(task=task, task_update=task_update)

@router.delete(
    '/{task_id}/', 
    response_model=int, 
    name='tasks:delete-task-by-id', 
    dependencies=[Depends(check_task_general_permissions)]
)
async def delete_task_by_id(
    task: TaskInDB = Depends(get_task_by_id_from_path),
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository)),
) -> int:
    return await tasks_repo.delete_task_by_id(task=task)
