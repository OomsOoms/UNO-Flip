from fastapi import FastAPI, HTTPException, status, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Union # Used when a function can return multiple types

from api.game import Game
from api.request_model import *
from api.connection_manager import ConectionManager
from utils.custom_logger import CustomLogger

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

manager = ConectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client says: {data}")
    except Exception as e:
        logger.error(e)
    finally:
        manager.disconnect(websocket)

@app.get("/connected_websockets")
async def get_connected_websockets():
    return {"connected_websockets": [str(ws.client) for ws in manager.active_connections]}


@app.get("/")
async def root():
    """
    Endpoint to check if the API is online

    Returns:
        str: A message indicating that the API is online
    """
    return "Online"


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
    logger.debug(f"Created game {game.game_id} with player {player_id}")
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
        logger.debug(f"Game {join_id_request.game_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    if game.started:
        logger.debug(f"Game {join_id_request.game_id} has already started")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game has already started")

    if len(game.players) >= 10:
        logger.debug(f"Game {join_id_request.game_id} is full")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Game is full")

    # Add the player to the game and get their ID
    player_id = game.add_player(player_name)
    
    return JSONResponse(content={"game_id": game.game_id, "player_id": player_id}, status_code=status.HTTP_201_CREATED)


@app.post("/lobby")
async def lobby(lobby_request: LobbyRequest) -> Union[dict, None]:
    """
    Handles lobby-related requests.

    Retrieves player names and host status based on the lobby request

    Args:
        lobby_request (LobbyRequest): The lobby request object

    Returns:
        dict: A dictionary containing player names and host status

    Raises:
        HTTPException: If lobby_request.game_id is not found in the games dictionary or if the player is not in this game
    """
    player_id = lobby_request.player_id

    game = games.get(lobby_request.game_id)
    
    if game is None or player_id not in game.players:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request to fetch lobby")
    
    is_host = next(iter(game.players)) == player_id
    player_names = [player.name for player in game.players.values()]
    logger.debug(f"Player {player_id} requested lobby for game {game.game_id}")
    return JSONResponse(content={"player_names": player_names, "is_host": is_host}, status_code=status.HTTP_200_OK)


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
    game = games.get(start_game_request.game_id)
        
    if game.started or list(game.players.keys())[0] != start_game_request.player_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request to start the game")

    elif len(game.players) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough players to start the game")
    # Set game.started to True to prevent new players from joining and select a card and player
    game.start_game()
    return True


@app.post("/get_game_state")
async def get_game_state(game_state_request: GetGameStateRequest) -> Union[dict, None]:
    """
    Handles requests to get the game state.

    Args:
        game_state_request (GetGameStateRequest): The game state request object.

    Returns:
        dict or None: A dictionary containing the game state for the specified player.

    Raises:
        HTTPException: If there's an invalid request to start the game or the game is not found.
    """
    player_id = game_state_request.player_id
    
    game = games.get(game_state_request.game_id)
    
    if game.started and player_id in game.players:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request to start the game")
    
    return game.get_game_state(player_id)

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
