import random

from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)

# Create a Card class
class Card:

    def __init__(self, light_side, dark_side):
        self.light = light_side
        self.dark = dark_side

# Create a Side class
class Side:

    def __init__(self, side, type):
        # eg. ["1", "Yellow"]
        self.side = side
        # Name of the class
        self.type = type

# Create different classes for different types of card sides that inherit from the Side class
class Number(Side):

    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        # Does nothing
        logger.debug(f"Played a number card, side: {self.side}")
        pass

class Flip(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        # Reverse the order of the discard pile and change the flip value
        game.flip = (game.flip + 1) % 2
        game.deck.discard = game.deck.discard[::-1]
        logger.debug(f"Flipped the discard pile, flip value: {game.flip}")

class Reverse(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        # Reverse the order the current_player_index will increment
        game.game_direction *= -1
        logger.debug(f"Reversed the game direction, game direction: {game.game_direction}")

class Wild(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        colour = input("Pick a colour ")
        self.side = [colour]
        logger.debug(f"Changed the colour to {colour}")

class Skip(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        # Skips the next player by incrementing or decrementing the current_player_index by 2 depending on the direction
        game.current_player_index = (game.current_player_index + game.game_direction*2) % len(game.players_list)
        logger.debug(f"Skipped the next player, current player index: {game.current_player_index}")

class SkipEveryone(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        # Player index will stay the same when incremented in the end_turn function
        game.current_player_index = (game.current_player_index + (2 * game.game_direction)) % len(game.players_list)
        logger.debug(f"Skipped everyone, current player index: {game.current_player_index}")

# TODO: Implement this behaviour
class DrawOne(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        current_player_hand = game.players[game.current_player_id].hand
        current_player_hand.append(game.deck.pick_card(game))
        game.end_turn()
        logger.debug(f"Drew 1 card, current player hand: {current_player_hand}")
        
class WildDrawTwo(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        colour = input("Pick a colour ")
        self.side = [colour]

        pass # TODO: Implement this behaviour

class DrawFive(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        current_player_hand = game.players[game.current_player_id].hand
        current_player_hand.extend(game.deck.pick_card(game) for _ in range(5))
        game.end_turn()
        logger.debug(f"Drew 5 cards, current player hand: {current_player_hand}")
        
class WildDrawColour(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        colour = input("Pick a colour ")
        self.side = [colour]

        pass # TODO: Implement this behaviour

# Create a Deck class
class Deck:
    # 0, light side, 1, dark side
    flip = 0
    # discarded careds are added to the discard pile
    discard = []

    def __init__(self, game):
        self.game = game

    # Create a method to deal a hand of cards to a player
    def deal_hand(self):
        hand = []
        for x in range(7):
            # pick a random card from the list of cards
            card = random.choice(self.cards)
            self.cards.remove(card)  # remove the card from the list of cards
            hand.append(card)  # add the card to the player's hand

        return hand
    
    def place_card(self, card):
        sides = (card.light, card.dark)
        self.discard.append(card)
        side = sides[self.flip]
        side.behaviour(self.game)

    # Create a method to pick a random card from the deck
    def pick_card(self, game):
        if len(self.cards) == 0:
            self.cards, self.discard = self.discard[1:], self.cards
            self.cards.extend(self.discard)
            self.discard = [self.cards.pop()]

        card = random.choice(self.cards)
        self.cards.remove(card)  # Remove the card from the list of cards
        return card

    # Create a list of cards
    cards = [
        Card(Number({"colour": "1", "colour": "Yellow"}), SkipEveryone({"action": "SkipEveryone", "colour": "Pink"})),
        Card(Number({"action": "1", "colour": "Yellow"}), Wild({"action": "Wild", "colour": None})),
        Card(Number({"action": "2", "colour": "Yellow"}), Number({"action": "1", "colour": "Turquoise"})),
        Card(Number({"action": "2", "colour": "Yellow"}), Number({"action": "8", "colour": "Turquoise"})),
        Card(Number({"action": "3", "colour": "Yellow"}), Number({"action": "1", "colour": "Purple"})),
        Card(Number({"action": "3", "colour": "Yellow"}), DrawFive({"action": "DrawFive", "colour": "Pink"})),
        Card(Number({"action": "4", "colour": "Yellow"}), DrawFive({"action": "DrawFive", "colour": "Pink"})),
        Card(Number({"action": "4", "colour": "Yellow"}), Flip({"action": "Flip", "colour": "Purple"})),
        Card(Number({"action": "5", "colour": "Yellow"}), Number({"action": "8", "colour": "Turquoise"})),
        Card(Number({"action": "5", "colour": "Yellow"}), Number({"action": "9", "colour": "Purple"})),
        Card(Number({"action": "6", "colour": "Yellow"}), SkipEveryone({"action": "SkipEveryone", "colour": "Orange"})),
        Card(Number({"action": "6", "colour": "Yellow"}), WildDrawColour({"action": "WildDrawColour", "colour": None})),
        Card(Number({"action": "7", "colour": "Yellow"}), Number({"action": "2", "colour": "Orange"})),
        Card(Number({"action": "7", "colour": "Yellow"}), Number({"action": "6", "colour": "Purple"})),
        Card(Number({"action": "8", "colour": "Yellow"}), Number({"action": "1", "colour": "Pink"})),
        Card(Number({"action": "8", "colour": "Yellow"}), Number({"action": "2", "colour": "Orange"})),
        Card(Number({"action": "9", "colour": "Yellow"}), Number({"action": "4", "colour": "Purple"})),
        Card(Number({"action": "9", "colour": "Yellow"}), Number({"action": "5", "colour": "Turquoise"})),

        Card(Number({"action": "1", "colour": "Red"}), Number({"action": "2", "colour": "Purple"})),
        Card(Number({"action": "1", "colour": "Red"}), Number({"action": "3", "colour": "Pink"})),
        Card(Number({"action": "2", "colour": "Red"}), DrawFive({"action": "DrawFive", "colour": "Purple"})),
        Card(Number({"action": "2", "colour": "Red"}), Reverse({"action": "Reverse", "colour": "Orange"})),
        Card(Number({"action": "3", "colour": "Red"}), Number({"action": "7", "colour": "Pink"})),
        Card(Number({"action": "3", "colour": "Red"}), WildDrawColour({"action": "WildDrawColour", "colour": None})),
        Card(Number({"action": "4", "colour": "Red"}), DrawFive({"action": "DrawFive", "colour": "Purple"})),
        Card(Number({"action": "4", "colour": "Red"}), Flip({"action": "Flip", "colour": "Orange"})),
        Card(Number({"action": "5", "colour": "Red"}), Number({"action": "2", "colour": "Pink"})),
        Card(Number({"action": "5", "colour": "Red"}), Number({"action": "5", "colour": "Turquoise"})),
        Card(Number({"action": "6", "colour": "Red"}), Number({"action": "9", "colour": "Orange"})),
        Card(Number({"action": "6", "colour": "Red"}), SkipEveryone({"action": "SkipEveryone", "colour": "Pink"})),
        Card(Number({"action": "7", "colour": "Red"}), Number({"action": "1", "colour": "Orange"})),
        Card(Number({"action": "7", "colour": "Red"}), Number({"action": "5", "colour": "Purple"})),
        Card(Number({"action": "8", "colour": "Red"}), Number({"action": "7", "colour": "Turquoise"})),
        Card(Number({"action": "8", "colour": "Red"}), Reverse({"action": "Reverse", "colour": "Purple"})),
        Card(Number({"action": "9", "colour": "Red"}), Number({"action": "5", "colour": "Purple"})),
        Card(Number({"action": "9", "colour": "Red"}), Reverse({"action": "Reverse", "colour": "Turquoise"})),
    
        Card(Number({"action": "1", "colour": "Blue"}), SkipEveryone({"action": "SkipEveryone", "colour": "Purple"})),
        Card(Number({"action": "1", "colour": "Blue"}), SkipEveryone({"action": "SkipEveryone", "colour": "Purple"})),
        Card(Number({"action": "2", "colour": "Blue"}), Number({"action": "8", "colour": "Orange"})),
        Card(Number({"action": "2", "colour": "Blue"}), Number({"action": "6", "colour": "Pink"})),
        Card(Number({"action": "3", "colour": "Blue"}), Number({"action": "2", "colour": "Turquoise"})),
        Card(Number({"action": "3", "colour": "Blue"}), Number({"action": "8", "colour": "Purple"})),
        Card(Number({"action": "4", "colour": "Blue"}), DrawFive({"action": "DrawFive", "colour": "Turquoise"})),
        Card(Number({"action": "4", "colour": "Blue"}), Number({"action": "1", "colour": "Purple"})),
        Card(Number({"action": "5", "colour": "Blue"}), Number({"action": "9", "colour": "Pink"})),
        Card(Number({"action": "5", "colour": "Blue"}), Reverse({"action": "Reverse", "colour": "Orange"})),
        Card(Number({"action": "6", "colour": "Blue"}), Reverse({"action": "Reverse", "colour": "Purple"})),
        Card(Number({"action": "6", "colour": "Blue"}), SkipEveryone({"action": "SkipEveryone", "colour": "Turquoise"})),
        Card(Number({"action": "7", "colour": "Blue"}), Number({"action": "3", "colour": "Orange"})),
        Card(Number({"action": "7", "colour": "Blue"}), SkipEveryone({"action": "SkipEveryone", "colour": "Orange"})),
        Card(Number({"action": "8", "colour": "Blue"}), Number({"action": "4", "colour": "Turquoise"})),
        Card(Number({"action": "8", "colour": "Blue"}), Reverse({"action": "Reverse", "colour": "Turquoise"})),
        Card(Number({"action": "9", "colour": "Blue"}), Number({"action": "5", "colour": "Orange"})),
        Card(Number({"action": "9", "colour": "Blue"}), Flip({"action": "Flip", "colour": "Purple"})),

        Card(Number({"action": "1", "colour": "Green"}), Number({"action": "5", "colour": "Orange"})),
        Card(Number({"action": "1", "colour": "Green"}), Flip({"action": "Flip", "colour": "Orange"})),
        Card(Number({"action": "2", "colour": "Green"}), SkipEveryone({"action": "SkipEveryone", "colour": "Turquoise"})),
        Card(Number({"action": "2", "colour": "Green"}), DrawFive({"action": "DrawFive", "colour": "Turquoise"})),
        Card(Number({"action": "3", "colour": "Green"}), Number({"action": "2", "colour": "Purple"})),
        Card(Number({"action": "3", "colour": "Green"}), Flip({"action": "Flip", "colour": "Pink"})),
        Card(Number({"action": "4", "colour": "Green"}), Number({"action": "9", "colour": "Turquoise"})),
        Card(Number({"action": "4", "colour": "Green"}), Number({"action": "8", "colour": "Pink"})),
        Card(Number({"action": "5", "colour": "Green"}), Number({"action": "4", "colour": "Turquoise"})),
        Card(Number({"action": "5", "colour": "Green"}), Number({"action": "7", "colour": "Orange"})),
        Card(Number({"action": "6", "colour": "Green"}), Number({"action": "5", "colour": "Pink"})),
        Card(Number({"action": "6", "colour": "Green"}), WildDrawColour({"action": "WildDrawColour", "colour": None})),
        Card(Number({"action": "7", "colour": "Green"}), Number({"action": "2", "colour": "Turquoise"})),
        Card(Number({"action": "7", "colour": "Green"}), Number({"action": "6", "colour": "Orange"})),
        Card(Number({"action": "8", "colour": "Green"}), Number({"action": "9", "colour": "Turquoise"})),
        Card(Number({"action": "8", "colour": "Green"}), Reverse({"action": "Reverse", "colour": "Pink"})),
        Card(Number({"action": "9", "colour": "Green"}), DrawFive({"action": "DrawFive", "colour": "Pink"})),
        Card(Number({"action": "9", "colour": "Green"}), Reverse({"action": "Reverse", "colour": "Orange"})),

        Card(DrawOne({"action": "DrawOne", "colour": "Yellow"}), Number({"action": "1", "colour": "Pink"})),
        Card(DrawOne({"action": "DrawOne", "colour": "Yellow"}), Number({"action": "8", "colour": "Purple"})),
        Card(DrawOne({"action": "DrawOne", "colour": "Red"}), Number({"action": "3", "colour": "Pink"})),
        Card(DrawOne({"action": "DrawOne", "colour": "Red"}), Number({"action": "4", "colour": "Pink"})),
        Card(DrawOne({"action": "DrawOne", "colour": "Blue"}), Number({"action": "6", "colour": "Pink"})),
        Card(DrawOne({"action": "DrawOne", "colour": "Blue"}), Number({"action": "6", "colour": "Turquoise"})),
        Card(DrawOne({"action": "DrawOne", "colour": "Green"}), Number({"action": "6", "colour": "Orange"})),
        Card(DrawOne({"action": "DrawOne", "colour": "Green"}), Number({"action": "6", "colour": "Turquoise"})),

        Card(Reverse({"action": "Reverse", "colour": "Yellow"}), Flip({"action": "Flip", "colour": "Turquoise"})),
        Card(Reverse({"action": "Reverse", "colour": "Yellow"}), Wild({"action": "Wild", "colour": None})),
        Card(Reverse({"action": "Reverse", "colour": "Red"}), Number({"action": "3", "colour": "Purple"})),
        Card(Reverse({"action": "Reverse", "colour": "Red"}), Number({"action": "7", "colour": "Turquoise"})),
        Card(Reverse({"action": "Reverse", "colour": "Blue"}), Number({"action": "4", "colour": "Orange"})),
        Card(Reverse({"action": "Reverse", "colour": "Blue"}), Wild({"action": "Wild", "colour": None})),
        Card(Reverse({"action": "Reverse", "colour": "Green"}), Number({"action": "1", "colour": "Orange"})),
        Card(Reverse({"action": "Reverse", "colour": "Green"}), Number({"action": "7", "colour": "Pink"})),

        Card(Flip({"action": "Flip", "colour": "Yellow"}), Number({"action": "4", "colour": "Pink"})),
        Card(Flip({"action": "Flip", "colour": "Yellow"}), Number({"action": "8", "colour": "Orange"})),
        Card(Flip({"action": "Flip", "colour": "Red"}), Number({"action": "3", "colour": "Purple"})),
        Card(Flip({"action": "Flip", "colour": "Red"}), Number({"action": "8", "colour": "Pink"})),
        Card(Flip({"action": "Flip", "colour": "Blue"}), Number({"action": "6", "colour": "Purple"})),
        Card(Flip({"action": "Flip", "colour": "Blue"}), Number({"action": "7", "colour": "Purple"})),
        Card(Flip({"action": "Flip", "colour": "Green"}), Number({"action": "3", "colour": "Turquoise"})),
        Card(Flip({"action": "Flip", "colour": "Green"}), WildDrawColour({"action": "WildDrawColour", "colour": None})),

        Card(Skip({"action": "Skip", "colour": "Yellow"}), Number({"action": "3", "colour": "Orange"})),
        Card(Skip({"action": "Skip", "colour": "Yellow"}), Flip({"action": "Flip", "colour": "Turquoise"})),
        Card(Skip({"action": "Skip", "colour": "Red"}), DrawFive({"action": "DrawFive", "colour": "Orange"})),
        Card(Skip({"action": "Skip", "colour": "Red"}), Wild({"action": "Wild", "colour": None})),
        Card(Skip({"action": "Skip", "colour": "Blue"}), Number({"action": "1", "colour": "Turquoise"})),
        Card(Skip({"action": "Skip", "colour": "Blue"}), Number({"action": "9", "colour": "Pink"})),
        Card(Skip({"action": "Skip", "colour": "Green"}), Number({"action": "4", "colour": "Purple"})),
        Card(Skip({"action": "Skip", "colour": "Green"}), Number({"action": "9", "colour": "Orange"})),

        Card(Wild({"action": "Wild", "colour": None}), Number({"action": "3", "colour": "Turquoise"})),
        Card(Wild({"action": "Wild", "colour": None}), Number({"action": "5", "colour": "Pink"})),
        Card(Wild({"action": "Wild", "colour": None}), Number({"action": "7", "colour": "Purple"})),
        Card(Wild({"action": "Wild", "colour": None}), Flip({"action": "Flip", "colour": "Pink"})),

        Card(WildDrawTwo({"action": "WildDrawTwo", "colour": None}), Number({"action": "2", "colour": "Pink"})),
        Card(WildDrawTwo({"action": "WildDrawTwo", "colour": None}), Number({"action": "4", "colour": "Orange"})),
        Card(WildDrawTwo({"action": "WildDrawTwo", "colour": None}), Number({"action": "7", "colour": "Orange"})),
        Card(WildDrawTwo({"action": "WildDrawTwo", "colour": None}), Number({"action": "9", "colour": "Purple"}))
    ]
