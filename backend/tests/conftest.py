import alembic, warnings, uuid, os, pytest, docker as pydocker
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database
from alembic.config import Config
from typing import List, Callable
from app.core.config import SECRET_KEY, JWT_TOKEN_PREFIX
from app.db.repositories.tasks import TasksRepository
from app.db.repositories.teams import TeamsRepository
from app.db.repositories.projects import ProjectsRepository
from app.db.repositories.users import UsersRepository
from app.db.repositories.members import MembersRepository
from app.models.tasks import TaskCreate, TaskInDB
from app.models.teams import TeamCreate, TeamInDB
from app.models.projects import ProjectCreate, ProjectInDB
from app.models.users import UserCreate, UserInDB
from app.models.members import MemberCreate, MemberUpdate
from app.services import auth_service


@pytest.fixture(scope='session')
def docker() -> pydocker.APIClient:
    return pydocker.APIClient(base_url='unix://var/run/docker.sock', version='auto')

@pytest.fixture(scope='session', autouse=True)
def postgres_container(docker: pydocker.APIClient):

    warnings.filterwarnings('ignore', category=DeprecationWarning)

    image = 'postgres:12.1-alpine'
    docker.pull(image)

    container = docker.create_container(
        image=image,
        name=f'test-postgres-{uuid.uuid4()}',
        detach=True
    )

    docker.start(container=container['Id'])
    
    config = alembic.config.Config('alembic.ini')

    try:
        os.environ['DB_SUFFIX'] = '_test'
        alembic.command.upgrade(config, 'head')
        yield container
    finally:
        alembic.command.downgrade(config, 'base')
        docker.kill(container['Id'])
        docker.remove_container(container=container['Id'], force=True)
    
@pytest.fixture
def app() -> FastAPI:
    from app.api.server import get_application
    return get_application()

@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db

@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url='http://testserver',
            headers={'Content-Type': 'application/json'}
        ) as client:
            yield client

@pytest.fixture
async def test_team(db: Database, test_user: UserInDB) -> TeamInDB:
    teams_repository = TeamsRepository(db)
    members_repo = MembersRepository(db)
    new_team = TeamCreate(
        name='fake team name',
        description='fake team description',
    )
    created_team = await teams_repository.create_team(new_team=new_team, requesting_user=test_user)
    await members_repo.create_member_for_team(
        new_member=MemberCreate(
            team_id=created_team.id,
            user_id=test_user.id
        )
    )
    return created_team

@pytest.fixture
async def test_project(db: Database, test_team: TeamInDB) -> ProjectInDB:
    projects_repository = ProjectsRepository(db)
    new_project = ProjectCreate(
        name='fake project name',
        description='fake project description',
        is_archived=False,
        team_id=test_team.id
    )
    return await projects_repository.create_project(new_project=new_project)

@pytest.fixture
async def test_project2(db: Database, test_team_with_members: TeamInDB) -> ProjectInDB:
    projects_repository = ProjectsRepository(db)
    new_project = ProjectCreate(
        name='fake project name',
        description='fake project description',
        is_archived=False,
        team_id=test_team_with_members.id
    )
    return await projects_repository.create_project(new_project=new_project)

@pytest.fixture
def authorized_client(client: AsyncClient, test_user: UserInDB) -> AsyncClient:
    access_token = auth_service.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))

    client.headers = {
        **client.headers,
        'Authorization': f'{JWT_TOKEN_PREFIX} {access_token}'
    }
    return client

async def user_fixture_factory(*, db: Database, new_user: UserCreate) -> UserInDB:
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)

@pytest.fixture
async def test_user(db: Database) -> UserInDB:
    new_user = UserCreate(email='lebron@james.io', username='lebronjames', password='heatcavslakers')
    return await user_fixture_factory(db=db, new_user=new_user)

@pytest.fixture
async def test_user2(db: Database) -> UserInDB:
    new_user = UserCreate(email='serena@williams.io', username='serenawilliams', password='tennistwins')
    return await user_fixture_factory(db=db, new_user=new_user)

