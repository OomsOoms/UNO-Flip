from uuid import uuid4

from utils.custom_logger import CustomLogger

from cards import Type, Colour

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

    def __init__(self, name, game):
        self.name = name
        self.id = str(uuid4())
        self.game = game
        self.hand = game.deck.deal(7)
        self.score = 0

    def get_player_hand(self) -> list:
        """Returns the formatted hand of a player."""
        player_hand = [
            {
                "colour": card.colour,
                "action": card.action,
                "isPlayable": card.is_playable() and self.id == self.game.players.current_player_id
            }
            for card in self.hand
        ]
        return player_hand
    
    
class Bot(Player):
    """Represents a bot in the game.

    Attributes:
        name (str): The name of the bot.
        game (Game): The game the bot is in.
        hand (list): A list of cards in the bot's hand.

    Properties:
        score (int): The score of the bot's hand.
    """

    def __init__(self, name, game):
        super().__init__(name, game)

    def play(self):
        """Makes the bot play a card."""
        logger.info(f"Bot {self.name} is playing a card")
        hand = self.get_player_hand()

        logger.debug(f"Playable cards: {hand}")


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
    
    def add_bot(self, bot_name: str):
        logger.info(f"Adding bot {bot_name} to game {self.game.game_id}")
        bot = Bot(bot_name, self.game)
        self.players[bot.id] = bot

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
