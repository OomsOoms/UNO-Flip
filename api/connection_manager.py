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

    async def update_lobby(self, game_object: Game):
        for connection, [conn_game_id, conn_player_id] in self.active_connections.items():
            if conn_game_id == game_object.game_id and game_object.started:     
                await connection.send_json({"type": "game_state", "game_state": game_object.get_game_state(conn_player_id)})
            else:   
                is_host = next(iter(game_object.players)) == conn_player_id
                player_names = [player.name for player in game_object.players.values()]
                await connection.send_json({"type": "lobby", "player_names": player_names, "is_host": is_host})
