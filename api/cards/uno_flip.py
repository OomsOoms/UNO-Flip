from enum import Enum

from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)


class Colour(Enum):
    YELLOW = "yellow"
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    ORANGE = "orange"
    PINK = "pink"
    PURPLE = "purple"
    TURQUOISE = "turquoise"

    @classmethod
    @property
    def LIGHT(cls):
        return [cls.YELLOW.value, cls.RED.value, cls.BLUE.value, cls.GREEN.value]
    
    @classmethod
    @property
    def DARK(cls):
        return [cls.ORANGE.value, cls.PINK.value, cls.PURPLE.value, cls.TURQUOISE.value]


class Side:
    """A side of a card. A card has two sides, a light side and a dark side.

    Attributes:
        colour (Colour): The colour of the card.
        action (str): The action text of the card.
        card_type (type): The type of the card. This is the class of the card.
    """

    def __init__(self, colour: Colour, action: str, card_type):
        self.colour = colour.value if colour else None
        self.action = action
        self.card_type = card_type


class Card:
    """A card in the game.

    The properties of the card are determined by the side that is face up.
    This allows the game to treat these 2 sided cards as a single card as in other versions.
    So the Side class in this case is a normal decks Card class.

    Attributes:
        light_side (Side): The light side of the card.
        dark_side (Side): The dark side of the card.
        deck (Deck): The deck the card is in.

    Properties: These mean that the card can be treated as a single card.
        score (int): The score of the card.
        action (str): The action text of the card.
        colour (Colour): The colour of the card.
        card_type (type): The type of the card.
    """

    def __init__(self, light_side: Side, dark_side: Side):
        self.light = light_side
        self.dark = dark_side
        # Only used for the UNO Flip! version of the game in properties
        self.deck = None

    @property
    def score(self):
        return self.light.score if self.deck.flip == 0 else self.dark.score

    @property
    def action(self):
        return self.light.action if self.deck.flip == 0 else self.dark.action

    @property
    def colour(self):
        return self.light.colour if self.deck.flip == 0 else self.dark.colour
    
    @colour.setter
    def colour(self, colour):
        if self.deck.flip == 0:
            self.light.colour = colour
        else:
            self.dark.colour = colour

    @property
    def face_value(self):
        return {"action": self.action, "colour": self.colour}

    @property
    def card_type(self):
        return self.light.card_type if self.deck.flip == 0 else self.dark.card_type

    def is_playable(self):
        discard_pile = self.deck.discard_pile
        if discard_pile:
            discard = discard_pile[-1]
            return (self.colour == discard.colour or self.action == discard.action) or not self.colour

    def behaviour(self, game):
        self.light.behaviour(
            game) if self.deck.flip == 0 else self.dark.behaviour(game)

    def __str__(self):
        return f"{self.colour.name} {self.action} {self.card_type.__name__}"


class Number(Side):
    """A number side of a card.

    This is the same for all the action cards.

    Attributes:
        colour (Colour): The colour of the card.
        action (str): The action text of the card.
        card_type (type): The type of the card.
        score (int): The score of the card.
    """

    def __init__(self, colour: Colour, action: str):
        super().__init__(colour, action, self.__class__)
        self.score = int(action)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")


class Flip(Side):

    score = 20

    def __init__(self, colour: Colour):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        # flip the deck attribute
        game.deck.flip = (game.deck.flip + 1) % 2
        # Reverse the discard pile
        game.deck.discard_pile = game.deck.discard_pile[::-1]


class Skip(Side):

    score = 20

    def __init__(self, colour: Colour):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        game.players.increment_turn()


class SkipEveryone(Side):

    score = 30

    def __init__(self, colour: Colour):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        # This cancels out the increment_turn() in the end_turn() method
        game.direction *= -1
        game.players.increment_turn()
        game.direction *= -1


class Reverse(Side):

    score = 20

    def __init__(self, colour: Colour):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        game.direction *= -1
        game.players.increment_turn()
        game.players.increment_turn()


class DrawOne(Side):

    score = 10

    def __init__(self, colour: Colour):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        player_hand = game.players.current_player.hand
        player_hand.append(game.deck.pick_card())
        game.players.increment_turn()


class DrawFive(Side):

    score = 20

    def __init__(self, colour: Colour):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        for _ in range(5):
            player_hand = game.players.current_player.hand
            player_hand.append(game.deck.pick_card())
        game.players.increment_turn()


