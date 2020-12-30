from typing import List
from fastapi import HTTPException, status
from asyncpg.exceptions import UniqueViolationError
from app.db.repositories.base import BaseRepository
from app.db.repositories.profiles import ProfilesRepository
from app.db.repositories.teams import TeamsRepository
from app.models.teams import TeamInDB, TeamPublic
from app.models.users import UserInDB
from app.models.profiles import ProfilePublic
from app.models.members import MemberCreate, MemberUpdate, MemberInDB

CREATE_MEMBER_FOR_TEAM_QUERY = '''
    INSERT INTO members (team_id, user_id, role)
    VALUES (:team_id, :user_id, :role)
    RETURNING team_id, user_id, role, created_at, updated_at;
'''

LIST_MEMBERS_FOR_TEAM_QUERY = '''
    SELECT team_id, user_id, role, created_at, updated_at
    FROM members
    WHERE team_id = :team_id;
'''

GET_MEMBER_FOR_TEAM_FROM_USER_QUERY = '''
    SELECT team_id, user_id, role, created_at, updated_at
    FROM members
    WHERE team_id = :team_id AND user_id = :user_id;
'''

SET_MEMBER_ROLE_QUERY = '''
    UPDATE members
    SET role = :role
    WHERE team_id = :team_id AND user_id = :user_id
    RETURNING team_id, user_id, role, created_at, updated_at;
'''

REMOVE_MEMBER_FROM_TEAM = '''
    DELETE FROM members
    WHERE team_id = :team_id
    AND user_id = :user_id
    RETURNING team_id, user_id;
'''

class MembersRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db)
        self.teams_repository = TeamsRepository(db)
        self.profiles_repository = ProfilesRepository(db)

    async def create_member_for_team(self, *, new_member: MemberCreate) -> MemberInDB:
        try:
            created_member = await self.db.fetch_one(
                query=CREATE_MEMBER_FOR_TEAM_QUERY, values={**new_member.dict(), 'role': 'none'}
            )
            return await self.populate_member(member=MemberInDB(**created_member))
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User cannot be added twice to the same team.',
            )

    async def list_members_for_team(self, *, team: TeamInDB, populate: bool = True) -> List[MemberInDB]:
        members = await self.db.fetch_all(
            query=LIST_MEMBERS_FOR_TEAM_QUERY, 
            values={'team_id': team.id}
        )
        if not members:
            return None
        if populate:
            return_list = []
            for member_record in members:
                populated_member_record = await self.populate_member(member=MemberInDB(**member_record))
                return_list.append(populated_member_record)
            return return_list
        else:
            return [MemberInDB(**o) for o in members]

    async def get_member_for_team_from_user(self, *, team: TeamInDB, user: UserInDB) -> MemberInDB:
        member_record = await self.db.fetch_one(
            query=GET_MEMBER_FOR_TEAM_FROM_USER_QUERY,
            values={'team_id': team.id, 'user_id': user.id},
        )
        if not member_record:
            return None
        return MemberInDB(**member_record)
    
    async def set_member_role(self, *, member: MemberInDB, member_update: MemberUpdate, team: TeamInDB) -> MemberInDB:
        if member_update.role is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid member role. Cannot be None.'
            )
        elif member_update.role in ['sm', 'po']:
            members_records = await self.list_members_for_team(team=team)
            for member_record in members_records:
                if member_update.role == member_record.role:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Invalid member role {member_update.role}. Must be unique in team.'
                    )
        updated_member = await self.db.fetch_one(
                query=SET_MEMBER_ROLE_QUERY,
                values={
                    'role': member_update.role,
                    'team_id': member.team_id,
                    'user_id': member.user_id
                }
            )
        populated_updated_member = await self.populate_member(member=MemberInDB(**updated_member))
        return populated_updated_member
    
    async def remove_member_from_team(self, *, member: MemberInDB) -> int:
        team_id, user_id = await self.db.fetch_one(
            query=REMOVE_MEMBER_FROM_TEAM,
            values={
                'team_id': member.team_id,
                'user_id': member.user_id
            }
        )
        return 1

    async def populate_member(self, *, member: MemberInDB) -> MemberInDB:
        member_team = await self.teams_repository.get_team_by_id(team_id=member.team_id)
        member_profile = await self.profiles_repository.get_profile_by_user_id(user_id=member.user_id)
        member.profile = ProfilePublic(**member_profile.dict())
        member.team = TeamPublic(**member_team.dict())
        return member
