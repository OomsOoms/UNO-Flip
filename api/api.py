from fastapi import FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Union # Used when a function can return multiple types

from api.game import Game
from api.request_model import *
from api.connection_manager import ConectionManager
from utils.custom_logger import CustomLogger
import asyncio

# Create a FastAPI instance, run using: uvicorn api.api:app --reload --host 0.0.0.0
app = FastAPI(title="UNO API", description="API for the UNO Flip game", version="0.1.0")

# Add the CORSMiddleware to the FastAPI instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a logger instance
logger = CustomLogger(__name__)

# Dictionary to store game objects with their IDs as keys
games = {}

# Create a connection manager instance to manage the websocket connections
manager = ConectionManager()

@app.get("/")
async def root():
    """
    Endpoint to check if the API is online

    Returns:
        str: A message indicating that the API is online
    """
    return "Online"

@app.websocket("/lobby")
async def websocket_endpoint(websocket: WebSocket, game_id: int, player_id: str):
    """
    Endpoint for the websocket connection
    
    This function handles the websocket connection for the lobby. It receives the websocket, game_id and player_id as parameters.
    It connects the websocket to the manager, and sends the game state to the active connections.
    It also sends the lobby information to the active connections.
    It handles the received data and disconnects the websocket if necessary.
    
    :param websocket: WebSocket object
    :param game_id: int representing the game id
    :param player_id: str representing the player id
    """
    game_object = games.get(game_id)
    if game_object and player_id in game_object.players:
        await manager.connect(websocket, game_id, player_id)
        logger.debug(f"Connected websocket {websocket.client}")

        await manager.update_lobby(game_object)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request to fetch lobby")
        

    try:
        while True:
            received_data = await websocket.receive_text()
            # TODO: Handle received data, this data will be actions in game
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.debug("Disconnecting websocket in 5 seconds if not reconnected")
        await asyncio.sleep(5)

        if not any(conn_game_id == game_id and conn_player_id == player_id for conn_game_id, conn_player_id in manager.active_connections.values()):
            game_object.players.pop(player_id, None)
            logger.debug(f"Disconnected websocket {websocket.client} for game {game_id} and player {player_id}")
            if not game_object.players:
                games.pop(game_id, None)
                logger.debug(f"Removed game {game_id} because there are no players left")
            await manager.update_lobby(game_object)

@app.get("/connected_websockets")
async def get_connected_websockets():
    """
    Endpoint for getting the connected websockets

    Returns:
        dict: A dictionary containing the connected websockets
    """
    connections = str(manager.active_connections)
    return connections

@app.post("/create_game")
async def create_game(create_game_request: CreateGameRequest) -> dict:
    """
    Create a new game and add a player

    Args:
        create_game_request (CreateGameRequest): Request model for creating a game
        
    Returns:
        dict: {'game_id': str, 'player_id': str} representing the game and player IDs.
    """
    player_name = create_game_request.player_name
    game = Game()
    games[game.game_id] = game
    player_id = game.add_player(player_name)
    return JSONResponse(content={"game_id": game.game_id, "player_id": player_id}, status_code=status.HTTP_201_CREATED)

@app.post("/join_game")
async def join_game(join_id_request: JoinGameRequest) -> Union[dict, None]:
    """
    Endpoint for joining a game.

    Args:
        join_id_request (JoinGameRequest): The request model for joining a game

    Returns:
        Union[dict, None]: A dictionary containing the game ID and player ID
    
    Raises:
        HTTPException: If game is not found, game has already started or game is full
    """
    # Retrieve the game and player name from the request
    game = games.get(join_id_request.game_id)
    player_name = join_id_request.player_name

    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    if game.started:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game has already started")

    if len(game.players) >= 10:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Game is full")

    # Add the player to the game and get their ID
    player_id = game.add_player(player_name)
    return JSONResponse(content={"game_id": game.game_id, "player_id": player_id}, status_code=status.HTTP_201_CREATED)

@app.post("/start_game")
async def start_game(start_game_request: StartGameRequest) -> Union[bool, None]:
    """
    Start a game if the player is the host and there are enough players

    Args:
        start_game_request (StartGameRequest): Request containing the game ID

    Returns:
        bool: True if the game is successfully started

    Raises:
        HTTPException: If the game, number of players or host player are invalid for starting the game
    """
    game_object = games.get(start_game_request.game_id)
    
    # Check if the game exists or has started and the player is the host
    if game_object.started or list(game_object.players.keys())[0] != start_game_request.player_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request to start the game")

    elif len(game_object.players) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough players to start the game")
    # Set game.started to True to prevent new players from joining and select a card and player
    game_object.start_game()
    logger.debug(f"Starting game {game_object.game_id} with {len(game_object.players)} players and host {start_game_request.player_id}")
    await manager.update_lobby(game_object)    

@app.post("/select_card")
async def select_card(select_card_request: SelectCardRequest) -> Union[dict, None]:
    player_id = SelectCardRequest.player_id
    
    game = games.get(SelectCardRequest.game_id)
    
    if game.started and player_id != game.current_player_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request to start the game")
    # TODO: Check if card is playable after selecting it, only playable cards can be selected but its just a check
    # TODO: Pick up card if no cards are playable

# TODO: endpoint for Calling uno, calling uno on someone else
# TODO: endpoint Card behaviour (prequisite_func)
# TODO: ending a turn, call at the end of select card for now, will give seperate endpoint later if needed
