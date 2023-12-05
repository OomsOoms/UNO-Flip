"""This module defines classes for representing a deck of UNO Flip cards.

Classes:
    Side: Represents a side of a card. It contains the action and colour of the side.
    Card: Represents a card in the game. It contains a light and dark side.
    Number: Represents a number card in the game. It inherits from Side.
    Flip: Represents a flip card in the game. It inherits from Side.
    Skip: Represents a skip card in the game. It inherits from Side.
    SkipEveryone: Represents a skip everyone card in the game. It inherits from Side.
    Reverse: Represents a reverse card in the game. It inherits from Side.
    DrawOne: Represents a draw one card in the game. It inherits from Side.
    DrawFive: Represents a draw five card in the game. It inherits from Side.
    Wild: Represents a wild card in the game. It inherits from Side.
    WildDrawTwo: Represents a wild draw two card in the game. It inherits from Side.
    WildDrawColour: Represents a wild draw colour card in the game. It inherits from Side.

Deck: Represents a deck of UNO Flip cards. It manages the cards in the deck, including shuffling and dealing.
"""

import random

from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)


class Side:
    """A class to represent a side of a card.

    Attributes:
        side (dict): A list containing the action and colour of the side
        type (str): The name of the class
    """

    def __init__(self, side: str, type: dict):
        self.side = side
        self.type = type


class Card:
    """A class to represent a card in the game.

    Attributes:
        light (Side): The light side of the card
        dark (Side): The dark side of the card
    """

    def __init__(self, light_side: Side, dark_side: Side):
        self.light = light_side
        self.dark = dark_side


class Number(Side):
    """A class to represent a number card in the game.
    
    Attributes:
        score (int): The score of the card which is an instance
        attribute as each score is based off the face value of the card

    Args:
        side (dict): A list containing the action and colour of the side
    """
    
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)
        self.score = int(side["action"])

    def behaviour(self, game):
        # Does nothing
        logger.debug(f"Behaviour of {self.side} called")
        pass


class Flip(Side):
    """A class to represent a flip card in the game.
    
    Attributes:
        score (int): The score of the card
    
    Args:
        side (dict): A list containing the action and colour of the side
    """

    score = 20

    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        """Flips the discard pile (list) order and changes the flip value."""
        game.deck.flip = (game.deck.flip + 1) % 2
        game.deck.discard = game.deck.discard[::-1]
        logger.debug(
            f"Behaviour of {self.side} called. Flipped the discard pile, flip value: {game.deck.flip}")


class Skip(Side):

    score = 20

    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        """Skips the next player, increments the current_player_index by 1."""
        game.current_player_index = (game.current_player_index +
                             game.game_direction * -1) % len(game.players)
        logger.debug(
            f"Behaviour of {self.side} called. Skipped the next player, current player index: {game.current_player_index}")


class SkipEveryone(Side):

    score = 30

    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        """Skips everyone, increments the current_player_index by 1."""
        game.current_player_index = (game.current_player_index +
                             game.game_direction) % len(game.players)
        logger.debug(
            f"Behaviour of {self.side} called. Skipped everyone, current player index: {game.current_player_index}")


class Reverse(Side):

    score = 20

    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        """Reverses the game direction."""
        game.game_direction *= -1
        logger.debug(
            f"Behaviour of {self.side} called. Reversed the game direction, game direction: {game.game_direction}")


class DrawOne(Side):

    score = 10

    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        """Draws one card from the deck and adds it to the current player's hand."""
        # Skip the players turn
        game.current_player_index = (game.current_player_index +
                             game.game_direction) % len(game.players)
        # Draw a card and add it to the current player's hand
        current_player_hand = game.players[game.current_player_id].hand
        current_player_hand.append(game.deck.pick_card())
        logger.debug(
            f"Behaviour of {self.side} called. Drew 1 card, current player hand: {current_player_hand}")


class DrawFive(Side):

    score = 20

    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        """Draws five cards from the deck and adds them to the current player's hand.s"""
        # Skip the players turn
        game.current_player_index = (game.current_player_index +
                             game.game_direction) % len(game.players)
        # Draw 5 cards and add them to the current player's hand
        current_player_hand = game.players[game.current_player_id].hand
        for _ in range(5):
            current_player_hand.append(game.deck.pick_card())
        logger.debug(
            f"Behaviour of {self.side} called. Drew 5 cardx, current player hand: {current_player_hand}")


class Wild(Side):

    score = 40

    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        pass  # TODO: Implement this behaviour


class WildDrawTwo(Side):

    score = 50

    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        pass  # TODO: Implement this behaviour


class WildDrawColour(Side):

    score = 60

    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        pass  # TODO: Implement this behaviour


class Deck:
    """A class to represent a deck of cards.
    
    Attributes:
        cards (list): A list of cards
        discard (list): A list of cards that have been discarded
    """

    def deal_hand(self) -> list:
        """Deals a hand of 7 cards to a player.
        
        Returns:
            list: A list of cards
        """
        hand = []
        for x in range(7):
            # pick a random card from the list of cards
            card = random.choice(self.cards)
            self.cards.remove(card) # remove the card from the list of cards
            hand.append(card) # add the card to the player's hand

        return hand

    def place_card(self, card) -> None:
        """Places a card on the discard pile.
        
        Args:
            card (Card): The card to place on the discard pile
        """
        sides = (card.light, card.dark)
        self.discard.append(card)
        side = sides[self.flip]
        side.behaviour(self.game)

    def pick_card(self) -> Card:
        """Picks a card from the deck.

        Returns:
            Card: A card from the deck
        """
        if len(self.cards) == 0:
            # If the deck is empty, swap the discard pile and the deck
            # apart from the last card in the discard pile 
            self.cards, self.discard = self.discard[:-1], self.cards
            self.cards.extend(self.discard)
            self.discard = [self.cards.pop()]

        card = random.choice(self.cards)
        self.cards.remove(card)
        return card

    def __init__(self, game) -> None:
        """Initialises the deck of cards.
        
        Args:
            game (Game): The game object  
        """
        self.game = game
        self.flip = 0 # 0, light side, 1, dark side
        
        # Create a list of cards
        self.discard = []
        self.cards = [
            Card(Number({"action": "1", "colour": "Yellow"}), SkipEveryone({"action": "SkipEveryone", "colour": "Pink"})),
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
