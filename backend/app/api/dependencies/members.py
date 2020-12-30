from fastapi import HTTPException, Depends, status
from app.models.users import UserInDB
from app.models.teams import TeamInDB
from app.models.members import MemberInDB
from app.db.repositories.members import MembersRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user
from app.api.dependencies.users import get_user_by_username_from_path
from app.api.dependencies.teams import get_team_by_id_from_path

async def get_member_for_team_from_user(
    *, user: UserInDB, team: TeamInDB, members_repo: MembersRepository,
) -> MemberInDB:
    member = await members_repo.get_member_for_team_from_user(team=team, user=user)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Member not found.')
    return member

async def get_member_for_team_from_user_by_path(
    user: UserInDB = Depends(get_user_by_username_from_path),
    team: TeamInDB = Depends(get_team_by_id_from_path),
    members_repo: MembersRepository = Depends(get_repository(MembersRepository)),
) -> MemberInDB:
    return await get_member_for_team_from_user(user=user, team=team, members_repo=members_repo)

async def check_member_create_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    team: TeamInDB = Depends(get_team_by_id_from_path),
    members_repo: MembersRepository = Depends(get_repository(MembersRepository)),
) -> None:
    if team.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Only team owner can add members.',
        )
    # if await members_repo.get_member_for_team_from_user(team=team, user=current_user):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail='User cannot be added twice to the same team.',
    #     )

def check_member_list_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    team: TeamInDB = Depends(get_team_by_id_from_path),
) -> None:
    if team.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Unable to access members.',
        )

def check_member_get_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    team: TeamInDB = Depends(get_team_by_id_from_path),
    member: MemberInDB = Depends(get_member_for_team_from_user_by_path),
) -> None:
    if team.owner_id != current_user.id and member.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Unable to access member.',
        )

def check_member_role_change_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    team: TeamInDB = Depends(get_team_by_id_from_path),
    member: MemberInDB = Depends(get_member_for_team_from_user_by_path)
) -> None:
    if team.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only the owner of the team may accept members.'
        )

def check_member_remove_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    team: TeamInDB = Depends(get_team_by_id_from_path),
    member: MemberInDB = Depends(get_member_for_team_from_user_by_path)
) -> None:
    if current_user.id not in [team.owner_id, member.user_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only team owner may remove other members, and members may remove only themselves.'
        )
    if member.user_id == team.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Team owner can\'t remove themselves.'
        )
