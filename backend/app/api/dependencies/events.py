from fastapi import HTTPException, Depends, Path, status
from app.models.users import UserInDB
from app.models.events import EventInDB
from app.db.repositories.events import EventsRepository
from app.db.repositories.teams import TeamsRepository
from app.db.repositories.projects import ProjectsRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user

async def get_event_by_id_from_path(
    event_id: int = Path(..., ge=1),
    current_user: UserInDB = Depends(get_current_active_user),
    events_repo: EventsRepository = Depends(get_repository(EventsRepository)),
) -> EventInDB:
    event = await events_repo.get_event_by_id(event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No project found with that id.',
        )
    return event

async def check_event_modification_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    event: EventInDB = Depends(get_event_by_id_from_path),
    teams_repo: TeamsRepository = Depends(get_repository(TeamsRepository)),
    projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository))
) -> None:
    project = await projects_repo.get_project_by_id(project_id=event.project_id)
    team = await teams_repo.get_team_by_id(team_id=project.team_id)
    if current_user.id == team.owner_id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Action forbidden. Users are only able to modify projects they own.',
    )
