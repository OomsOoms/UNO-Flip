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

    def behaviour(self, game):
        pass


class Flip(Side):
    def __init__(self, side):
        super().__init__(side, "Flip")

    def behaviour(self, game):
        game.flip *= -1
        game.deck.discard = game.deck.discard[::-1]


class DrawOne(Side):
    def __init__(self, side):
        super().__init__(side, "DrawOne")

    def behaviour(self, game):
        pass


class Reverse(Side):
    def __init__(self, side):
        super().__init__(side, "Reverse")

    def behaviour(self, game):
        game.direction *= -1


class Wild(Side):
    def __init__(self, side):
        super().__init__(side, "Wild")

    def behaviour(self, game):
        colour = input("Pick a colour")
        self.side = [colour]


class WildDrawTwo(Side):
    def __init__(self, side):
        super().__init__(side, "WildDrawTwo")

    def behaviour(self, game):
        colour = input("Pick a colour ")
        self.side = [colour]


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


class Skip(Side):
    def __init__(self, side):
        super().__init__(side, "Skip")

    def behaviour(self, game):
        pass


# Create a Deck class
class Deck:

    def __init__(self, game):
        self.game = game

        self.discard = []

        # Create a list of cards
        self.cards = [
            Card(Number(["1", "Yellow"]), SkipEveryone(["Pink"])),
            Card(Number(["1", "Yellow"]), Wild(["Black"])),
            Card(Number(["2", "Yellow"]), Number(["1", "Turquoise"])),
            Card(Number(["2", "Yellow"]), Number(["8", "Turquoise"])),
            Card(Number(["3", "Yellow"]), Number(["1", "Purple"])),
            Card(Number(["3", "Yellow"]), DrawFive(["Pink"])),
            Card(Number(["4", "Yellow"]), DrawFive(["Pink"])),
            Card(Number(["4", "Yellow"]), Flip(["Purple"])),
            Card(Number(["5", "Yellow"]), Number(["8", "Turquoise"])),
            Card(Number(["5", "Yellow"]), Number(["9", "Purple"])),
            Card(Number(["6", "Yellow"]), SkipEveryone(["Orange"])),
            Card(Number(["6", "Yellow"]), WildDrawColour(["Black"])),
            Card(Number(["7", "Yellow"]), Number(["2", "Orange"])),
            Card(Number(["7", "Yellow"]), Number(["6", "Purple"])),
            Card(Number(["8", "Yellow"]), Number(["1", "Pink"])),
            Card(Number(["8", "Yellow"]), Number(["2", "Orange"])),
            Card(Number(["9", "Yellow"]), Number(["4", "Purple"])),
            Card(Number(["9", "Yellow"]), Number(["5", "Turquoise"])),

            Card(Number(["1", "Red"]), Number(["2", "Purple"])),
            Card(Number(["1", "Red"]), Number(["3", "Pink"])),
            Card(Number(["2", "Red"]), DrawFive(["Purple"])),
            Card(Number(["2", "Red"]), Reverse(["Orange"])),
            Card(Number(["3", "Red"]), Number(["7", "Pink"])),
            Card(Number(["3", "Red"]), WildDrawColour(["Black"])),
            Card(Number(["4", "Red"]), DrawFive(["Purple"])),
            Card(Number(["4", "Red"]), Flip(["Orange"])),
            Card(Number(["5", "Red"]), Number(["2", "Pink"])),
            Card(Number(["5", "Red"]), Number(["5", "Turquoise"])),
            Card(Number(["6", "Red"]), Number(["9", "Orange"])),
            Card(Number(["6", "Red"]), SkipEveryone(["Pink"])),
            Card(Number(["7", "Red"]), Number(["1", "Orange"])),
            Card(Number(["7", "Red"]), Number(["5", "Purple"])),
            Card(Number(["8", "Red"]), Number(["7", "Turquoise"])),
            Card(Number(["8", "Red"]), Reverse(["Purple"])),
            Card(Number(["9", "Red"]), Number(["5", "Purple"])),
            Card(Number(["9", "Red"]), Reverse(["Turquoise"])),

            Card(Number(["1", "Blue"]), SkipEveryone(["Purple"])),
            Card(Number(["1", "Blue"]), SkipEveryone(["Purple"])),
            Card(Number(["2", "Blue"]), Number(["8", "Orange"])),
            Card(Number(["2", "Blue"]), Number(["6", "Pink"])),
            Card(Number(["3", "Blue"]), Number(["2", "Turquoise"])),
            Card(Number(["3", "Blue"]), Number(["8", "Purple"])),
            Card(Number(["4", "Blue"]), DrawFive(["Turquoise"])),
            Card(Number(["4", "Blue"]), Number(["1", "Purple"])),
            Card(Number(["5", "Blue"]), Number(["9", "Pink"])),
            Card(Number(["5", "Blue"]), Reverse(["Orange"])),
            Card(Number(["6", "Blue"]), Reverse(["Purple"])),
            Card(Number(["6", "Blue"]), SkipEveryone(["Turquoise"])),
            Card(Number(["7", "Blue"]), Number(["3", "Orange"])),
            Card(Number(["7", "Blue"]), SkipEveryone(["Orange"])),
            Card(Number(["8", "Blue"]), Number(["4", "Turquoise"])),
            Card(Number(["8", "Blue"]), Reverse(["Turquoise"])),
            Card(Number(["9", "Blue"]), Number(["5", "Orange"])),
            Card(Number(["9", "Blue"]), Flip(["Purple"])),

            Card(Number(["1", "Green"]), Number(["5", "Orange"])),
            Card(Number(["1", "Green"]), Flip(["Orange"])),
            Card(Number(["2", "Green"]), SkipEveryone(["Turquoise"])),
            Card(Number(["2", "Green"]), DrawFive(["Turquoise"])),
            Card(Number(["3", "Green"]), Number(["2", "Purple"])),
            Card(Number(["3", "Green"]), Flip(["Pink"])),
            Card(Number(["4", "Green"]), Number(["9", "Turquoise"])),
            Card(Number(["4", "Green"]), Number(["8", "Pink"])),
            Card(Number(["5", "Green"]), Number(["4", "Turquoise"])),
            Card(Number(["5", "Green"]), Number(["7", "Orange"])),
            Card(Number(["6", "Green"]), Number(["5", "Pink"])),
            Card(Number(["6", "Green"]), WildDrawColour(["Black"])),
            Card(Number(["7", "Green"]), Number(["2", "Turquoise"])),
            Card(Number(["7", "Green"]), Number(["6", "Orange"])),
            Card(Number(["8", "Green"]), Number(["9", "Turquoise"])),
            Card(Number(["8", "Green"]), Reverse(["Pink"])),
            Card(Number(["9", "Green"]), DrawFive(["Pink"])),
            Card(Number(["9", "Green"]), Reverse(["Orange"])),

            Card(DrawOne(["Yellow"]), Number(["1", "Pink"])),
            Card(DrawOne(["Yellow"]), Number(["8", "Purple"])),
            Card(DrawOne(["Red"]), Number(["3", "Pink"])),
            Card(DrawOne(["Red"]), Number(["4", "Pink"])),
            Card(DrawOne(["Blue"]), Number(["6", "Pink"])),
            Card(DrawOne(["Blue"]), Number(["6", "Turquoise"])),
            Card(DrawOne(["Green"]), Number(["6", "Orange"])),
            Card(DrawOne(["Green"]), Number(["6", "Turquoise"])),

            Card(Reverse(["Yellow"]), Flip(["Turquoise"])),
            Card(Reverse(["Yellow"]), Wild(["Black"])),
            Card(Reverse(["Red"]), Number(["3", "Purple"])),
            Card(Reverse(["Red"]), Number(["7", "Turquoise"])),
            Card(Reverse(["Blue"]), Number(["4", "Orange"])),
            Card(Reverse(["Blue"]), Wild(["Black"])),
            Card(Reverse(["Green"]), Number(["1", "Orange"])),
            Card(Reverse(["Green"]), Number(["7", "Pink"])),

            Card(Flip(["Yellow"]), Number(["4", "Pink"])),
            Card(Flip(["Yellow"]), Number(["8", "Orange"])),
            Card(Flip(["Red"]), Number(["3", "Purple"])),
            Card(Flip(["Red"]), Number(["8", "Pink"])),
            Card(Flip(["Blue"]), Number(["6", "Purple"])),
            Card(Flip(["Blue"]), Number(["7", "Purple"])),
            Card(Flip(["Green"]), Number(["3", "Turquoise"])),
            Card(Flip(["Green"]), WildDrawColour(["Black"])),

            Card(Skip(["Yellow"]), Number(["3", "Orange"])),
            Card(Skip(["Yellow"]), Flip(["Turquoise"])),
            Card(Skip(["Red"]), DrawFive(["Orange"])),
            Card(Skip(["Red"]), Wild(["Black"])),
            Card(Skip(["Blue"]), Number(["1", "Turquoise"])),
            Card(Skip(["Blue"]), Number(["9", "Pink"])),
            Card(Skip(["Green"]), Number(["4", "Purple"])),
            Card(Skip(["Green"]), Number(["9", "Orange"])),

            Card(Wild(["Black"]), Number(["3", "Turquoise"])),
            Card(Wild(["Black"]), Number(["5", "Pink"])),
            Card(Wild(["Black"]), Number(["7", "Purple"])),
            Card(Wild(["Black"]), Flip(["Pink"])),

            Card(WildDrawTwo(["Black"]), Number(["2", "Pink"])),
            Card(WildDrawTwo(["Black"]), Number(["4", "Orange"])),
            Card(WildDrawTwo(["Black"]), Number(["7", "Orange"])),
            Card(WildDrawTwo(["Black"]), Number(["9", "Purple"]))
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

    def place_card(self, card):
        sides = (card.light, card.dark)
        side = sides[::self.game.flip][0]
        side.behaviour(self.game)
        self.discard.append(card)
