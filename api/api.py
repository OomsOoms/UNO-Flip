from fastapi import FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Union # Used when a function can return multiple types

from api.game import Game
from api.request_model import *
from api.connection_manager import ConectionManager
from utils.custom_logger import CustomLogger
import asyncio

# Run with logging:
# uvicorn api.api:app --reload --host 0.0.0.0
# Run without logging:
# uvicorn api.api:app --reload --host 0.0.0.0 --log-level critical
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

@app.get("/admin_stats")
async def admin_stats():
    """
    Admin page
    """
    game_stats = []
    for game_id, game_object in games.items():
        players = {player_id: player_object.name for player_id, player_object in game_object.players.items()}
        game_stat = {
            "gameId": game_id,
            "players": players,
            "host": list(players.keys())[0],
            "currentPlayerIndex": game_object.current_player_index,
            "currentPlayerId": game_object.current_player_id,
            "deckLength": len(game_object.deck.cards),
            "discardLength": len(game_object.deck.discard),
            "discardTop": game_object.deck.discard[-1] if len(game_object.deck.discard) else None,
            "gameDirection": game_object.game_direction,
            "gameFlip": game_object.deck.flip,
            "gameStarted": str(game_object.started)
        }
        game_stats.append(game_stat)

    websocket_stats = {}
    for connection_id, (game_id, player_id) in manager.active_connections.items():
        websocket_stats[f"{str(connection_id.client[0])}:{str(connection_id.client[1])}"] = {"gameId": game_id, "playerId": player_id}
    return {
        "gameStats": game_stats,
        "websocketStats": websocket_stats
    }
    

@app.websocket("/lobby")
async def lobby(websocket: WebSocket, game_id: int, player_id: str):
    """
    Endpoint for the websocket connection to the lobby
    """
    game_object = games.get(game_id)

    if game_object and (player_id in game_object.players):
        await manager.connect(websocket, game_id, player_id)
        await websocket.send_json(game_object.get_game_state(player_id))
    else:
        await websocket.close()
        return
    
    try:
        message = await websocket.receive_json()
        logger.debug(f"Received message: {message}")
        #game_object.play_card(player_id, int(message["card_index"]))
        #await manager.broadcast_gamestate(game_object)

    # Only runs when an authenticated websocket disconnects
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # Provides a 5 second window for the player to reconnect
        await asyncio.sleep(5)
        if [game_id, player_id] not in list(manager.active_connections.values()):
            if game_object.players.get(player_id):
                game_object.remove_player(player_id)
                if not len(game_object.players):
                    del games[game_id]
                    logger.debug(f"Deleting game {game_id} because thre are no players left")
                else:
                    await manager.broadcast_gamestate(game_object)
    
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
    game_object = Game()
    games[game_object.game_id] = game_object
    player_id = game_object.add_player(player_name)
    return JSONResponse(content={"game_id": game_object.game_id, "player_id": player_id}, status_code=status.HTTP_201_CREATED)

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
    game_object = games.get(join_id_request.game_id)
    player_name = join_id_request.player_name

    if game_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    if game_object.started:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game has already started")

    if len(game_object.players) >= 10:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Game is full")

    # Add the player to the game and get their ID
    player_id = game_object.add_player(player_name)
    await manager.broadcast_gamestate(game_object)
    return JSONResponse(content={"game_id": game_object.game_id, "player_id": player_id}, status_code=status.HTTP_201_CREATED)

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
    await manager.broadcast_gamestate(game_object)   
    return JSONResponse(content={"detail": "Game started", "started": True}, status_code=status.HTTP_200_OK) 

@app.post("/select_card")
async def select_card(select_card_request: SelectCardRequest) -> Union[dict, None]:
    player_id = SelectCardRequest.player_id
    
    game_object = games.get(SelectCardRequest.game_id)
    
    if game_object.started and player_id != game_object.current_player_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request to start the game")
    # TODO: Check if card is playable after selecting it, only playable cards can be selected but its just a check
    # TODO: Pick up card if no cards are playable

# TODO: endpoint for Calling uno, calling uno on someone else
# TODO: endpoint Card behaviour (prequisite_func)
# TODO: ending a turn, call at the end of select card for now, will give seperate endpoint later if needed
