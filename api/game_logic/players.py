from uuid import uuid4

from utils.custom_logger import CustomLogger

from cards import Type, Colour, Card, FlipCard

logger = CustomLogger(__name__)


class Player:
    """Represents a player in the game.

    Attributes:
        name (str): The name of the player.
        game (Game): The game the player is in.
        hand (list): A list of cards in the player's hand.

    Properties:
        score (int): The score of the player's hand.
    """
    hand: Card | FlipCard = []

    def __init__(self, name, game):
        self.name = name
        self.id = str(uuid4())
        self.game = game
        self.score = 0

    def assign_hand(self, hand_size):
        """Assigns a hand of cards to the player.

        Args:
            hand_size (int): The number of cards to deal.
        """
        self.hand = self.game.deck.deal(hand_size)


class Players:

    def __init__(self, game):
        self.game = game
        self.players = {}
        self.current_player_index = 0

    @property
    def current_player_id(self) -> str:
        return list(self.players.keys())[self.current_player_index]

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_id]

    def increment_turn(self) -> None:
        self.current_player_index = (
            self.current_player_index + self.game.direction) % len(self.players)

    def add_player(self, player_name: str) -> str:
        logger.info(f"Adding {player_name} to game {self.game.game_id}")
        player = Player(player_name, self.game)
        self.players[player.id] = player
        return player.id

    def remove_player(self, player_id: str) -> None:
        logger.info(f"Removing {player_id} from game {self.game.game_id}")

        player = self.players.get(player_id)

        if not player:
            return

        if self.game.direction:
            if list(self.players.keys()).index(player_id) < self.current_player_index:
                self.current_player_index -= 1
            if self.current_player_index >= len(self.players)-1:
                self.current_player_index = 0

        # TODO: RESET WILD CARDS COLOUR
        self.game.deck.cards += player.hand
        del self.players[player_id]

    # Allows the Players object to be used like a dictionary
    def __getitem__(self, player_id: str):
        return self.players[player_id]
    
    def get (self, player_id: str):
        return self.players.get(player_id)

    def items(self):
        return self.players.items()

    def values(self):
        return self.players.values()

    def keys(self):
        return self.players.keys()

    def __len__(self):
        return len(self.players)
