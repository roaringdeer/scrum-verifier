from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from app.models.projects import ProjectInDB
from app.models.events import EventCreate, EventPublic, EventUpdate, EventInDB
from app.models.users import UserInDB
from app.models.tasks import TaskPublic
from app.db.repositories.events import EventsRepository
from app.db.repositories.tasks import TasksRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user
from app.api.dependencies.events import get_event_by_id_from_path, check_event_modification_permissions

router = APIRouter()

@router.post('/', response_model=EventPublic, name='events:create-event', status_code=status.HTTP_201_CREATED)
async def create_new_event(
    new_event: EventCreate = Body(..., embed=True),
    events_repository: EventsRepository = Depends(get_repository(EventsRepository))
) -> EventPublic:
    return await events_repository.create_event(new_event=new_event)

@router.get('/', response_model=List[EventPublic], name='events:get-all-user-events')
async def get_all_user_events(
    current_user: UserInDB = Depends(get_current_active_user),
    events_repository: EventsRepository = Depends(get_repository(EventsRepository))
) -> List[EventPublic]:
    return await events_repository.get_all_user_events(requesting_user=current_user)

@router.get('/{event_id}/', response_model=EventPublic, name='events:get-event-by-id')
async def get_event_by_id(event: EventInDB = Depends(get_event_by_id_from_path)) -> EventPublic:
    return event

@router.put('/{event_id}/', response_model=EventPublic, name='events:update-event-by-id', dependencies=[Depends(check_event_modification_permissions)])
async def update_event_by_id(
    event: ProjectInDB = Depends(get_event_by_id_from_path),
    event_update: EventUpdate = Body(..., embed=True),
    events_repo: EventsRepository = Depends(get_repository(EventsRepository)),
) -> EventPublic:
    return await events_repo.update_event(event=event, event_update=event_update)

@router.delete('/{event_id}/', response_model=int, name='events:delete-event-by-id', dependencies=[Depends(check_event_modification_permissions)])
async def delete_event_by_id(
    event: EventInDB = Depends(get_event_by_id_from_path),
    events_repo: EventsRepository = Depends(get_repository(EventsRepository)),
) -> int:
    return await events_repo.delete_event_by_id(event=event)