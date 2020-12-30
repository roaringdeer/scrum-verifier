from typing import Optional
from pydantic import EmailStr, constr, HttpUrl
from enum import Enum
from datetime import datetime
from app.models.core import DatetimeModelMixin, IDModelMixin, CoreModel

class EventType(str, Enum):
    other = 'other'
    daily = 'daily'
    retro = 'retro'
    review = 'review'
    planning = 'planning'
    

class EventBase(CoreModel):
    title: Optional[str]
    description: Optional[str]
    project_id: Optional[int]
    event_type: Optional[EventType] = EventType.other
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    all_day: Optional[bool] = False

class EventCreate(EventBase):
    title: str
    start_date: datetime
    project_id: int
    end_date: datetime

class EventUpdate(EventBase):
    event_type: Optional[EventType]
    all_day: Optional[bool]

class EventInDB(EventBase, IDModelMixin, DatetimeModelMixin):
    title: str
    project_id: int
    event_type: EventType
    start_date: datetime
    end_date: datetime
    all_day: bool

class EventPublic(EventInDB):
    pass