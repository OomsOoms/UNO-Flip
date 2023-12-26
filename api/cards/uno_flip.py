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

    def colours(game) -> list:
        # Game object is only used in the flip version of the game
        if game.deck.flip == 0:
            return [colour.value for colour in Colours][:4]
        else:
            return [colour.value for colour in Colours][4:]


class Side:
    """A side of a card. A card has two sides, a light side and a dark side.

    Attributes:
        colour (Colour): The colour of the card.
        action (str): The action text of the card.
    """

    def __init__(self, colour: Colours, action: str):
        self.colour = colour.value if colour else None
        self.action = action


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


class Number(Side):
    """A number side of a card.

    Attributes:
        colour (Colour): The colour of the card.
        action (str): The action text of the card.
        score (int): The score of the card.
    """

    def __init__(self, colour: Colours, action: str):
        super().__init__(colour, action)
        self.score = int(action)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")


class Flip(Side):

    score = 20

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        # flip the deck attribute
        game.deck.flip = (game.deck.flip + 1) % 2
        # Reverse the discard pile
        game.deck.discard_pile = game.deck.discard_pile[::-1]


class Skip(Side):

    score = 20

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        game.players.increment_turn()


class SkipEveryone(Side):

    score = 30

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        # This cancels out the increment_turn() in the end_turn() method
        game.direction *= -1
        game.players.increment_turn()
        game.direction *= -1


class Reverse(Side):

    score = 20

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        game.direction *= -1
        game.players.increment_turn()
        game.players.increment_turn()


class DrawOne(Side):

    score = 10

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        player_hand = game.players.current_player.hand
        player_hand.append(game.deck.pick_card())
        game.players.increment_turn()


class DrawFive(Side):

    score = 20

    def __init__(self, colour: Colours):
        super().__init__(colour, self.__class__.__name__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")
        for _ in range(5):
            player_hand = game.players.current_player.hand
            player_hand.append(game.deck.pick_card())
        game.players.increment_turn()


class Wild(Side):

    score = 40

    def __init__(self):
        super().__init__(None, self.__class__.__name__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")


class WildDrawTwo(Side):

    score = 50

    def __init__(self):
        super().__init__(None, self.__class__.__name__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")

        for _ in range(2):
            player_hand = game.players.current_player.hand
            player_hand.append(game.deck.pick_card())
        game.players.increment_turn()


class WildDrawColour(Side):

    score = 60

    def __init__(self):
        super().__init__(None, self.__class__.__name__)

    def behaviour(self, game):
        logger.debug(f"Behaviour of {self.action} running")

        player_hand = game.players.current_player.hand

        while True:
            card = game.deck.pick_card()
            player_hand.append(card)
            if card.colour == game.deck.discard_pile[-1].colour:
                break

        game.players.increment_turn()


