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

    def colours(deck) -> list:
        if deck.flip == 0:
            return [colour for colour in Colour][:4]
        else:
            return [colour for colour in Colour][4:]
    
class Type(Enum):
    NUMBER = "number"
    SKIP = "skip"
    DRAW = "draw"
    WILD = "wild"
    REVERSE = "reverse"

class Card:

    def __init__(self, type: Type, colour: Colour | None, behaviour, action_name: str, score: int):
        self.type = type
        self.colour = colour
        self.behaviour = behaviour
        self.action_name = action_name
        self.score = score

    def is_playable(self, deck):
        discard_pile = deck.discard_pile
        if discard_pile:
            discard = discard_pile[-1]
            # if the discard is a wild card
            if not discard.colour:
                return True
            return (self.colour == discard.colour or self.action_name == discard.action_name) or not self.colour

    def __str__(self):
        return f"{self.colour} {self.action_name}"

    @staticmethod
    def number(colour: Colour, number: int):
        def behaviour(game):
            logger.debug(f"Behaviour of {number} running")
        return Card(Type.NUMBER, colour, behaviour, str(number), score=number)
    
    @staticmethod
    def skip(colour: Colour):
        def behaviour(game):
            logger.debug("Behaviour of skip running")
            game.players.increment_turn()
        return Card(Type.SKIP, colour, behaviour, "skip", score=20)
    
    @staticmethod
    def reverse(colour: Colour):
        def behaviour(game):
            logger.debug("Behaviour of reverse running")
            game.direction *= -1
            game.players.increment_turn()
            game.players.increment_turn()
        return Card(Type.REVERSE, colour, behaviour, "reverse", score=20)
    
    @staticmethod
    def draw(colour: Colour, number: int, *, score: int = 20):
        def behaviour(game):
            logger.debug(f"Behaviour of draw {number} running")
            for _ in range(number):
                player_hand = game.players.current_player.hand
                player_hand.append(game.deck.pick_card())
            game.players.increment_turn()
        return Card(Type.DRAW, colour, behaviour, f"draw{number}", score=score)
    
    @staticmethod
    def wild():
        def behaviour(game):
            logger.debug("Behaviour of wild running")
        return Card(Type.WILD, None, behaviour, "wild", score=40)
    
    @staticmethod
    def wild_draw(number: int):
        def behaviour(game):
            logger.debug("Behaviour of wild draw four running")
            for _ in range(number):
                player_hand = game.players.current_player.hand
                player_hand.append(game.deck.pick_card())
            game.players.increment_turn()
        return Card(Type.WILD, None, behaviour, f"WildDraw{number}", score=50)
    
    # UNO Flip cards

    @staticmethod
    def flip(colour: Colour):
        def behaviour(game):
            logger.debug("Behaviour of flip running")
            game.deck.flip = 1 - game.deck.flip 
            game.deck.discard_pile = game.deck.discard_pile[::-1]
        return Card(Type.WILD, colour, behaviour, "flip", score=20)
    
    @staticmethod
    def skip_everyone(colour: Colour):
        def behaviour(game):
            logger.debug("Behaviour of skip everyone running")
            game.direction *= -1
            game.players.increment_turn()
            game.direction *= -1
        return Card(Type.SKIP, colour, behaviour, "skip everyone", score=20)
    
    @staticmethod
    def wild_draw_colour():
        def behaviour(game):
            logger.debug("Behaviour of wild draw colour running")
            player_hand = game.players.current_player.hand

            while True:
                card = game.deck.pick_card()
                player_hand.append(card)
                if card.colour == game.deck.discard_pile[-1].colour:
                    break

            game.players.increment_turn()
        return Card(Type.WILD, None, behaviour, "wild draw colour", score=60)

class FlipCard:

    def __init__(self, light_card: Card, dark_card: Card):
        
        self.light = light_card
        self.dark = dark_card
        self.deck = None

    def __str__(self):
        return str(self.light) if self.deck.flip == 0 else str(self.dark)

    @property
    def score(self):
        return self.light.score if self.deck.flip == 0 else self.dark.score

    @property
    def action_name(self):
        return self.light.action_name if self.deck.flip == 0 else self.dark.action_name

    @property
    def colour(self):
        return self.light.colour if self.deck.flip == 0 else self.dark.colour
    
    @property
    def behaviour(self):
        return self.light.behaviour if self.deck.flip == 0 else self.dark.behaviour
    
    @property
    def type(self):
        return self.light.type if self.deck.flip == 0 else self.dark.type

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
        
    def is_playable(self, deck):
        discard_pile = deck.discard_pile
        if discard_pile:
            discard = discard_pile[-1]
            # if the discard is a wild card
            if not discard.colour:
                return True
            return (self.colour == discard.colour or self.action_name == discard.action_name) or not self.colour

