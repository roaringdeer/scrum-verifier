from typing import Optional
from datetime import date
from app.models.core import DatetimeModelMixin, IDModelMixin, CoreModel

class SprintBase(CoreModel):
    number: Optional[int]
    project_id: Optional[int]
    date_start: Optional[date]
    date_end: Optional[date]

class SprintCreate(SprintBase):
    number: int
    project_id: int
    date_start: date
    date_end: date

class SprintInDB(SprintBase, IDModelMixin, DatetimeModelMixin):
    number: int
    project_id: int
    date_start: date
    date_end: date

class SprintPublic(SprintInDB):
    pass