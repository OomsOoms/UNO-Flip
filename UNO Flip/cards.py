import random


# Create a Card class
class Card:

    def __init__(self, light_side, dark_side):
        self.light = light_side
        self.dark = dark_side

# Create a Side class


class Side:

    def __init__(self, side, type):
        self.side = side
        self.type = type

# Create different classes for different types of card sides that inherit from the Side class


class Number(Side):

    def __init__(self, side):
        super().__init__(side, "Number")

    def behaviour(self):
        pass


class Flip(Side):
    def __init__(self, side):
        super().__init__(side, "Flip")

    def behaviour(self, game):
        game.deck.flip *= -1


class DrawOne(Side):
    def __init__(self, side):
        super().__init__(side, "DrawOne")

    def behaviour(self, game):
        pass


class Reverse(Side):
    def __init__(self, side):
        super().__init__(side, "Reverse")

    def behaviour(self, game):
        pass


class Wild(Side):
    def __init__(self, side):
        super().__init__(side, "Wild")

    def behaviour(self, game):
        pass


class WildDrawTwo(Side):
    def __init__(self, side):
        super().__init__(side, "WildDrawTwo")

    def behaviour(self, game):
        pass


class DrawFive(Side):
    def __init__(self, side):
        super().__init__(side, "DrawFive")

    def behaviour(self, game):
        pass


class SkipEveryone(Side):
    def __init__(self, side):
        super().__init__(side, "SkipEveryone")

    def behaviour(self, game):
        pass


class WildDrawColour(Side):
    def __init__(self, side):
        super().__init__(side, "WildDrawColour")

    def behaviour(self, game):
        pass


