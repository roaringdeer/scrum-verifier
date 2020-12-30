from fastapi import HTTPException, Depends, Path, status
from app.models.users import UserInDB
from app.models.teams import TeamInDB
from app.db.repositories.teams import TeamsRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user

async def get_team_by_id_from_path(
    team_id: int = Path(..., ge=1),
    current_user: UserInDB = Depends(get_current_active_user),
    teams_repo: TeamsRepository = Depends(get_repository(TeamsRepository)),
) -> TeamInDB:
    team = await teams_repo.get_team_by_id(team_id=team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No team found with that id.',
        )
    return team

def check_team_modification_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    team: TeamInDB = Depends(get_team_by_id_from_path),
) -> None:
    pass
    if team.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Action forbidden. Users are only able to modify teams they own.',
        )
