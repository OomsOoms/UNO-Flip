"""Module representing a deck of cards used in a game.

This module contains the Deck class, representing a deck of cards used in a game.
The Deck class manages the cards, deals hands, and handles discards for the specified game.
"""

from random import choice

from cards import Card, FlipCard

class Deck:
    """Represents a deck of cards used in a game.

    Attributes:
        game (str): The name of the game this deck belongs to.
        flip (int): Indicates the current side of the card: 0 for light side, 1 for dark side. only used in uno flip
        discard (list): A list to store discarded cards.
        cards (list): A list of cards in the deck.

    Methods:
        __init__(game): Initializes the Deck object for the specified game.
        deal_hand(): Deals a hand of 7 cards from the deck.
        place_card(card): Places a card onto the discard pile.
        pick_card(): Picks a card from the deck, reshuffling if necessary.
    """

    def __init__(self, game, card_builder):
        """Initialize the Deck.

        Args:
            game (str): The name of the game.
        """
        self.game = game
        self.flip = 0
        self.discard_pile = []
        self.cards = card_builder(self)

    def deal(self, cards: int = 7) -> list[Card | FlipCard]:
        """Deal a hand of 7 cards from the deck.

        Returns:
            list: A list of cards representing the hand dealt.
        """
        hand = [self.pick_card() for _ in range(cards)]
        return hand

    def pick_card(self) -> Card | FlipCard:
        """Pick a card from the deck, reshuffling if necessary.

        Returns:
            Card | FlipCard: The card picked from the deck as an object.
        """
        # Check if the deck is empty
        if not self.cards:
            # Moves cards from discard pile to the deck, except the last card
            # TODO: reset wild card colours
            self.cards = self.discard_pile[:-1]
            self.discard_pile = [self.discard_pile[-1]]

        # Pick a random card from the deck
        card = choice(self.cards)
        self.cards.remove(card)
        return card
