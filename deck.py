import random

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
        pass

class Flip(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        game.flip *= -1
        game.deck.discard = game.deck.discard[::-1]

class DrawOne(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        game.num_pickup += 1

class Reverse(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        game.direction *= -1

class Wild(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        colour = input("Pick a colour ")
        self.side = [colour]

class WildDrawTwo(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        colour = input("Pick a colour ")
        self.side = [colour]
        game.num_pickup += 2

class DrawFive(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        game.num_pickup += 5

class SkipEveryone(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        game.prerequisite = self.type

class WildDrawColour(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        game.prerequisite = self.type
        colour = input("Pick a colour ")
        self.side = [colour]
        return colour

class Skip(Side):
    def __init__(self, side):
        super().__init__(side, self.__class__.__name__)

    def behaviour(self, game):
        game.current_player_index = (game.current_player_index + game.direction) % len(game.players_list)


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
        Card(Number(["1", "Yellow"]), SkipEveryone(["SkipEveryone", "Pink"])),
        Card(Number(["1", "Yellow"]), Wild(["Wild", None])),
        Card(Number(["2", "Yellow"]), Number(["1", "Turquoise"])),
        Card(Number(["2", "Yellow"]), Number(["8", "Turquoise"])),
        Card(Number(["3", "Yellow"]), Number(["1", "Purple"])),
        Card(Number(["3", "Yellow"]), DrawFive(["DrawFive", "Pink"])),
        Card(Number(["4", "Yellow"]), DrawFive(["DrawFive", "Pink"])),
        Card(Number(["4", "Yellow"]), Flip(["Flip", "Purple"])),
        Card(Number(["5", "Yellow"]), Number(["8", "Turquoise"])),
        Card(Number(["5", "Yellow"]), Number(["9", "Purple"])),
        Card(Number(["6", "Yellow"]), SkipEveryone(["SkipEveryone", "Orange"])),
        Card(Number(["6", "Yellow"]), WildDrawColour(["WildDrawColour", None])),
        Card(Number(["7", "Yellow"]), Number(["2", "Orange"])),
        Card(Number(["7", "Yellow"]), Number(["6", "Purple"])),
        Card(Number(["8", "Yellow"]), Number(["1", "Pink"])),
        Card(Number(["8", "Yellow"]), Number(["2", "Orange"])),
        Card(Number(["9", "Yellow"]), Number(["4", "Purple"])),
        Card(Number(["9", "Yellow"]), Number(["5", "Turquoise"])),

        Card(Number(["1", "Red"]), Number(["2", "Purple"])),
        Card(Number(["1", "Red"]), Number(["3", "Pink"])),
        Card(Number(["2", "Red"]), DrawFive(["DrawFive", "Purple"])),
        Card(Number(["2", "Red"]), Reverse(["Reverse", "Orange"])),
        Card(Number(["3", "Red"]), Number(["7", "Pink"])),
        Card(Number(["3", "Red"]), WildDrawColour(["WildDrawColour", None])),
        Card(Number(["4", "Red"]), DrawFive(["DrawFive", "Purple"])),
        Card(Number(["4", "Red"]), Flip(["Flip", "Orange"])),
        Card(Number(["5", "Red"]), Number(["2", "Pink"])),
        Card(Number(["5", "Red"]), Number(["5", "Turquoise"])),
        Card(Number(["6", "Red"]), Number(["9", "Orange"])),
        Card(Number(["6", "Red"]), SkipEveryone(["SkipEveryone", "Pink"])),
        Card(Number(["7", "Red"]), Number(["1", "Orange"])),
        Card(Number(["7", "Red"]), Number(["5", "Purple"])),
        Card(Number(["8", "Red"]), Number(["7", "Turquoise"])),
        Card(Number(["8", "Red"]), Reverse(["Reverse"< "Purple"])),
        Card(Number(["9", "Red"]), Number(["5", "Purple"])),
        Card(Number(["9", "Red"]), Reverse(["Reverse", "Turquoise"])),
    
        Card(Number(["1", "Blue"]), SkipEveryone(["SkipEveryone", "Purple"])),
        Card(Number(["1", "Blue"]), SkipEveryone(["SkipEveryone", "Purple"])),
        Card(Number(["2", "Blue"]), Number(["8", "Orange"])),
        Card(Number(["2", "Blue"]), Number(["6", "Pink"])),
        Card(Number(["3", "Blue"]), Number(["2", "Turquoise"])),
        Card(Number(["3", "Blue"]), Number(["8", "Purple"])),
        Card(Number(["4", "Blue"]), DrawFive(["DrawFive", "Turquoise"])),
        Card(Number(["4", "Blue"]), Number(["1", "Purple"])),
        Card(Number(["5", "Blue"]), Number(["9", "Pink"])),
        Card(Number(["5", "Blue"]), Reverse(["Reverse", "Orange"])),
        Card(Number(["6", "Blue"]), Reverse(["Reverse", "Purple"])),
        Card(Number(["6", "Blue"]), SkipEveryone(["SkipEveryone", "Turquoise"])),
        Card(Number(["7", "Blue"]), Number(["3", "Orange"])),
        Card(Number(["7", "Blue"]), SkipEveryone(["SkipEveryone", "Orange"])),
        Card(Number(["8", "Blue"]), Number(["4", "Turquoise"])),
        Card(Number(["8", "Blue"]), Reverse(["Reverse", "Turquoise"])),
        Card(Number(["9", "Blue"]), Number(["5", "Orange"])),
        Card(Number(["9", "Blue"]), Flip(["Flip", "Purple"])),

        Card(Number(["1", "Green"]), Number(["5", "Orange"])),
        Card(Number(["1", "Green"]), Flip(["Flip", "Orange"])),
        Card(Number(["2", "Green"]), SkipEveryone(["SkipEveryone", "Turquoise"])),
        Card(Number(["2", "Green"]), DrawFive(["DrawFive", "Turquoise"])),
        Card(Number(["3", "Green"]), Number(["2", "Purple"])),
        Card(Number(["3", "Green"]), Flip(["Flip", "Pink"])),
        Card(Number(["4", "Green"]), Number(["9", "Turquoise"])),
        Card(Number(["4", "Green"]), Number(["8", "Pink"])),
        Card(Number(["5", "Green"]), Number(["4", "Turquoise"])),
        Card(Number(["5", "Green"]), Number(["7", "Orange"])),
        Card(Number(["6", "Green"]), Number(["5", "Pink"])),
        Card(Number(["6", "Green"]), WildDrawColour(["WildDrawColour", None])),
        Card(Number(["7", "Green"]), Number(["2", "Turquoise"])),
        Card(Number(["7", "Green"]), Number(["6", "Orange"])),
        Card(Number(["8", "Green"]), Number(["9", "Turquoise"])),
        Card(Number(["8", "Green"]), Reverse(["Reverse", "Pink"])),
        Card(Number(["9", "Green"]), DrawFive(["DrawFive", "Pink"])),
        Card(Number(["9", "Green"]), Reverse(["Reverse", "Orange"])),

        Card(DrawOne(["DrawOne", "Yellow"]), Number(["1", "Pink"])),
        Card(DrawOne(["DrawOne", "Yellow"]), Number(["8", "Purple"])),
        Card(DrawOne(["DrawOne", "Red"]), Number(["3", "Pink"])),
        Card(DrawOne(["DrawOne", "Red"]), Number(["4", "Pink"])),
        Card(DrawOne(["DrawOne", "Blue"]), Number(["6", "Pink"])),
        Card(DrawOne(["DrawOne", "Blue"]), Number(["6", "Turquoise"])),
        Card(DrawOne(["DrawOne", "Green"]), Number(["6", "Orange"])),
        Card(DrawOne(["DrawOne", "Green"]), Number(["6", "Turquoise"])),

        Card(Reverse(["Reverse", "Yellow"]), Flip(["Flip", "Turquoise"])),
        Card(Reverse(["Reverse", "Yellow"]), Wild(["Wild", None])),
        Card(Reverse(["Reverse", "Red"]), Number(["3", "Purple"])),
        Card(Reverse(["Reverse", "Red"]), Number(["7", "Turquoise"])),
        Card(Reverse(["Reverse", "Blue"]), Number(["4", "Orange"])),
        Card(Reverse(["Reverse", "Blue"]), Wild(["Wild", None])),
        Card(Reverse(["Reverse", "Green"]), Number(["1", "Orange"])),
        Card(Reverse(["Reverse", "Green"]), Number(["7", "Pink"])),

        Card(Flip(["Flip", "Yellow"]), Number(["4", "Pink"])),
        Card(Flip(["Flip", "Yellow"]), Number(["8", "Orange"])),
        Card(Flip(["Flip", "Red"]), Number(["3", "Purple"])),
        Card(Flip(["Flip", "Red"]), Number(["8", "Pink"])),
        Card(Flip(["Flip", "Blue"]), Number(["6", "Purple"])),
        Card(Flip(["Flip", "Blue"]), Number(["7", "Purple"])),
        Card(Flip(["Flip", "Green"]), Number(["3", "Turquoise"])),
        Card(Flip(["Flip", "Green"]), WildDrawColour(["WildDrawColour", None])),

        Card(Skip(["Skip", "Yellow"]), Number(["3", "Orange"])),
        Card(Skip(["Skip", "Yellow"]), Flip(["Flip", "Turquoise"])),
        Card(Skip(["Skip", "Red"]), DrawFive(["DrawFive", "Orange"])),
        Card(Skip(["Skip", "Red"]), Wild(["Wild", None])),
        Card(Skip(["Skip", "Blue"]), Number(["1", "Turquoise"])),
        Card(Skip(["Skip", "Blue"]), Number(["9", "Pink"])),
        Card(Skip(["Skip", "Green"]), Number(["4", "Purple"])),
        Card(Skip(["Skip", "Green"]), Number(["9", "Orange"])),

        Card(Wild(["Wild", None]), Number(["3", "Turquoise"])),
        Card(Wild(["Wild", None]), Number(["5", "Pink"])),
        Card(Wild(["Wild", None]), Number(["7", "Purple"])),
        Card(Wild(["Wild", None]), Flip(["Flip", "Pink"])),

        Card(WildDrawTwo(["WildDrawTwo", None]), Number(["2", "Pink"])),
        Card(WildDrawTwo(["WildDrawTwo", None]), Number(["4", "Orange"])),
        Card(WildDrawTwo(["WildDrawTwo", None]), Number(["7", "Orange"])),
        Card(WildDrawTwo(["WildDrawTwo", None]), Number(["9", "Purple"]))
    ]
    
