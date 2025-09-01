from typing import Dict

from fastapi import WebSocket, WebSocketDisconnect


class ChatManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, group_id: int, user_id: int):
        await websocket.accept()

        if not group_id in self.active_connections:
            self.active_connections[group_id] = {}
        self.active_connections[group_id][user_id] = websocket
