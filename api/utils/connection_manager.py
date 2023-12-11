"""The module is a connection manager for managing websocket connections in a game.

This module provides a ConnectionManager class that is responsible for managing websocket connections in a game. It allows for connecting and disconnecting websockets, as well as broadcasting the game state to all connected websockets.

Classes:
    ConnectionManager: Class to manage the websocket connections.

Functions:
    connect: Method to connect a websocket to the connection manager.
    disconnect: Method to disconnect a websocket from the connection manager.
    broadcast_gamestate: Method to broadcast the game state to all websockets in a game.
"""

from fastapi import WebSocket
from typing import Dict

from game_logic.game import Game
from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)


class ConectionManager:
    """Class to manage the websocket connections.

    Attributes:
        active_connections (Dict[WebSocket, list]): A dictionary with the websocket connections as keys and a list with the game ID and player ID as values
    """

    def __init__(self):
        """Constructor method for the ConnectionManager class.

        Initializes the active_connections attribute as an empty dictionary.
        """
        self.active_connections: Dict[WebSocket, list] = {}

    async def connect(self, websocket: WebSocket, game_id: int, player_id: str):
        """Method to connect a websocket to the connection manager.

        Adds the websocket to the active_connections dictionary.

        Args:
            websocket (WebSocket): The websocket connection
            game_id (int): The ID of the game
            player_id (str): The ID of the player
        """
        await websocket.accept()
        self.active_connections[websocket] = [game_id, player_id]
        logger.debug(
            f"Accepted and added websocket {websocket.client} to active connections")

    def disconnect(self, websocket: WebSocket):
        """Method to disconnect a websocket from the connection manager.

        Removes the websocket from the active_connections dictionary.

        Args:
            websocket (WebSocket): The websocket connection
        """
        self.active_connections.pop(websocket, None)
        logger.debug(
            f"Removed websocket {websocket.client} from active connections")

    async def broadcast_gamestate(self, game: Game):
        """Method to broadcast the game state to all websockets in a game.

        Args:
            game (Game): The game object to broadcast
        """
        logger.debug(f"Broadcasting gamestate for game {game.game_id}")
        for connection, [conn_game_id, conn_player_id] in self.active_connections.items():
            if conn_game_id == game.game_id:
                await connection.send_json(game.get_game_state(conn_player_id))

    async def broadcast(self, game: Game, message: str):
        """Method to broadcast a message to all websockets in a game.

        Args:
            game (Game): The game object to broadcast
            message (str): The message to broadcast
        """
        logger.debug(f"Broadcasting message for game {game.game_id}")
        for connection, [conn_game_id, conn_player_id] in self.active_connections.items():
            if conn_game_id == game.game_id:
                await connection.send_json({"type": "message", "message": message})
