from enum import Enum

from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)


class Colours(Enum):
    YELLOW = "yellow"
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    ORANGE = "orange"
    PINK = "pink"
    PURPLE = "purple"
    TURQUOISE = "turquoise"

    def colours(game_object) -> list:
        # Game object is only used in the flip version of the game
        if game_object.deck.flip == 0:
            return [colour.value for colour in Colours][:4]
        else:
            return [colour.value for colour in Colours][4:]


class Side:
    """A side of a card. A card has two sides, a light side and a dark side.

    Attributes:
        colour (Colour): The colour of the card.
        action (str): The action text of the card.
        card_type (type): The type of the card. This is the class of the card.
    """

    def __init__(self, colour: Colours, action: str, card_type):
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
    
    @property
    def __class__(self):
        if self.deck.flip == 0:
            return self.light.__class__
        else:
            return self.dark.__class__

    def is_playable(self):
        discard_pile = self.deck.discard_pile
        if discard_pile:
            discard = discard_pile[-1]
            # if the discard is a wild card
            if not discard.colour:
                return True
            return (self.colour == discard.colour or self.action == discard.action) or not self.colour

    def behaviour(self, game):
        self.light.behaviour(
            game) if self.deck.flip == 0 else self.dark.behaviour(game)

    def __str__(self):
        return f"{self.colour.name} {self.action} {self.card_type.__name__}"


class Number(Side):
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


class Flip(Side):

    score = 20

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        # flip the deck attribute
        game.deck.flip = (game.deck.flip + 1) % 2
        # Reverse the discard pile
        game.deck.discard_pile = game.deck.discard_pile[::-1]


class Skip(Side):

    score = 20

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        game.players.increment_turn()


class SkipEveryone(Side):

    score = 30

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        # This cancels out the increment_turn() in the end_turn() method
        game.direction *= -1
        game.players.increment_turn()
        game.direction *= -1


class Reverse(Side):

    score = 20

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        game.direction *= -1
        game.players.increment_turn()
        game.players.increment_turn()


class DrawOne(Side):

    score = 10

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        player_hand = game.players.current_player.hand
        player_hand.append(game.deck.pick_card())
        game.players.increment_turn()


class DrawFive(Side):

    score = 20

    def __init__(self, colour: Colours):
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


