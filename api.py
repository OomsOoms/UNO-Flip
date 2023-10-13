from fastapi import FastAPI
from pydantic import BaseModel

from game import Game

# Game ID: game object
games = {}

# run using uvicorn api:app --reload --port 8000
app = FastAPI()

class CreateGameRequest(BaseModel):
    player_name: str

class JoinGameRequest(BaseModel):
    game_id: int
    player_name: str

@app.get("/")
async def root():
    return "Online"

# It is assumed user ID is already in the session data
@app.post("/create_game")
async def create_game(create_game_request: CreateGameRequest):
    game = Game()
    games[game.game_id] = game
    player_name = create_game_request.player_name
    player_id = game.add_player(player_name)
    return {"game_id": game.game_id, "player_id": player_id}
    
# It is assumed user ID is already in the session data
@app.post("/join_game")
async def join_game(join_id_request: JoinGameRequest):
    game_id = join_id_request.game_id
    if game_id in games:
        player_name = join_id_request.player_name
        game = games[game_id]
        # Unique to every game
        player_id = game.add_player(player_name)
        return {"game_id": game.game_id, "player_id": player_id}

