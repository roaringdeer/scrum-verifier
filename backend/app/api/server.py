from fastapi import FastAPI
from fastapi.websockets import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.core import config, tasks
from app.utils.websockets import WebSocketManager
from app.api.routes import router as api_router

def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    app.add_event_handler('startup', tasks.create_start_app_handler(app))
    app.add_event_handler('shutdown', tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix='/api')

    return app

app = get_application()

@app.get("/")
async def read_main():
    return {"msg": "This is Scrum-Verifier API"}

# @app.websocket_route("/ws")
# async def websocket(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_json({"msg": "Hello WebSocket"})
#     await websocket.close()