from fastapi import HTTPException, Depends, Path, status
from app.models.users import UserInDB
from app.models.tasks import TaskInDB
from app.db.repositories.tasks import TasksRepository
from app.db.repositories.projects import ProjectsRepository
from app.db.repositories.teams import TeamsRepository
from app.db.repositories.members import MembersRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user

async def get_task_by_id_from_path(
    task_id: int = Path(..., ge=1),
    current_user: UserInDB = Depends(get_current_active_user),
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository)),
) -> TaskInDB:
    task = await tasks_repo.get_task_by_id(id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No task found with that id.',
        )
    return task

async def check_task_general_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    task: TaskInDB = Depends(get_task_by_id_from_path),
    projects_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
    teams_repo: TeamsRepository = Depends(get_repository(TeamsRepository)),
    members_repo: MembersRepository = Depends(get_repository(MembersRepository))
) -> None:
    project = await projects_repo.get_project_by_id(project_id=task.project_id)
    team = await teams_repo.get_team_by_id(team_id=project.team_id)
    member = await members_repo.get_member_for_team_from_user(team=team, user=current_user)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Users aren\'t allowed to access tasks if they don\'t belong to team.',
        )
