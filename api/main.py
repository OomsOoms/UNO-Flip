"""API module for the UNO Flip game.

This module contains the FastAPI endpoints and websocket logic for the UNO Flip game.
It provides functionality for creating and joining games, starting games, playing cards,
and managing websocket connections.
"""

import asyncio

from fastapi import FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from game_logic.game import Game, GameState
from utils.request_model import *
from utils.connection_manager import ConectionManager
from utils.custom_logger import CustomLogger

# Run with logging:
# uvicorn main:app --reload --host 0.0.0.0
# Run without logging:
# uvicorn main:app --reload --host 0.0.0.0 --log-level critical
app = FastAPI(title="UNO API",
              description="API for the UNO Flip game", version="0.1.0")

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
    """Endpoint to check if the API is online.

    Returns:
        str: A message indicating that the API is online
    """
    return "Online"


@app.websocket("/lobby")
async def lobby(websocket: WebSocket, game_id: int, player_id: str):
    """Endpoint for the websocket connection to the lobby.

    Provies authentication for the websocket connection and handles the lobby logic, such as adding and removing players.
    It also broadcasts the game state to all players in the lobby.
    And it handles removing players and deleting the game if they are empty.

    Args:
        websocket (WebSocket): The websocket connection
        game_id (int): The ID of the game
        player_id (str): The ID of the player

    Raises:
        WebSocketDisconnect: If the websocket connection is closed
    """
    game = games.get(game_id)

    if game and game.players.get(player_id):
        await manager.connect(websocket, game_id, player_id)
        await websocket.send_json(game.get_game_state(player_id))
    else:
        await websocket.close()
        return
    try:
        while True:
            message = await websocket.receive_json()

            if message["type"] == "message":
                await manager.broadcast_message(game, message["message"])

            if game.state != GameState.GAME:
                continue
            
            match message["type"]:
                case "play_card":
                    if game.play_card(player_id, int(message["index"]), message["wildColour"]):
                        await manager.broadcast_gamestate(game)
                case "pick_card":
                    if game.pick_card(player_id):
                        await manager.broadcast_gamestate(game)
                case "call_uno":
                    if game.call_uno(player_id):
                        await manager.broadcast_gamestate(game)
                case _:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message type")

    # Only runs when an authenticated websocket disconnects
    except WebSocketDisconnect as e:

        # If the websocket is closed by the server, don't do anything
        if e.code == 1012:
            return

        manager.disconnect(websocket)
        # Wait 5 seconds to see if the player reconnects
        await asyncio.sleep(5)
        if [game_id, player_id] not in list(manager.active_connections.values()):
            if game.players[player_id]:
                game.players.remove_player(player_id)
                if not len(game.players):
                    logger.info(
                        f"Deleting game {game_id} because thre are no players left")
                    del games[game_id]
                else:
                    await manager.broadcast_gamestate(game)


@app.post("/create_game")
async def create_game(create_game_request: CreateGameRequest):
    """Create a new game and add a host player.

    Args:
        create_game_request (CreateGameRequest): Request model for creating a game

    Returns:
        JSONResponse: A JSON response containing the game ID and player ID
    """
    game = Game()
    player_name = create_game_request.player_name
    games[game.game_id] = game
    player_id = game.players.add_player(player_name)
    return JSONResponse(content={"game_id": game.game_id, "player_id": player_id}, status_code=status.HTTP_201_CREATED)


@app.post("/join_game")
async def join_game(join_id_request: JoinGameRequest):
    """Endpoint for joining a game.

    Args:
        join_id_request (JoinGameRequest): The request model for joining a game

    Returns:
        JSONResponse: A JSON response containing the game ID and player ID

    Raises:
        HTTPException: If game is not found, game has already started or game is full
    """
    game = games.get(join_id_request.game_id)
    player_name = join_id_request.player_name

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    if game.state != GameState.LOBBY:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Game has already started")

    if len(game.players) >= 10:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Game is full")

    player_id = game.players.add_player(player_name)
    await manager.broadcast_gamestate(game)
    return JSONResponse(content={"game_id": game.game_id, "player_id": player_id}, status_code=status.HTTP_201_CREATED)


@app.post("/start_game")
async def start_game(start_game_request: StartGameRequest):
    """Start a game if the player is the host and there are enough players.

    Args:
        start_game_request (StartGameRequest): Request containing the game ID

    Returns:
        JSONResponse: A JSON response containing a message and a boolean indicating if the game was started

    Raises:
        HTTPException: If the game, number of players or host player are invalid for starting the game
    """
    game = games.get(start_game_request.game_id)

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    if game.start_game(start_game_request.player_id):
        await manager.broadcast_gamestate(game)
        return JSONResponse(content={"detail": "Game started", "started": True}, status_code=status.HTTP_200_OK)


@app.get("/admin_stats")
async def admin_stats():
    """Retrieves the statistics for the admin page."""
    game_stats = []
    for game_id, game in games.items():
        players = {player_id: player.name for player_id,
                   player in game.players.items()}
        game_stats.append({
            "gameId": game_id,
            "players": players,
            "host": list(players.keys())[0],
            "currentPlayerIndex": game.players.current_player_index,
            "currentPlayerId": game.players.current_player_id,
            "deckLength": len(game.deck.cards),
            "discardLength": len(game.deck.discard_pile),
            "gameDirection": game.direction,
            "gameFlip": game.deck.flip,
            "gameStarted": str(game.state.value),
            "playerScores": (player.score for player_id, player in game.players.items())
        })

    websocket_stats = {}
    for connection_id, (game_id, player_id) in manager.active_connections.items():
        websocket_stats[f"{str(connection_id.client[0])}:{str(connection_id.client[1])}"] = {  # type: ignore
            "gameId": game_id, "playerId": player_id}
    return {
        "gameStats": game_stats,
        "websocketStats": websocket_stats
    }
