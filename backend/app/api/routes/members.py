from typing import List
from fastapi import APIRouter, Path, Body, status, Depends
from app.models.members import MemberCreate, MemberUpdate, MemberInDB, MemberPublic
from app.models.teams import TeamInDB, TeamPublic
from app.models.users import UserInDB
from app.db.repositories.members import MembersRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user
from app.api.dependencies.teams import get_team_by_id_from_path
from app.api.dependencies.members import (
    check_member_create_permissions,
    check_member_get_permissions,
    check_member_list_permissions,
    get_member_for_team_from_user_by_path,
    check_member_role_change_permissions,
    check_member_remove_permissions
)

router = APIRouter()
@router.post(
    '/',
    response_model=MemberPublic,
    name='members:create-member',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_member_create_permissions)]
)
async def create_member(
    team: TeamInDB = Depends(get_team_by_id_from_path),
    current_user: UserInDB = Depends(get_current_active_user),
    new_member: MemberCreate = Body(...,embed=True),
    members_repository = Depends(get_repository(MembersRepository))
) -> MemberPublic:
    return await members_repository.create_member_for_team(new_member=new_member)

@router.get(
    '/',
    response_model=List[MemberPublic],
    name='members:list-members-for-team',
    dependencies=[Depends(check_member_list_permissions)]
)
async def get_member_for_team(
    team: TeamInDB = Depends(get_team_by_id_from_path),
    members_repository: MembersRepository = Depends(get_repository(MembersRepository))
) -> MemberPublic:
    return await members_repository.list_members_for_team(team=team)

@router.get(
    '/{username}',
    response_model=MemberPublic,
    name='members:get-member-for-user',
    dependencies=[Depends(check_member_get_permissions)]
)
async def get_member_for_user(
    member: MemberInDB = Depends(get_member_for_team_from_user_by_path)
) -> MemberPublic:
    return member

@router.put(
    '/{username}',
    response_model=MemberPublic,
    name='members:set-user-role',
    dependencies=[Depends(check_member_role_change_permissions)]
)
async def set_user_role_in_team(
    team: TeamInDB = Depends(get_team_by_id_from_path),
    member_update: MemberUpdate = Body(...,embed=True),
    member: MemberInDB = Depends(get_member_for_team_from_user_by_path),
    members_repository: MembersRepository = Depends(get_repository(MembersRepository))
) -> MemberPublic:
    return await members_repository.set_member_role(
        member=member,
        member_update=member_update,
        team=team
    )

@router.delete(
    '/{username}',
    response_model=int,
    name='members:remove-member-from-team',
    dependencies=[Depends(check_member_remove_permissions)]
)
async def remove_member_from_team(
    member: MemberInDB = Depends(get_member_for_team_from_user_by_path),
    members_repository: MembersRepository = Depends(get_repository(MembersRepository))
) -> int:
    return await members_repository.remove_member_from_team(member=member)
