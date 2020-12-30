from typing import List, Optional, Tuple
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status, Request, Query
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from sse_starlette.sse import EventSourceResponse
from app.utils.websockets import WebSocketManager
from app.services.tasks import project_tasks_generator
from app.models.projects import ProjectCreate, ProjectPublic, ProjectUpdate, ProjectInDB
from app.models.users import UserInDB
from app.models.tasks import TaskPublic, TaskUpdate, TaskCreate
from app.models.events import EventPublic
from app.models.project_stats import ProjectStats
from app.db.repositories.projects import ProjectsRepository
from app.db.repositories.tasks import TasksRepository, TasksRepositoryWS
from app.db.repositories.events import EventsRepository
from app.db.repositories.members import MembersRepository
from app.api.dependencies.database import get_repository, get_repository_ws
from app.api.dependencies.authentication import get_current_active_user
from app.api.dependencies.projects import get_project_by_id_from_path, check_project_modification_permissions
from app.api.dependencies.stream import get_stream_key

router = APIRouter()

@router.post('/', response_model=ProjectPublic, name='projects:create-project', status_code=status.HTTP_201_CREATED)
async def create_new_project(
    new_project: ProjectCreate = Body(..., embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    projects_repository: ProjectsRepository = Depends(get_repository(ProjectsRepository))
) -> ProjectPublic:
    return await projects_repository.create_project(new_project=new_project)

@router.get('/', response_model=List[ProjectPublic], name='projects:get-all-user-projects')
async def get_all_user_projects(
    current_user: UserInDB = Depends(get_current_active_user),
    projects_repository: ProjectsRepository = Depends(get_repository(ProjectsRepository))
) -> List[ProjectPublic]:
    return await projects_repository.get_all_user_projects(requesting_user=current_user)

@router.get('/{project_id}/', response_model=ProjectPublic, name='projects:get-project-by-id')
async def get_project_by_id(project: ProjectInDB = Depends(get_project_by_id_from_path)) -> ProjectPublic:
    return project

######## DO TESTÓW
@router.get('/{project_id}/tasks', response_model=List[TaskPublic], name='projects:get-project-tasks')
async def get_project_tasks(
    project: ProjectInDB = Depends(get_project_by_id_from_path),
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository))
) -> List[TaskPublic]:
    return await tasks_repo.get_all_project_tasks(project=project)

@router.get('/{project_id}/events', response_model=List[EventPublic], name='projects:get-project-events')
async def get_project_events(
    project: ProjectInDB = Depends(get_project_by_id_from_path),
    events_repo: EventsRepository = Depends(get_repository(EventsRepository))
) -> List[EventPublic]:
    return await events_repo.get_all_project_events(project=project)

@router.get('/{project_id}/stats', response_model=ProjectStats, name='projects:get-project-stats')
async def get_project_stats(
    project_id: int = Path(...,ge=1),
    projects_repository: ProjectsRepository = Depends(get_repository(ProjectsRepository))
) -> ProjectStats:
    return await projects_repository.get_project_stats_by_id(project_id=project_id)

@router.get('/{project_id}/chart')
async def get_project_chart(
    project_id: int = Path(...,ge=1),
    projects_repository: ProjectsRepository = Depends(get_repository(ProjectsRepository))
):
    return await projects_repository.get_project_burndown_chart_by_id(project_id=project_id)

@router.put('/{project_id}/', response_model=ProjectPublic, name='projects:update-project-by-id', dependencies=[Depends(check_project_modification_permissions)])
async def update_project_by_id(
    project: ProjectInDB = Depends(get_project_by_id_from_path),
    project_update: ProjectUpdate = Body(..., embed=True),
    projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
) -> ProjectPublic:
    return await projects_repo.update_project(project=project, project_update=project_update)

@router.delete('/{project_id}/', response_model=int, name='projects:delete-project-by-id', dependencies=[Depends(check_project_modification_permissions)])
async def delete_project_by_id(
    project: ProjectInDB = Depends(get_project_by_id_from_path),
    projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
) -> int:
    return await projects_repo.delete_project_by_id(project=project)

manager = WebSocketManager()

@router.get('/ws/ticket')
async def get_ticket(
    current_user: UserInDB = Depends(get_current_active_user)
):
    return {'ticket': manager.create_new_ticket(requesting_user=current_user)}

@router.websocket('/{project_id}/ws')
async def tasks_ws(
    websocket: WebSocket,
    ticket: str = Query(...),
    project_id: int = Path(...),
    tasks_repo: TasksRepositoryWS = Depends(get_repository_ws(TasksRepositoryWS))
):
    user_id = manager.consume_ticket(ticket=ticket)
    if user_id is not None:
        if await tasks_repo.is_user_allowed(user_id=user_id, project_id=project_id):
            await manager.connect(websocket=websocket, project_id=project_id)
            try:
                while True:
                    message = await websocket.receive_json()
                    if 'user_id' in message['payload'] and message['payload']['user_id'] is not None:
                        # manager.broadcast_text('a', project_id=project_id)
                        if not isinstance(message['payload']['user_id'], int):
                            message['payload']['user_id'] = message['payload']['user_id']['id']
                    if message['action'] == 'create':
                        payload_task = TaskCreate(**message['payload'])
                        created_task = await tasks_repo.create_task(new_task=payload_task)
                    elif message['action'] == 'update':
                        payload_task = TaskUpdate(**message['payload'])
                        updated_task = await tasks_repo.update_task(task_id=message['payload']['id'], task_update=payload_task)
                    elif message['action'] == 'delete':
                        deleted_task_id = await tasks_repo.delete_task_by_id(task_id=message['payload']['id'])
                    all_tasks = await tasks_repo.get_all_project_tasks(project_id=project_id)
                    await manager.broadcast_json(json=jsonable_encoder(all_tasks), project_id=project_id)
            except WebSocketDisconnect:
                manager.disconnect(websocket=websocket, project_id=project_id)