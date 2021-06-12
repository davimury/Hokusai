from typing import List
from fastapi import APIRouter, WebSocket
from models import User
from db.db_main import Session, USERS

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.connections: List[User] = []

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()

        try:
            session = Session()
            user = session.query(USERS).filter_by(user_id=client_id).first()
        except:
            pass
        
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    while True:
        data = await websocket.receive_text()
        await manager.broadcast(f"Client {client_id}: {data}")