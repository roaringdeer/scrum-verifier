import string, random
from datetime import datetime, timedelta
from fastapi.websockets import WebSocket, WebSocketDisconnect
from typing import List


class WebSocketManager:
    def __init__(self):
        self.active_connections = {} # key - project_id, value - list of websockets
        self.tickets = {}
        self.tickets_exp_timedelta = timedelta(minutes=1)
    
    def create_new_ticket(self, requesting_user):
        ticket = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
        self.tickets[ticket] = {'time': datetime.now(), 'user_id': requesting_user.id}
        return ticket
    
    def consume_ticket(self, ticket):
        if len(self.tickets) > 1000:
            self.cleanup_tickets()
        if ticket in self.tickets:
            if self.tickets[ticket]['time'] + self.tickets_exp_timedelta > datetime.now():
                return self.tickets[ticket]['user_id']
        return None

    async def cleanup_tickets(self):
        now = datetime.now()
        for ticket, exp_date in self.tickets.items():
            if exp_date + self.tickets_exp_timedelta > now:
                del self.tickets[ticket]

    async def connect(self, websocket: WebSocket, project_id: int):
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = [websocket]
        else:
            self.active_connections[project_id].append(websocket)

    def disconnect(self, websocket: WebSocket, project_id: int):
        self.active_connections[project_id].remove(websocket)

    async def broadcast_text(self, message: str, project_id: int):
        for connection in self.active_connections[project_id]:
            await connection.send_text(message)

    async def broadcast_json(self, json: dict, project_id: int):
        for connection in self.active_connections[project_id]:
            await connection.send_json(json)