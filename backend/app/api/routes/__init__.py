from fastapi import APIRouter
from app.api.routes.tasks import router as tasks_router
from app.api.routes.users import router as users_router
from app.api.routes.profiles import router as profiles_router
from app.api.routes.projects import router as projects_router
from app.api.routes.teams import router as teams_router
from app.api.routes.members import router as members_router
from app.api.routes.events import router as events_router
from app.api.routes.files import router as files_router
from app.api.routes.websockets import router as websocket_router

router = APIRouter()

router.include_router(users_router, prefix='/users', tags=['users'])
router.include_router(profiles_router, prefix='/profiles', tags=['profiles'])
router.include_router(teams_router, prefix='/teams', tags=['teams'])
router.include_router(members_router, prefix='/teams/{team_id}/members', tags=['members'])
router.include_router(projects_router, prefix='/projects', tags=['projects'])
router.include_router(tasks_router, prefix='/tasks', tags=['tasks'])
router.include_router(events_router, prefix='/events', tags=['events'])
router.include_router(files_router, prefix='/files', tags=['files'])
router.include_router(websocket_router, prefix='/websockets', tags=['websockets'])

