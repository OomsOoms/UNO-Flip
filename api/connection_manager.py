from fastapi import WebSocket
from typing import Dict

from utils.custom_logger import CustomLogger
logger = CustomLogger(__name__)


class ConectionManager:

    def __init__(self):
        self.active_connections: Dict[WebSocket, list] = {}

    async def connect(self, websocket: WebSocket, game_id: int, player_id: str):
        await websocket.accept()
        self.active_connections[websocket] = [game_id, player_id]

    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket, None)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        logger.debug(f"Sent message {message} to websocket {websocket.client}")


    async def broadcast(self, message: str, game_id: int):
        for connection, [conn_game_id, conn_player_id] in self.active_connections.items():
            if conn_game_id == game_id:
                await connection.send_text(message)
                logger.debug(f"Sent message {message} to websocket {connection.client}")
