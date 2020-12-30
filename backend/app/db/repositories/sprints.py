from typing import List
from fastapi import HTTPException, status
from app.db.repositories.base import BaseRepository
from app.models.projects import ProjectCreate, ProjectUpdate, ProjectInDB
from app.models.project_stats import ProjectStats
from app.models.burndown_chart_datasets import BurndownChartDataset, BurndownChartDataPoint
from app.models.teams import TeamInDB
from app.models.users import UserInDB
from app.models.members import MemberInDB

CREATE_SPRINT_QUERY = '''
    INSERT INTO sprints (number, project_id, date_start, date_end)
    VALUES (:number, :project_id, :date_start, :date_end)
    RETURNING
            id,
            number,
            project_id,
            date_start,
            date_end,
            created_at,
            updated_at
'''

GET_SPRINT_BY_ID = '''
    SELECT
        id,
        number,
        project_id,
        date_start,
        date_end,
        created_at,
        updated_at
    FROM sprints
    WHERE id = :id
'''

GET_ALL_PROJECT_SPRINTS = '''
    SELECT
        id,
        number,
        project_id,
        date_start,
        date_end,
        created_at,
        updated_at
    FROM sprints
    WHERE project_id = :project_id;
'''

GET_PROJECT_SPRINT_BY_NUMBER = '''
    SELECT
        id,
        number,
        project_id,
        date_start,
        date_end,
        created_at,
        updated_at
    FROM sprints
    WHERE project_id = :project_id
    AND number = :number;
'''

DELETE_SPRINT_BY_ID_QUERY = '''
    DELETE FROM projects
    WHERE id = :id
    RETURNING id;
'''



class ProjectsRepository(BaseRepository):
    async def create_sprint(self, *, project: ProjectCreate) -> ProjectInDB:
        sprint = await self.db.fetch_one(
            query=CREATE_SPRINT_QUERY,
            values={
                'number': project
            }
        )
        stats = await self.get_project_stats_by_id(project_id=dict(project)['id'])
        return ProjectInDB(**project, stats=stats)
    
    async def get_project_by_id(self, *, project_id: int) -> ProjectInDB:
        project = await self.db.fetch_one(
            query=GET_PROJECT_BY_ID_QUERY,
            values={'id': project_id}
        )
        if not project:
            return None
        stats = await self.get_project_stats_by_id(project_id=dict(project)['id'])
        return ProjectInDB(**project, stats=stats)
    
    async def get_all_user_projects(self, requesting_user: UserInDB) -> List[ProjectInDB]:
        project_records = await self.db.fetch_all(
            query=GET_ALL_USER_PROJECTS_QUERY,
            values={'user_id': requesting_user.id}
        )
        return [
            ProjectInDB(
                **x,
                stats=(await self.get_project_stats_by_id(project_id=dict(x)['id']))
            ) for x in project_records
        ]
    
    async def get_all_team_projects(self, team: TeamInDB) -> List[ProjectInDB]:
        project_records = await self.db.fetch_all(
            query=GET_ALL_TEAM_PROJECTS_QUERY,
            values={'team_id': team.id}
        )
        return [
            ProjectInDB(
                **x,
                stats=(await self.get_project_stats_by_id(project_id=dict(x)['id']))
            ) for x in project_records
        ]

    async def update_project(self, *, project: ProjectInDB, project_update: ProjectUpdate) -> ProjectInDB:
        project_update_parameters = project.copy(update=project_update.dict(exclude_unset=True))
        try:
            await self.db.fetch_one(
                query=UPDATE_PROJECT_BY_ID_QUERY,
                values={
                    **project_update_parameters.dict(
                        exclude={
                            'created_at',
                            'updated_at',
                            'team_id',
                            'stats',
                            'sprint_interval'
                        }
                    )
                }
            )
            return await self.get_project_by_id(project_id=project.id)
            # return ProjectInDB(**updated_project)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid update parameters.')
    
    async def delete_project_by_id(self, *, project: ProjectInDB) -> int:
        return await self.db.execute(query=DELETE_PROJECT_BY_ID_QUERY, values={'id': project.id})
    
    async def get_project_stats_by_id(self, *, project_id: int) -> ProjectStats:
        burndown = await self.get_project_burndown_chart_by_id(project_id=project_id)
        stats = await self.db.fetch_one(query=GET_PROJECT_STATS_BY_ID_QUERY, values={'project_id': project_id})
        print(dict(stats))
        return ProjectStats(**stats, chart_data=burndown)
    
    async def get_project_burndown_chart_by_id(self, *, project_id: int):
        data = await self.db.fetch_all(
            query=GET_PROJECT_CHART_DATA_QUERY,
            values={'project_id': project_id}
        )

        added = [{'t': x['t'], 'y': x['c_sum']} for x in data]
        burned = [{'t': x['t'], 'y': x['d_sum']} for x in data]
        current = [{'t': x['t'], 'y': x['c_sum'] - x['d_sum']} for x in data]

        return BurndownChartDataset(added=added, burned=burned, current=current)