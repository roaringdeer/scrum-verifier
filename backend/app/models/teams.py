from typing import Optional, Union
from enum import Enum
from app.models.core import CoreModel, IDModelMixin, DatetimeModelMixin
from app.models.users import UserPublic

class TeamBase(CoreModel):
    name: Optional[str]
    description: Optional[str]

class TeamCreate(TeamBase):
    name: str

class TeamUpdate(TeamBase):
    pass

class TeamInDB(IDModelMixin, TeamBase, DatetimeModelMixin):
    name: str
    owner_id: Union[int, UserPublic]
    
class TeamPublic(TeamInDB):
    pass
