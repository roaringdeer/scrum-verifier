from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class CoreModel(BaseModel):
    '''
    Common logic shared by all models
    '''
    pass

class IDModelMixin(BaseModel):
    '''
    Mixin class containing id field
    '''
    id: int

class DatetimeModelMixin(BaseModel):
    '''
    Mixin class containing creation and update timestamps
    '''
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator('created_at', 'updated_at', pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()