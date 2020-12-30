from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from app.models.teams import TeamCreate, TeamPublic, TeamUpdate, TeamInDB
from app.models.projects import ProjectPublic
from app.models.users import UserInDB
from app.db.repositories.teams import TeamsRepository
from app.db.repositories.projects import ProjectsRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user
from app.api.dependencies.teams import get_team_by_id_from_path, check_team_modification_permissions

router = APIRouter()

@router.post('/', response_model=TeamPublic, name='teams:create-team', status_code=status.HTTP_201_CREATED)
async def create_new_team(
    new_team: TeamCreate = Body(..., embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    teams_repository: TeamsRepository = Depends(get_repository(TeamsRepository))
) -> TeamPublic:
    return await teams_repository.create_team(new_team=new_team, requesting_user=current_user)

@router.get('/', response_model=List[TeamPublic], name='teams:get-all-user-teams')
async def list_all_user_teams(
    current_user: UserInDB = Depends(get_current_active_user),
    teams_repository: TeamsRepository = Depends(get_repository(TeamsRepository))
) -> List[TeamPublic]:
    return await teams_repository.get_all_user_teams(requesting_user=current_user)

@router.get('/{team_id}/', response_model=TeamPublic, name='teams:get-team-by-id')
async def get_team_by_id(team: TeamInDB = Depends(get_team_by_id_from_path)) -> TeamPublic:
    return team


################### DO ZMIANY ############
@router.get('/{team_id}/projects', response_model=List[ProjectPublic], name='teams:get-team-by-id')
async def get_team_projects(
    team: TeamInDB = Depends(get_team_by_id_from_path),
    projects_repository: ProjectsRepository = Depends(get_repository(ProjectsRepository))
) -> List[ProjectPublic]:
    return await projects_repository.get_all_team_projects(team)
#############################################

@router.put('/{team_id}/', response_model=TeamPublic, name='teams:update-team-by-id', dependencies=[Depends(check_team_modification_permissions)])
async def update_team_by_id(
    team: TeamInDB = Depends(get_team_by_id_from_path),
    team_update: TeamUpdate = Body(..., embed=True),
    teams_repo: TeamsRepository = Depends(get_repository(TeamsRepository)),
) -> TeamPublic:
    return await teams_repo.update_team(team=team, team_update=team_update)

@router.delete('/{team_id}/', response_model=int, name='teams:delete-team-by-id', dependencies=[Depends(check_team_modification_permissions)])
async def delete_team_by_id(
    team: TeamInDB = Depends(get_team_by_id_from_path),
    teams_repo: TeamsRepository = Depends(get_repository(TeamsRepository)),
) -> int:
    return await teams_repo.delete_team_by_id(team=team)
