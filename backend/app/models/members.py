from typing import Optional, Union
from enum import Enum
from pydantic import Field
from app.models.core import CoreModel, IDModelMixin, DatetimeModelMixin
from app.models.profiles import ProfilePublic
from app.models.teams import TeamPublic


class UserRole(str, Enum):
    developer = 'dev'
    scrum_master = 'sm'
    product_owner = 'po'
    none = 'none'

class MemberBase(CoreModel):
    user_id: Optional[int]
    team_id: Optional[int]
    role: Optional[str] = UserRole.developer

class MemberCreate(MemberBase):
    user_id: int
    team_id: int

class MemberUpdate(CoreModel):
    role: UserRole

class MemberInDB(DatetimeModelMixin, MemberBase):
    profile: Optional[ProfilePublic]
    team: Optional[TeamPublic]

class MemberPublic(MemberInDB):
    pass
