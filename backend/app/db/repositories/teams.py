from typing import List
from fastapi import HTTPException, status
from app.db.repositories.base import BaseRepository
from app.models.teams import TeamCreate, TeamUpdate, TeamInDB
from app.models.users import UserInDB

CREATE_TEAM_QUERY = '''
    INSERT INTO teams (name, description, owner_id)
    VALUES (:name, :description, :owner_id)
    RETURNING id, name, description, owner_id, created_at, updated_at;
'''

ADD_INITIAL_TEAM_MEMBER_QUERY = '''
    INSERT INTO members (team_id, user_id)
    VALUES (:team_id, :user_id)
'''

GET_TEAM_BY_ID_QUERY = '''
    SELECT id, name, description, owner_id, created_at, updated_at
    FROM teams
    WHERE id = :id;
'''

GET_ALL_TEAMS_QUERY = '''
    SELECT id, name, description, owner_id, created_at, updated_at
    FROM teams;
'''

GET_ALL_USER_TEAMS_QUERY = '''
    SELECT id, name, description, owner_id, created_at, updated_at
    FROM teams
    WHERE owner_id = :owner_id;
'''

UPDATE_TEAM_BY_ID_QUERY = '''
    UPDATE teams
    SET 
        name        = :name,
        description = :description
    WHERE id = :id
    RETURNING id, name, description, owner_id, created_at, updated_at
'''

DELETE_TEAM_BY_ID_QUERY = '''
    DELETE FROM teams
    WHERE id = :id
    RETURNING id;
'''

class TeamsRepository(BaseRepository):
    async def create_team(self, *, new_team: TeamCreate, requesting_user: UserInDB) -> TeamInDB:
        query_values = new_team.dict()
        team = await self.db.fetch_one(
            query=CREATE_TEAM_QUERY,
            values={
                **query_values,
                'owner_id': requesting_user.id
            }
        )
        await self.db.fetch_one(
            query=ADD_INITIAL_TEAM_MEMBER_QUERY,
            values={
                'team_id': TeamInDB(**team).id,
                'user_id': requesting_user.id
            }
        )
        return TeamInDB(**team)
    
    async def get_team_by_id(self, *, team_id: int) -> TeamInDB:
        team = await self.db.fetch_one(query=GET_TEAM_BY_ID_QUERY, values={'id': team_id})
        if not team:
            return None
        return TeamInDB(**team)
    
    async def get_all_user_teams(self, requesting_user: UserInDB) -> List[TeamInDB]:
        team_records = await self.db.fetch_all(
            query=GET_ALL_USER_TEAMS_QUERY,
            values={'owner_id': requesting_user.id}
        )
        return [TeamInDB(**x) for x in team_records]

    async def update_team(
        self, *, team: TeamInDB, team_update: TeamUpdate
    ) -> TeamInDB:
        team_update_params = team.copy(update=team_update.dict(exclude_unset=True))
        # if team_update_params.status is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid team type. Cannot be None.'
        #     )
        updated_team = await self.db.fetch_one(
            query=UPDATE_TEAM_BY_ID_QUERY,
            values={
                **team_update_params.dict(exclude={'created_at', 'updated_at', 'owner_id'})
            },
        )
        return TeamInDB(**updated_team)

    async def delete_team_by_id(self, *, team: TeamInDB) -> int:
        return await self.db.execute(query=DELETE_TEAM_BY_ID_QUERY, values={'id': team.id}) 
