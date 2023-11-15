from fastapi import WebSocket
from typing import Dict

from api.game import Game
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

    async def broadcast(self, message: dict, game_id: int):
        for connection, [conn_game_id, conn_player_id] in self.active_connections.items():
            if conn_game_id == game_id:
                await connection.send_json(message)
                logger.debug(f"Sent message {message} to websocket {connection.client}")

    async def broadcast_gamestate(self, game_object: Game):
        logger.debug(f"Broadcasting gamestate for game {game_object.game_id}")
        for connection, [conn_game_id, conn_player_id] in self.active_connections.items():
            if conn_game_id == game_object.game_id:
                await connection.send_json(game_object.get_game_state(conn_player_id))
