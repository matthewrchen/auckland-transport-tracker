from fastapi import WebSocket
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_to_all(self, payload: dict):
        if not self.active_connections:
            return
        await asyncio.gather(
            *[client.send_json(payload) for client in self.active_connections],
            return_exceptions=True
        )

websocket_manager = ConnectionManager()