@pytest.fixture
async def test_user3(db: Database) -> UserInDB:
    new_user = UserCreate(email='brad@pitt.io', username='bradpitt', password='adastra')
    return await user_fixture_factory(db=db, new_user=new_user)

@pytest.fixture
async def test_user4(db: Database) -> UserInDB:
    new_user = UserCreate(email='jennifer@lopez.io', username='jlo', password='jennyfromtheblock')
    return await user_fixture_factory(db=db, new_user=new_user)

@pytest.fixture
async def test_user5(db: Database) -> UserInDB:
    new_user = UserCreate(email='bruce@lee.io', username='brucelee', password='martialarts')
    return await user_fixture_factory(db=db, new_user=new_user)

@pytest.fixture
async def test_user6(db: Database) -> UserInDB:
    new_user = UserCreate(email='kal@penn.io', username='kalpenn', password='haroldandkumar')
    return await user_fixture_factory(db=db, new_user=new_user)

@pytest.fixture
async def test_user_list(
    test_user3: UserInDB, test_user4: UserInDB, test_user5: UserInDB, test_user6: UserInDB,
) -> List[UserInDB]:
    return [test_user3, test_user4, test_user5, test_user6]

@pytest.fixture
def create_authorized_client(client: AsyncClient) -> Callable:
    def _create_authorized_client(*, user: UserInDB) -> AsyncClient:
        access_token = auth_service.create_access_token_for_user(user=user, secret_key=str(SECRET_KEY))
        client.headers = {
            **client.headers,
            'Authorization': f'{JWT_TOKEN_PREFIX} {access_token}'
        }
        return client
    return _create_authorized_client

@pytest.fixture
async def test_team_with_members(db: Database, test_user2: UserInDB, test_user_list: List[UserInDB]) -> TeamInDB:
    teams_repo = TeamsRepository(db)
    members_repo = MembersRepository(db)
    new_team = TeamCreate(
        name='team with members',
        description='desc for team'
    )
    created_team = await teams_repo.create_team(new_team=new_team, requesting_user=test_user2)
    for user in test_user_list:
        await members_repo.create_member_for_team(
            new_member=MemberCreate(
                team_id=created_team.id,
                user_id=user.id
            )
        )
    return created_team

async def task_fixture_factory(*, db: Database, user: UserInDB, new_task: TaskCreate):
    task_repository = TasksRepository(db)
    return await task_repository.create_task(new_task=new_task, requesting_user=user)

@pytest.fixture
async def test_task(db: Database, test_project: ProjectInDB, test_user: UserInDB) -> TaskInDB:
    new_task = TaskCreate(
        name='fake task name',
        description='fake task description',
        cost=1,
        status='to_do',
        project_id=test_project.id,
        user_id=test_user.id
    )
    return await task_fixture_factory(db=db, user=test_user, new_task=new_task)

@pytest.fixture
async def test_task2(db: Database, test_project: ProjectInDB, test_user: UserInDB) -> TaskInDB:
    new_task = TaskCreate(
        name='fake task 2',
        description='fake task description',
        cost=1,
        status='to_do',
        project_id=test_project.id
    )
    return await task_fixture_factory(db=db, user=test_user, new_task=new_task)

@pytest.fixture
async def test_task3(db: Database, test_project: ProjectInDB, test_user: UserInDB) -> TaskInDB:
    new_task = TaskCreate(
        name='fake task 3',
        description='fake task description',
        cost=1,
        status='to_do',
        project_id=test_project.id
    )
    return await task_fixture_factory(db=db, user=test_user, new_task=new_task)

@pytest.fixture
async def test_task4(db: Database, test_project: ProjectInDB, test_user: UserInDB) -> TaskInDB:
    new_task = TaskCreate(
        name='fake task 4',
        description='fake task description',
        cost=1,
        status='to_do',
        project_id=test_project.id
    )
    return await task_fixture_factory(db=db, user=test_user, new_task=new_task)    
