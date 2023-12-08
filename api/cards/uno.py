from enum import Enum

from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)


class Colours(Enum):
    YELLOW = "yellow"
    RED = "red"
    BLUE = "blue"
    GREEN = "green"

    def colours(game_object) -> list:
        return [colour.value for colour in Colours]


class Card:
    def __init__(self, colour: Colours, action: str, card_type):
        self._colour = colour.value if colour else None
        self.action = action
        self.card_type = card_type
        self.deck = None
        self.face_value = {"action": self.action, "colour": self._colour}

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, new_colour):
        self._colour = new_colour
        self.face_value["colour"] = new_colour  # Update face value if needed

    def is_playable(self):
        discard_pile = self.deck.discard_pile
        if discard_pile:
            discard = discard_pile[-1]
            # if the discard is a wild card
            if not discard.colour:
                return True
            return (self.colour == discard.colour or self.action == discard.action) or not self.colour


class Number(Card):
    """A number side of a card.

    Attributes:
        colour (Colour): The colour of the card.
        action (str): The action text of the card.
        card_type (type): The type of the card.
        score (int): The score of the card.
    """

    def __init__(self, colour: Colours, action: str):
        super().__init__(colour, action, self.__class__)
        self.score = int(action)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")


class Skip(Card):

    score = 20

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        game.players.increment_turn()


class Reverse(Card):

    score = 20

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        game.direction *= -1
        game.players.increment_turn()
        game.players.increment_turn()


class DrawTwo(Card):

    score = 20

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")

        for _ in range(2):
            player_hand = game.players.current_player.hand
            player_hand.append(game.deck.pick_card())
        game.players.increment_turn()


class Wild(Card):

    score = 40

    def __init__(self):
        super().__init__(None, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")


class WildDrawFour(Card):

    score = 50

    def __init__(self):
        super().__init__(None, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")

        for _ in range(4):
            player_hand = game.players.current_player.hand
            player_hand.append(game.deck.pick_card())
        game.players.increment_turn()

cards = [
    Number(Colours.YELLOW, "1"),
    Number(Colours.YELLOW, "1"),
    Number(Colours.YELLOW, "2"),
    Number(Colours.YELLOW, "2"),
    Number(Colours.YELLOW, "3"),
    Number(Colours.YELLOW, "3"),
    Number(Colours.YELLOW, "4"),
    Number(Colours.YELLOW, "4"),
    Number(Colours.YELLOW, "5"),
    Number(Colours.YELLOW, "5"),
    Number(Colours.YELLOW, "6"),
    Number(Colours.YELLOW, "6"),
    Number(Colours.YELLOW, "7"),
    Number(Colours.YELLOW, "7"),
    Number(Colours.YELLOW, "8"),
    Number(Colours.YELLOW, "8"),
    Number(Colours.YELLOW, "9"),
    Number(Colours.YELLOW, "9"),
    Number(Colours.YELLOW, "0"),
    
    Number(Colours.RED, "1"),
    Number(Colours.RED, "1"),
    Number(Colours.RED, "2"),
    Number(Colours.RED, "2"),
    Number(Colours.RED, "3"),
    Number(Colours.RED, "3"),
    Number(Colours.RED, "4"),
    Number(Colours.RED, "4"),
    Number(Colours.RED, "5"),
    Number(Colours.RED, "5"),
    Number(Colours.RED, "6"),
    Number(Colours.RED, "6"),
    Number(Colours.RED, "7"),
    Number(Colours.RED, "7"),
    Number(Colours.RED, "8"),
    Number(Colours.RED, "8"),
    Number(Colours.RED, "9"),
    Number(Colours.RED, "9"),
    Number(Colours.RED, "0"),

    Number(Colours.BLUE, "1"),
    Number(Colours.BLUE, "1"),
    Number(Colours.BLUE, "2"),
    Number(Colours.BLUE, "2"),
    Number(Colours.BLUE, "3"),
    Number(Colours.BLUE, "3"),
    Number(Colours.BLUE, "4"),
    Number(Colours.BLUE, "4"),
    Number(Colours.BLUE, "5"),
    Number(Colours.BLUE, "5"),
    Number(Colours.BLUE, "6"),
    Number(Colours.BLUE, "6"),
    Number(Colours.BLUE, "7"),
    Number(Colours.BLUE, "7"),
    Number(Colours.BLUE, "8"),
    Number(Colours.BLUE, "8"),
    Number(Colours.BLUE, "9"),
    Number(Colours.BLUE, "9"),
    Number(Colours.BLUE, "0"),

    Number(Colours.GREEN, "1"),
    Number(Colours.GREEN, "1"),
    Number(Colours.GREEN, "2"),
    Number(Colours.GREEN, "2"),
    Number(Colours.GREEN, "3"),
    Number(Colours.GREEN, "3"),
    Number(Colours.GREEN, "4"),
    Number(Colours.GREEN, "4"),
    Number(Colours.GREEN, "5"),
    Number(Colours.GREEN, "5"),
    Number(Colours.GREEN, "6"),
    Number(Colours.GREEN, "6"),
    Number(Colours.GREEN, "7"),
    Number(Colours.GREEN, "7"),
    Number(Colours.GREEN, "8"),
    Number(Colours.GREEN, "8"),
    Number(Colours.GREEN, "9"),
    Number(Colours.GREEN, "9"),
    Number(Colours.GREEN, "0"),
    
    DrawTwo(Colours.YELLOW),
    DrawTwo(Colours.YELLOW),
    DrawTwo(Colours.RED),
    DrawTwo(Colours.RED),
    DrawTwo(Colours.BLUE),
    DrawTwo(Colours.BLUE),
    DrawTwo(Colours.GREEN),
    DrawTwo(Colours.GREEN),
    
    Skip(Colours.YELLOW),
    Skip(Colours.YELLOW),
    Skip(Colours.RED),
    Skip(Colours.RED),
    Skip(Colours.BLUE),
    Skip(Colours.BLUE),
    Skip(Colours.GREEN),
    Skip(Colours.GREEN),
    
    Reverse(Colours.YELLOW),
    Reverse(Colours.YELLOW),
    Reverse(Colours.RED),
    Reverse(Colours.RED),
    Reverse(Colours.BLUE),
    Reverse(Colours.BLUE),
    Reverse(Colours.GREEN),
    Reverse(Colours.GREEN),

    Wild(),
    Wild(),
    Wild(),
    Wild(),

    WildDrawFour(),
    WildDrawFour(),
    WildDrawFour(),
    WildDrawFour(),
]