# Create a Deck class
class Deck:

    def __init__(self, game):
        self.game = game

        self.flip = 1

        self.discard = []

        # Create a list of cards
        self.cards = [
            Card(Number(["1", "Yellow"]), Flip(["Red"])),
            Card(Number(["1", "Yellow"]), Flip(["Red"])),
            Card(Number(["2", "Yellow"]), Flip(["Red"])),
            Card(Number(["2", "Yellow"]), Flip(["Red"])),
            Card(Number(["3", "Yellow"]), Flip(["Red"])),
            Card(Number(["3", "Yellow"]), Flip(["Red"])),
            Card(Number(["4", "Yellow"]), Flip(["Red"])),
            Card(Number(["4", "Yellow"]), Flip(["Red"])),
            Card(Number(["5", "Yellow"]), Flip(["Red"])),
            Card(Number(["5", "Yellow"]), Flip(["Red"])),
            Card(Number(["6", "Yellow"]), Flip(["Red"])),
            Card(Number(["6", "Yellow"]), Flip(["Red"])),
            Card(Number(["7", "Yellow"]), Flip(["Red"])),
            Card(Number(["7", "Yellow"]), Flip(["Red"])),
            Card(Number(["8", "Yellow"]), Flip(["Red"])),
            Card(Number(["8", "Yellow"]), Flip(["Red"])),
            Card(Number(["9", "Yellow"]), Flip(["Red"])),
            Card(Number(["9", "Yellow"]), Flip(["Red"])),
            Card(Number(["1", "Red"]), Flip(["Red"])),
            Card(Number(["1", "Red"]), Flip(["Red"])),
            Card(Number(["2", "Red"]), Flip(["Red"])),
            Card(Number(["2", "Red"]), Flip(["Red"])),
            Card(Number(["3", "Red"]), Flip(["Red"])),
            Card(Number(["3", "Red"]), Flip(["Red"])),
            Card(Number(["4", "Red"]), Flip(["Red"])),
            Card(Number(["4", "Red"]), Flip(["Red"])),
            Card(Number(["5", "Red"]), Flip(["Red"])),
            Card(Number(["5", "Red"]), Flip(["Red"])),
            Card(Number(["6", "Red"]), Flip(["Red"])),
            Card(Number(["6", "Red"]), Flip(["Red"])),
            Card(Number(["7", "Red"]), Flip(["Red"])),
            Card(Number(["7", "Red"]), Flip(["Red"])),
            Card(Number(["8", "Red"]), Flip(["Red"])),
            Card(Number(["8", "Red"]), Flip(["Red"])),
            Card(Number(["9", "Red"]), Flip(["Red"])),
            Card(Number(["9", "Red"]), Flip(["Red"])),
            Card(Number(["1", "Blue"]), Flip(["Red"])),
            Card(Number(["1", "Blue"]), Flip(["Red"])),
            Card(Number(["2", "Blue"]), Flip(["Red"])),
            Card(Number(["2", "Blue"]), Flip(["Red"])),
            Card(Number(["3", "Blue"]), Flip(["Red"])),
            Card(Number(["3", "Blue"]), Flip(["Red"])),
            Card(Number(["4", "Blue"]), Flip(["Red"])),
            Card(Number(["4", "Blue"]), Flip(["Red"])),
            Card(Number(["5", "Blue"]), Flip(["Red"])),
            Card(Number(["5", "Blue"]), Flip(["Red"])),
            Card(Number(["6", "Blue"]), Flip(["Red"])),
            Card(Number(["6", "Blue"]), Flip(["Red"])),
            Card(Number(["7", "Blue"]), Flip(["Red"])),
            Card(Number(["7", "Blue"]), Flip(["Red"])),
            Card(Number(["8", "Blue"]), Flip(["Red"])),
            Card(Number(["8", "Blue"]), Flip(["Red"])),
            Card(Number(["9", "Blue"]), Flip(["Red"])),
            Card(Number(["9", "Blue"]), Flip(["Red"])),
            Card(Number(["1", "Green"]), Flip(["Red"])),
            Card(Number(["1", "Green"]), Flip(["Red"])),
            Card(Number(["2", "Green"]), Flip(["Red"])),
            Card(Number(["2", "Green"]), Flip(["Red"])),
            Card(Number(["3", "Green"]), Flip(["Red"])),
            Card(Number(["3", "Green"]), Flip(["Red"])),
            Card(Number(["4", "Green"]), Flip(["Red"])),
            Card(Number(["4", "Green"]), Flip(["Red"])),
            Card(Number(["5", "Green"]), Flip(["Red"])),
            Card(Number(["5", "Green"]), Flip(["Red"])),
            Card(Number(["6", "Green"]), Flip(["Red"])),
            Card(Number(["6", "Green"]), Flip(["Red"])),
            Card(Number(["7", "Green"]), Flip(["Red"])),
            Card(Number(["7", "Green"]), Flip(["Red"])),
            Card(Number(["8", "Green"]), Flip(["Red"])),
            Card(Number(["8", "Green"]), Flip(["Red"])),
            Card(Number(["9", "Green"]), Flip(["Red"])),
            Card(Number(["9", "Green"]), Flip(["Red"])),

            Card(DrawOne(["Yellow"]), Flip(["Red"])),
            Card(DrawOne(["Yellow"]), Flip(["Red"])),
            Card(DrawOne(["Red"]), Flip(["Red"])),
            Card(DrawOne(["Red"]), Flip(["Red"])),
            Card(DrawOne(["Blue"]), Flip(["Red"])),
            Card(DrawOne(["Blue"]), Flip(["Red"])),
            Card(DrawOne(["Green"]), Flip(["Red"])),
            Card(DrawOne(["Green"]), Flip(["Red"])),

            Card(Reverse(["Yellow"]), Flip(["Red"])),
            Card(Reverse(["Yellow"]), Flip(["Red"])),
            Card(Reverse(["Red"]), Flip(["Red"])),
            Card(Reverse(["Red"]), Flip(["Red"])),
            Card(Reverse(["Blue"]), Flip(["Red"])),
            Card(Reverse(["Blue"]), Flip(["Red"])),
            Card(Reverse(["Green"]), Flip(["Red"])),
            Card(Reverse(["Green"]), Flip(["Red"])),

            Card(Flip(["Yellow"]), Flip(["Red"])),
            Card(Flip(["Yellow"]), Flip(["Red"])),
            Card(Flip(["Red"]), Flip(["Red"])),
            Card(Flip(["Red"]), Flip(["Red"])),
            Card(Flip(["Blue"]), Flip(["Red"])),
            Card(Flip(["Blue"]), Flip(["Red"])),
            Card(Flip(["Green"]), Flip(["Red"])),
            Card(Flip(["Green"]), Flip(["Red"])),

            Card(DrawFive(["Yellow"]), Flip(["Red"])),
            Card(DrawFive(["Yellow"]), Flip(["Red"])),
            Card(DrawFive(["Red"]), Flip(["Red"])),
            Card(DrawFive(["Red"]), Flip(["Red"])),
            Card(DrawFive(["Blue"]), Flip(["Red"])),
            Card(DrawFive(["Blue"]), Flip(["Red"])),
            Card(DrawFive(["Green"]), Flip(["Red"])),
            Card(DrawFive(["Green"]), Flip(["Red"])),

            Card(Wild(["Yellow"]), Flip(["Red"])),
            Card(Wild(["Red"]), Flip(["Red"])),
            Card(Wild(["Blue"]), Flip(["Red"])),
            Card(Wild(["Green"]), Flip(["Red"])),

            Card(WildDrawTwo(["Yellow"]), Flip(["Red"])),
            Card(WildDrawTwo(["Red"]), Flip(["Red"])),
            Card(WildDrawTwo(["Blue"]), Flip(["Red"])),
            Card(WildDrawTwo(["Green"]), Flip(["Red"]))
        ]

    # Create a method to deal a hand of cards to a player
    def deal_hand(self):
        hand = []
        for x in range(7):
            # pick a random card from the list of cards
            card = random.choice(self.cards)
            self.cards.remove(card)  # remove the card from the list of cards
            hand.append(card)  # add the card to the player's hand

        return hand

    # Create a method to pick a card from the deck
    def pick_card(self):
        # pick a random card from the list of cards
        card = random.choice(self.cards)
        self.cards.remove(card)  # remove the card from the list of cards

        return card

    def check_discard(self):
        return self.discard[self.flip]

    def place(self, card):
        card.behaviour(self.game)
        self.discard.append(card)
