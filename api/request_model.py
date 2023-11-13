from pydantic import BaseModel

# TODO: combinr identical requests into one class
class CreateGameRequest(BaseModel):
    player_name: str

class JoinGameRequest(BaseModel):
    game_id: int
    player_name: str

class LobbyRequest(BaseModel):
    game_id: int
    player_id: str

class StartGameRequest(BaseModel):
    game_id: int
    player_id: str

class GetGameStateRequest(BaseModel):
    game_id: int
    player_id: str

class SelectCardRequest(BaseModel):
    game_id: int
    player_id: str
    card_index: int
    