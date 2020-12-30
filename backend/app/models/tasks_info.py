from typing import Optional, Union, List
from enum import Enum
from datetime import datetime
from app.models.core import CoreModel, IDModelMixin, DatetimeModelMixin
from app.models.users import UserPublic
from app.models.projects import ProjectPublic

class TaskStatus(str, Enum):
    to_do = 'to_do'
    ongoing = 'ongoing'
    done = 'done'

class TaskBase(CoreModel):
    name: Optional[str]
    description: Optional[str]
    cost: Optional[int]
    project_id: Optional[int]
    status: Optional[TaskStatus] = TaskStatus.to_do
    user_id: Optional[Union[None, int]]
    date_done: Optional[datetime]
    dependent_on: Optional[List[int]] = []

class TaskCreate(TaskBase):
    name: str
    cost: int
    project_id: int

class TaskUpdate(TaskBase):
    status: Optional[TaskStatus]
    dependent_on: Optional[List[int]]
    user_id: Optional[Union[None, int]]

class TaskInDB(IDModelMixin, DatetimeModelMixin, TaskBase):
    name: str
    cost: int
    status: TaskStatus
    user_id: Union[None, int, UserPublic]
    project_id: Union[int, ProjectPublic]

class TaskPublic(TaskInDB):
    pass
