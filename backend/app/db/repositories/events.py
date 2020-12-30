from typing import List
import pytz
from datetime import datetime
from fastapi import HTTPException, status
from app.db.repositories.base import BaseRepository
from app.models.events import EventCreate, EventUpdate, EventInDB, EventBase
from app.models.projects import ProjectInDB
from app.models.users import UserInDB

CREATE_EVENT_QUERY = '''
    INSERT INTO events (title, description, project_id, event_type, start_date, end_date, all_day)
    VALUES (:title, :description, :project_id, :event_type, :start_date, :end_date, :all_day)
    RETURNING id, title, description, project_id, event_type, start_date, end_date, all_day, created_at, updated_at;
'''

GET_EVENT_BY_ID_QUERY = '''
    SELECT id, title, description, project_id, event_type, start_date, end_date, all_day, created_at, updated_at
    FROM events
    WHERE id = :event_id;
'''

GET_ALL_EVENTS_QUERY = '''
    SELECT title, description, project_id, event_type, start_date, end_date, all_day, created_at, updated_at
    FROM events;
'''

GET_ALL_USER_EVENTS_QUERY = '''
    SELECT e.id, e.title, e.description, e.project_id, e.event_type, e.start_date, e.end_date, e.all_day, e.created_at, e.updated_at
    FROM events e
    WHERE e.project_id IN (
        SELECT p.id
        FROM projects p
        WHERE p.team_id IN(
            SELECT m.team_id
            FROM members m
            WHERE m.user_id = :user_id
        )
    );
'''

GET_ALL_PROJECT_EVENTS_QUERY = '''
    SELECT id, title, description, project_id, event_type, start_date, end_date, all_day, created_at, updated_at
    FROM events
    WHERE project_id = :project_id;
'''

UPDATE_EVENT_BY_ID_QUERY = '''
    UPDATE events
    SET 
        title = :title,
        description = :description,
        event_type = :event_type,
        start_date = :start_date,
        end_date = :end_date,
        all_day = :all_day
    WHERE id = :id
    RETURNING id, title, description, project_id, event_type, start_date, end_date, all_day, created_at, updated_at
'''

DELETE_EVENT_BY_ID_QUERY = '''
    DELETE FROM events
    WHERE id = :event_id
    RETURNING id;
'''

class EventsRepository(BaseRepository):
    async def create_event(self, *, new_event: EventCreate) -> EventInDB:
        # new_event = self.convert_to_utc(event=new_event)
        query_values = new_event.dict()
        print('-'*20, query_values)
        event = await self.db.fetch_one(
            query=CREATE_EVENT_QUERY,
            values={
                **query_values
            }
        )
        return EventInDB(**event)
    
    async def get_event_by_id(self, *, event_id: int) -> EventInDB:
        event = await self.db.fetch_one(query=GET_EVENT_BY_ID_QUERY, values={'event_id': event_id})
        if not event:
            return None
        return EventInDB(**event)
    
    async def get_all_user_events(self, requesting_user: UserInDB) -> List[EventInDB]:
        event_records = await self.db.fetch_all(
            query=GET_ALL_USER_EVENTS_QUERY,
            values={'user_id': requesting_user.id}
        )
        return [EventInDB(**x) for x in event_records]

    async def get_all_project_events(self, project: ProjectInDB) -> List[EventInDB]:
        event_records = await self.db.fetch_all(
            query=GET_ALL_PROJECT_EVENTS_QUERY,
            values={'project_id': project.id}
        )
        return [EventInDB(**x) for x in event_records]

    async def update_event(
        self, *, event: EventInDB, event_update: EventUpdate
    ) -> EventInDB:
        # event = self.convert_to_utc(event=event)
        # event_update = self.convert_to_utc(event=event_update)
        event_update_params = event.copy(update=event_update.dict(exclude_unset=True))
        # if team_update_params.status is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid team type. Cannot be None.'
        #     )
        updated_event = await self.db.fetch_one(
            query=UPDATE_EVENT_BY_ID_QUERY,
            values={
                **event_update_params.dict(exclude={'created_at', 'updated_at', 'project_id'})
            },
        )
        return EventInDB(**updated_event)

    async def delete_event_by_id(self, *, event: EventInDB) -> int:
        return await self.db.execute(query=DELETE_EVENT_BY_ID_QUERY, values={'event_id': event.id})
    
    # def convert_to_utc(self, event: EventBase):
    #     if not event.start_date:
    #         event.start_date = datetime.utcnow()
    #     else:
    #         event.start_date = event.start_date.astimezone(pytz.utc).replace(tzinfo=None)
    #     if not event.end_date:
    #         event.end_date = event.start_date
    #     else:
    #         event.end_date = event.end_date.astimezone(pytz.utc).replace(tzinfo=None)
    #     return event
