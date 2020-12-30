from typing import List
from fastapi import HTTPException, status
from app.db.repositories.base import BaseRepository
from app.models.projects import ProjectCreate, ProjectUpdate, ProjectInDB
from app.models.project_stats import ProjectStats
from app.models.burndown_chart_datasets import BurndownChartDataset, BurndownChartDataPoint
from app.models.teams import TeamInDB
from app.models.users import UserInDB
from app.models.members import MemberInDB

CREATE_PROJECT_QUERY = '''
    INSERT INTO projects (name, description, is_archived, team_id, sprint_interval)
    VALUES (:name, :description, :is_archived, :team_id, :sprint_interval)
    RETURNING
            id,
            name,
            description,
            is_archived,
            team_id,
            sprint_interval,
            created_at,
            updated_at
'''

GET_PROJECT_BY_ID_QUERY = '''
    SELECT
        id,
        name,
        description,
        is_archived,
        team_id,
        sprint_interval,
        created_at,
        updated_at
    FROM projects
    WHERE id = :id
'''

GET_ALL_TEAM_PROJECTS_QUERY="""
    SELECT
        id,
        name,
        description,
        is_archived,
        team_id,
        sprint_interval,
        created_at,
        updated_at
    FROM projects
    WHERE team_id = :team_id
"""

GET_ALL_USER_PROJECTS_QUERY = '''
    SELECT
        id,
        name,
        description,
        is_archived,
        team_id,
        sprint_interval,
        created_at,
        updated_at
    FROM projects
    WHERE team_id
    IN (
        SELECT m.team_id
        FROM members AS m
        WHERE m.user_id = :user_id
    );
'''

UPDATE_PROJECT_BY_ID_QUERY = '''
    UPDATE projects
    SET name = :name,
        description = :description,
        is_archived = :is_archived
    WHERE id = :id;
'''

DELETE_PROJECT_BY_ID_QUERY = '''
    DELETE FROM projects
    WHERE id = :id
    RETURNING id;
'''

GET_PROJECT_STATS_BY_ID_QUERY = '''
    SELECT
        COUNT(t.id) FILTER(WHERE t.status = 'backlog') AS backlog_count,
        COUNT(t.id) FILTER(WHERE t.status = 'to_do') AS todo_count,
        COUNT(t.id) FILTER(WHERE t.status = 'ongoing') AS ongoing_count,
        COUNT(t.id) FILTER(WHERE t.status = 'done') AS done_count,
        COALESCE(SUM(t.cost) FILTER(WHERE t.status = 'backlog'), 0) AS backlog_points,
        COALESCE(SUM(t.cost) FILTER(WHERE t.status = 'to_do'), 0) AS todo_points,
        COALESCE(SUM(t.cost) FILTER(WHERE t.status = 'ongoing'), 0) AS ongoing_points,
        COALESCE(SUM(t.cost) FILTER(WHERE t.status = 'done'), 0) AS done_points
    FROM tasks t
    WHERE t.project_id = :project_id
'''


GET_PROJECT_CHART_DATA_QUERY = '''
    SELECT 
        COALESCE(c.created_at::DATE, d.date_done::DATE) AS t,
        COALESCE(SUM(c.sum) OVER (ORDER BY COALESCE(c.created_at::DATE, d.date_done::DATE) ASC), 0) AS c_sum,
        COALESCE(SUM(d.sum) OVER (ORDER BY COALESCE(c.created_at::DATE, d.date_done::DATE) ASC), 0) AS d_sum
    FROM
        (SELECT
            created_at::DATE,
            SUM(cost)
        FROM tasks
        WHERE project_id = :project_id
        GROUP BY created_at::DATE) c
    FULL OUTER JOIN
        (SELECT
            date_done::DATE,
            SUM(cost)
        FROM tasks
        WHERE project_id = :project_id
        GROUP BY date_done::DATE) d
    ON c.created_at::DATE = d.date_done::DATE
    WHERE c.created_at IS NOT NULL
    OR d.date_done IS NOT NULL;
'''

class ProjectsRepository(BaseRepository):
    async def create_project(self, *, new_project: ProjectCreate) -> ProjectInDB:
        query_values = new_project.dict()
        project = await self.db.fetch_one(query=CREATE_PROJECT_QUERY, values={**query_values})
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
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid update parameters.')
    
    async def delete_project_by_id(self, *, project: ProjectInDB) -> int:
        return await self.db.execute(query=DELETE_PROJECT_BY_ID_QUERY, values={'id': project.id})
    
    async def get_project_stats_by_id(self, *, project_id: int) -> ProjectStats:
        burndown = await self.get_project_burndown_chart_by_id(project_id=project_id)
        stats = await self.db.fetch_one(query=GET_PROJECT_STATS_BY_ID_QUERY, values={'project_id': project_id})
        # print(dict(stats))
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