class Wild(Side):

    score = 40

    def __init__(self):
        super().__init__(None, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        # TODO


class WildDrawTwo(Side):

    score = 50

    def __init__(self):
        super().__init__(None, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        # TODO


class WildDrawColour(Side):

    score = 60

    def __init__(self):
        super().__init__(None, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        # TODO


# TODO: Add the actual cards
cards = [
    Card(Number(Colour.YELLOW, "1"), SkipEveryone(Colour.PINK)),
    Card(Number(Colour.YELLOW, "1"), Wild()),
    Card(Number(Colour.YELLOW, "2"), Number(Colour.TURQUOISE, "1")),
    Card(Number(Colour.YELLOW, "2"), Number(Colour.TURQUOISE, "8")),
    Card(Number(Colour.YELLOW, "3"), Number(Colour.PURPLE, "1")),
    Card(Number(Colour.YELLOW, "3"), DrawFive(Colour.PINK)),
    Card(Number(Colour.YELLOW, "4"), DrawFive(Colour.PINK)),
    Card(Number(Colour.YELLOW, "4"), Flip(Colour.PURPLE)),
    Card(Number(Colour.YELLOW, "5"), Number(Colour.TURQUOISE, "8")),
    Card(Number(Colour.YELLOW, "5"), Number(Colour.PURPLE, "9")),
    Card(Number(Colour.YELLOW, "6"), SkipEveryone(Colour.ORANGE)),
    Card(Number(Colour.YELLOW, "6"), WildDrawColour()),
    Card(Number(Colour.YELLOW, "7"), Number(Colour.ORANGE, "2")),
    Card(Number(Colour.YELLOW, "7"), Number(Colour.PURPLE, "6")),
    Card(Number(Colour.YELLOW, "8"), Number(Colour.PINK, "1")),
    Card(Number(Colour.YELLOW, "8"), Number(Colour.ORANGE, "2")),
    Card(Number(Colour.YELLOW, "9"), Number(Colour.PURPLE, "4")),
    Card(Number(Colour.YELLOW, "9"), Number(Colour.TURQUOISE, "5")),

    Card(Number(Colour.RED, "1"), Number(Colour.PURPLE, "2")),
    Card(Number(Colour.RED, "1"), Number(Colour.PINK, "3")),
    Card(Number(Colour.RED, "2"), DrawFive(Colour.PURPLE)),
    Card(Number(Colour.RED, "2"), Reverse(Colour.ORANGE)),
    Card(Number(Colour.RED, "3"), Number(Colour.PINK, "7")),
    Card(Number(Colour.RED, "3"), WildDrawColour()),
    Card(Number(Colour.RED, "4"), DrawFive(Colour.PURPLE)),
    Card(Number(Colour.RED, "4"), Flip(Colour.ORANGE)),
    Card(Number(Colour.RED, "5"), Number(Colour.PINK, "2")),
    Card(Number(Colour.RED, "5"), Number(Colour.TURQUOISE, "5")),
    Card(Number(Colour.RED, "6"), Number(Colour.ORANGE, "9")),
    Card(Number(Colour.RED, "6"), SkipEveryone(Colour.PINK)),
    Card(Number(Colour.RED, "7"), Number(Colour.ORANGE, "1")),
    Card(Number(Colour.RED, "7"), Number(Colour.PURPLE, "5")),
    Card(Number(Colour.RED, "8"), Number(Colour.TURQUOISE, "7")),
    Card(Number(Colour.RED, "8"), Reverse(Colour.PURPLE)),
    Card(Number(Colour.RED, "9"), Number(Colour.PURPLE, "5")),
    Card(Number(Colour.RED, "9"), Reverse(Colour.TURQUOISE)),

    Card(Number(Colour.BLUE, "1"), SkipEveryone(Colour.PURPLE)),
    Card(Number(Colour.BLUE, "1"), SkipEveryone(Colour.PURPLE)),
    Card(Number(Colour.BLUE, "2"), Number(Colour.ORANGE, "8")),
    Card(Number(Colour.BLUE, "2"), Number(Colour.PINK, "6")),
    Card(Number(Colour.BLUE, "3"), Number(Colour.TURQUOISE, "2")),
    Card(Number(Colour.BLUE, "3"), Number(Colour.PURPLE, "8")),
    Card(Number(Colour.BLUE, "4"), DrawFive(Colour.TURQUOISE)),
    Card(Number(Colour.BLUE, "4"), Number(Colour.PURPLE, "1")),
    Card(Number(Colour.BLUE, "5"), Number(Colour.PINK, "9")),
    Card(Number(Colour.BLUE, "5"), Reverse(Colour.ORANGE)),
    Card(Number(Colour.BLUE, "6"), Reverse(Colour.PURPLE)),
    Card(Number(Colour.BLUE, "6"), SkipEveryone(Colour.TURQUOISE)),
    Card(Number(Colour.BLUE, "7"), Number(Colour.ORANGE, "3")),
    Card(Number(Colour.BLUE, "7"), SkipEveryone(Colour.ORANGE)),
    Card(Number(Colour.BLUE, "8"), Number(Colour.TURQUOISE, "4")),
    Card(Number(Colour.BLUE, "8"), Reverse(Colour.TURQUOISE)),
    Card(Number(Colour.BLUE, "9"), Number(Colour.ORANGE, "5")),
    Card(Number(Colour.BLUE, "9"), Flip(Colour.PURPLE)),

    Card(Number(Colour.GREEN, "1"), Number(Colour.ORANGE, "5")),
    Card(Number(Colour.GREEN, "1"), Flip(Colour.ORANGE)),
    Card(Number(Colour.GREEN, "2"), SkipEveryone(Colour.TURQUOISE)),
    Card(Number(Colour.GREEN, "2"), DrawFive(Colour.TURQUOISE)),
    Card(Number(Colour.GREEN, "3"), Number(Colour.PURPLE, "2")),
    Card(Number(Colour.GREEN, "3"), Flip(Colour.PINK)),
    Card(Number(Colour.GREEN, "4"), Number(Colour.TURQUOISE, "9")),
    Card(Number(Colour.GREEN, "4"), Number(Colour.PINK, "8")),
    Card(Number(Colour.GREEN, "5"), Number(Colour.TURQUOISE, "4")),
    Card(Number(Colour.GREEN, "5"), Number(Colour.ORANGE, "7")),
    Card(Number(Colour.GREEN, "6"), Number(Colour.PINK, "5")),
    Card(Number(Colour.GREEN, "6"), WildDrawColour()),
    Card(Number(Colour.GREEN, "7"), Number(Colour.TURQUOISE, "2")),
    Card(Number(Colour.GREEN, "7"), Number(Colour.ORANGE, "6")),
    Card(Number(Colour.GREEN, "8"), Number(Colour.TURQUOISE, "9")),
    Card(Number(Colour.GREEN, "8"), Reverse(Colour.PINK)),
    Card(Number(Colour.GREEN, "9"), DrawFive(Colour.PINK)),
    Card(Number(Colour.GREEN, "9"), Reverse(Colour.ORANGE)),

    Card(DrawOne(Colour.YELLOW), Number(Colour.PINK, "1")),
    Card(DrawOne(Colour.YELLOW), Number(Colour.PURPLE, "8")),
    Card(DrawOne(Colour.RED), Number(Colour.PINK, "3")),
    Card(DrawOne(Colour.RED), Number(Colour.PINK, "4")),
    Card(DrawOne(Colour.BLUE), Number(Colour.PINK, "6")),
    Card(DrawOne(Colour.BLUE), Number(Colour.TURQUOISE, "6")),
    Card(DrawOne(Colour.GREEN), Number(Colour.ORANGE, "6")),
    Card(DrawOne(Colour.GREEN), Number(Colour.TURQUOISE, "6")),

    Card(Reverse(Colour.YELLOW), Flip(Colour.TURQUOISE)),
    Card(Reverse(Colour.YELLOW), Wild()),
    Card(Reverse(Colour.RED), Number(Colour.PURPLE, "3")),
    Card(Reverse(Colour.RED), Number(Colour.TURQUOISE, "7")),
    Card(Reverse(Colour.BLUE), Number(Colour.ORANGE, "4")),
    Card(Reverse(Colour.BLUE), Wild()),
    Card(Reverse(Colour.GREEN), Number(Colour.ORANGE, "1")),
    Card(Reverse(Colour.GREEN), Number(Colour.PINK, "7")),

    Card(Flip(Colour.YELLOW), Number(Colour.PINK, "4")),
    Card(Flip(Colour.YELLOW), Number(Colour.ORANGE, "8")),
    Card(Flip(Colour.RED), Number(Colour.PURPLE, "3")),
    Card(Flip(Colour.RED), Number(Colour.PINK, "8")),
    Card(Flip(Colour.BLUE), Number(Colour.PURPLE, "6")),
    Card(Flip(Colour.BLUE), Number(Colour.PURPLE, "7")),
    Card(Flip(Colour.GREEN), Number(Colour.TURQUOISE, "3")),
    Card(Flip(Colour.GREEN), WildDrawColour()),

    Card(Skip(Colour.YELLOW), Number(Colour.ORANGE, "3")),
    Card(Skip(Colour.YELLOW), Flip(Colour.TURQUOISE)),
    Card(Skip(Colour.RED), DrawFive(Colour.ORANGE)),
    Card(Skip(Colour.RED), Wild()),
    Card(Skip(Colour.BLUE), Number(Colour.TURQUOISE, "1")),
    Card(Skip(Colour.BLUE), Number(Colour.PINK, "9")),
    Card(Skip(Colour.GREEN), Number(Colour.PURPLE, "4")),
    Card(Skip(Colour.GREEN), Number(Colour.ORANGE, "9")),

    Card(Wild(), Number(Colour.TURQUOISE, "3")),
    Card(Wild(), Number(Colour.PINK, "5")),
    Card(Wild(), Number(Colour.PURPLE, "7")),
    Card(Wild(), Flip(Colour.PINK)),

    Card(WildDrawTwo(), Number(Colour.PINK, "2")),
    Card(WildDrawTwo(), Number(Colour.ORANGE, "4")),
    Card(WildDrawTwo(), Number(Colour.ORANGE, "7")),
    Card(WildDrawTwo(), Number(Colour.PURPLE, "9")),
]
