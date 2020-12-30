from typing import List, Union
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status, Header, Query
from fastapi.websockets import WebSocket
from fastapi.responses import FileResponse
from app.models.users import UserInDB
from app.db.repositories.tasks import TasksRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_active_user
import os

router = APIRouter()

@router.websocket('/tasks')
async def tasks_ws(
    websocket: WebSocket,
    ticket: str = Query(...),
    # dep: TasksRepository = Depends(get_repository(TasksRepository))
):
    await websocket.accept()
    await websocket.send_text('aaa')
    # websocket.send_text(ticket)
    # websocket.close()