class WildDrawTwo(Side):

    score = 50

    def __init__(self):
        super().__init__(None, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")

        for _ in range(2):
            player_hand = game.players.current_player.hand
            player_hand.append(game.deck.pick_card())
        game.players.increment_turn()


class WildDrawColour(Side):

    score = 60

    def __init__(self):
        super().__init__(None, self.__class__.__name__, self.__class__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")

        player_hand = game.players.current_player.hand

        while True:
            card = game.deck.pick_card()
            player_hand.append(card)
            if card.colour == game.deck.discard_pile[-1].colour:
                break

        game.players.increment_turn()


cards = [
    Card(Number(Colours.YELLOW, "1"), SkipEveryone(Colours.PINK)),
    Card(Number(Colours.YELLOW, "1"), Wild()),
    Card(Number(Colours.YELLOW, "2"), Number(Colours.TURQUOISE, "1")),
    Card(Number(Colours.YELLOW, "2"), Number(Colours.TURQUOISE, "8")),
    Card(Number(Colours.YELLOW, "3"), Number(Colours.PURPLE, "1")),
    Card(Number(Colours.YELLOW, "3"), DrawFive(Colours.PINK)),
    Card(Number(Colours.YELLOW, "4"), DrawFive(Colours.PINK)),
    Card(Number(Colours.YELLOW, "4"), Flip(Colours.PURPLE)),
    Card(Number(Colours.YELLOW, "5"), Number(Colours.TURQUOISE, "8")),
    Card(Number(Colours.YELLOW, "5"), Number(Colours.PURPLE, "9")),
    Card(Number(Colours.YELLOW, "6"), SkipEveryone(Colours.ORANGE)),
    Card(Number(Colours.YELLOW, "6"), WildDrawColour()),
    Card(Number(Colours.YELLOW, "7"), Number(Colours.ORANGE, "2")),
    Card(Number(Colours.YELLOW, "7"), Number(Colours.PURPLE, "6")),
    Card(Number(Colours.YELLOW, "8"), Number(Colours.PINK, "1")),
    Card(Number(Colours.YELLOW, "8"), Number(Colours.ORANGE, "2")),
    Card(Number(Colours.YELLOW, "9"), Number(Colours.PURPLE, "4")),
    Card(Number(Colours.YELLOW, "9"), Number(Colours.TURQUOISE, "5")),

    Card(Number(Colours.RED, "1"), Number(Colours.PURPLE, "2")),
    Card(Number(Colours.RED, "1"), Number(Colours.PINK, "3")),
    Card(Number(Colours.RED, "2"), DrawFive(Colours.PURPLE)),
    Card(Number(Colours.RED, "2"), Reverse(Colours.ORANGE)),
    Card(Number(Colours.RED, "3"), Number(Colours.PINK, "7")),
    Card(Number(Colours.RED, "3"), WildDrawColour()),
    Card(Number(Colours.RED, "4"), DrawFive(Colours.PURPLE)),
    Card(Number(Colours.RED, "4"), Flip(Colours.ORANGE)),
    Card(Number(Colours.RED, "5"), Number(Colours.PINK, "2")),
    Card(Number(Colours.RED, "5"), Number(Colours.TURQUOISE, "5")),
    Card(Number(Colours.RED, "6"), Number(Colours.ORANGE, "9")),
    Card(Number(Colours.RED, "6"), SkipEveryone(Colours.PINK)),
    Card(Number(Colours.RED, "7"), Number(Colours.ORANGE, "1")),
    Card(Number(Colours.RED, "7"), Number(Colours.PURPLE, "5")),
    Card(Number(Colours.RED, "8"), Number(Colours.TURQUOISE, "7")),
    Card(Number(Colours.RED, "8"), Reverse(Colours.PURPLE)),
    Card(Number(Colours.RED, "9"), Number(Colours.PURPLE, "5")),
    Card(Number(Colours.RED, "9"), Reverse(Colours.TURQUOISE)),

    Card(Number(Colours.BLUE, "1"), SkipEveryone(Colours.PURPLE)),
    Card(Number(Colours.BLUE, "1"), SkipEveryone(Colours.PURPLE)),
    Card(Number(Colours.BLUE, "2"), Number(Colours.ORANGE, "8")),
    Card(Number(Colours.BLUE, "2"), Number(Colours.PINK, "6")),
    Card(Number(Colours.BLUE, "3"), Number(Colours.TURQUOISE, "2")),
    Card(Number(Colours.BLUE, "3"), Number(Colours.PURPLE, "8")),
    Card(Number(Colours.BLUE, "4"), DrawFive(Colours.TURQUOISE)),
    Card(Number(Colours.BLUE, "4"), Number(Colours.PURPLE, "1")),
    Card(Number(Colours.BLUE, "5"), Number(Colours.PINK, "9")),
    Card(Number(Colours.BLUE, "5"), Reverse(Colours.ORANGE)),
    Card(Number(Colours.BLUE, "6"), Reverse(Colours.PURPLE)),
    Card(Number(Colours.BLUE, "6"), SkipEveryone(Colours.TURQUOISE)),
    Card(Number(Colours.BLUE, "7"), Number(Colours.ORANGE, "3")),
    Card(Number(Colours.BLUE, "7"), SkipEveryone(Colours.ORANGE)),
    Card(Number(Colours.BLUE, "8"), Number(Colours.TURQUOISE, "4")),
    Card(Number(Colours.BLUE, "8"), Reverse(Colours.TURQUOISE)),
    Card(Number(Colours.BLUE, "9"), Number(Colours.ORANGE, "5")),
    Card(Number(Colours.BLUE, "9"), Flip(Colours.PURPLE)),

    Card(Number(Colours.GREEN, "1"), Number(Colours.ORANGE, "5")),
    Card(Number(Colours.GREEN, "1"), Flip(Colours.ORANGE)),
    Card(Number(Colours.GREEN, "2"), SkipEveryone(Colours.TURQUOISE)),
    Card(Number(Colours.GREEN, "2"), DrawFive(Colours.TURQUOISE)),
    Card(Number(Colours.GREEN, "3"), Number(Colours.PURPLE, "2")),
    Card(Number(Colours.GREEN, "3"), Flip(Colours.PINK)),
    Card(Number(Colours.GREEN, "4"), Number(Colours.TURQUOISE, "9")),
    Card(Number(Colours.GREEN, "4"), Number(Colours.PINK, "8")),
    Card(Number(Colours.GREEN, "5"), Number(Colours.TURQUOISE, "4")),
    Card(Number(Colours.GREEN, "5"), Number(Colours.ORANGE, "7")),
    Card(Number(Colours.GREEN, "6"), Number(Colours.PINK, "5")),
    Card(Number(Colours.GREEN, "6"), WildDrawColour()),
    Card(Number(Colours.GREEN, "7"), Number(Colours.TURQUOISE, "2")),
    Card(Number(Colours.GREEN, "7"), Number(Colours.ORANGE, "6")),
    Card(Number(Colours.GREEN, "8"), Number(Colours.TURQUOISE, "9")),
    Card(Number(Colours.GREEN, "8"), Reverse(Colours.PINK)),
    Card(Number(Colours.GREEN, "9"), DrawFive(Colours.PINK)),
    Card(Number(Colours.GREEN, "9"), Reverse(Colours.ORANGE)),

    Card(DrawOne(Colours.YELLOW), Number(Colours.PINK, "1")),
    Card(DrawOne(Colours.YELLOW), Number(Colours.PURPLE, "8")),
    Card(DrawOne(Colours.RED), Number(Colours.PINK, "3")),
    Card(DrawOne(Colours.RED), Number(Colours.PINK, "4")),
    Card(DrawOne(Colours.BLUE), Number(Colours.PINK, "6")),
    Card(DrawOne(Colours.BLUE), Number(Colours.TURQUOISE, "6")),
    Card(DrawOne(Colours.GREEN), Number(Colours.ORANGE, "6")),
    Card(DrawOne(Colours.GREEN), Number(Colours.TURQUOISE, "6")),

    Card(Reverse(Colours.YELLOW), Flip(Colours.TURQUOISE)),
    Card(Reverse(Colours.YELLOW), Wild()),
    Card(Reverse(Colours.RED), Number(Colours.PURPLE, "3")),
    Card(Reverse(Colours.RED), Number(Colours.TURQUOISE, "7")),
    Card(Reverse(Colours.BLUE), Number(Colours.ORANGE, "4")),
    Card(Reverse(Colours.BLUE), Wild()),
    Card(Reverse(Colours.GREEN), Number(Colours.ORANGE, "1")),
    Card(Reverse(Colours.GREEN), Number(Colours.PINK, "7")),

    Card(Flip(Colours.YELLOW), Number(Colours.PINK, "4")),
    Card(Flip(Colours.YELLOW), Number(Colours.ORANGE, "8")),
    Card(Flip(Colours.RED), Number(Colours.PURPLE, "3")),
    Card(Flip(Colours.RED), Number(Colours.PINK, "8")),
    Card(Flip(Colours.BLUE), Number(Colours.PURPLE, "6")),
    Card(Flip(Colours.BLUE), Number(Colours.PURPLE, "7")),
    Card(Flip(Colours.GREEN), Number(Colours.TURQUOISE, "3")),
    Card(Flip(Colours.GREEN), WildDrawColour()),

    Card(Skip(Colours.YELLOW), Number(Colours.ORANGE, "3")),
    Card(Skip(Colours.YELLOW), Flip(Colours.TURQUOISE)),
    Card(Skip(Colours.RED), DrawFive(Colours.ORANGE)),
    Card(Skip(Colours.RED), Wild()),
    Card(Skip(Colours.BLUE), Number(Colours.TURQUOISE, "1")),
    Card(Skip(Colours.BLUE), Number(Colours.PINK, "9")),
    Card(Skip(Colours.GREEN), Number(Colours.PURPLE, "4")),
    Card(Skip(Colours.GREEN), Number(Colours.ORANGE, "9")),

    Card(Wild(), Number(Colours.TURQUOISE, "3")),
    Card(Wild(), Number(Colours.PINK, "5")),
    Card(Wild(), Number(Colours.PURPLE, "7")),
    Card(Wild(), Flip(Colours.PINK)),

    Card(WildDrawTwo(), Number(Colours.PINK, "2")),
    Card(WildDrawTwo(), Number(Colours.ORANGE, "4")),
    Card(WildDrawTwo(), Number(Colours.ORANGE, "7")),
    Card(WildDrawTwo(), Number(Colours.PURPLE, "9")),
]
