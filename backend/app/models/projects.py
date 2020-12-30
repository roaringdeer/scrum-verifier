from typing import Optional, Union
from enum import Enum
from app.models.core import CoreModel, IDModelMixin, DatetimeModelMixin
from app.models.teams import TeamPublic
from app.models.project_stats import ProjectStats
from app.models.sprints import SprintInDB

class ProjectBase(CoreModel):
    name: Optional[str]
    description: Optional[str]
    is_archived: Optional[bool] = False
    team_id: Optional[int]
    sprint_interval: Optional[int]

class ProjectCreate(ProjectBase):
    name: str
    team_id: int
    sprint_interval: int

class ProjectUpdate(ProjectBase):
    is_archived: Optional[bool]

class ProjectInDB(IDModelMixin, ProjectBase, DatetimeModelMixin):
    name: str
    is_archived: bool
    team_id: Union[int, TeamPublic]
    sprint_interval: int
    # current_sprint: SprintInDB
    stats: ProjectStats
    
class ProjectPublic(ProjectInDB):
    pass
