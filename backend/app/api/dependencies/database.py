from typing import Callable, Type
from databases import Database
from fastapi import Depends
from fastapi.websockets import WebSocket
from starlette.requests import Request
from app.db.repositories.base import BaseRepository

def get_database(request: Request) -> Database:
    return request.app.state._db

def get_repository(repository_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        return repository_type(db)
    return get_repo

def get_database_ws(websocket: WebSocket) -> Database:
    return websocket.app.state._db

def get_repository_ws(repository_type: Type[BaseRepository]) -> Callable:
    def get_repo_ws(db: Database = Depends(get_database_ws)) -> Type[BaseRepository]:
        return repository_type(db)
    return get_repo_ws