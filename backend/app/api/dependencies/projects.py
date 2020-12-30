from fastapi import HTTPException, Depends, Path, status
from app.models.users import UserInDB
from app.models.projects import ProjectInDB
from app.db.repositories.projects import ProjectsRepository
from app.db.repositories.teams import TeamsRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user

async def get_project_by_id_from_path(
    project_id: int = Path(..., ge=1),
    current_user: UserInDB = Depends(get_current_active_user),
    projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
) -> ProjectInDB:
    project = await projects_repo.get_project_by_id(project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No project found with that id.',
        )
    return project

async def check_project_modification_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    project: ProjectInDB = Depends(get_project_by_id_from_path),
    teams_repo: TeamsRepository = Depends(get_repository(TeamsRepository))
) -> None:
    user_teams = await teams_repo.get_all_user_teams(requesting_user=current_user)
    for team in user_teams:
        if project.team_id == team.id:
            return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail='Action forbidden. Users are only able to modify projects they own.',
    )
