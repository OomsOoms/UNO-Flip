import random

light_colours = ["Yellow", "Red", "Blue", "Green"]
dark_colours = ["Orange", "Pink", "Purple", "turquoise"]

light_types = [["Wild", "+2"], ["Flip", "+1", "Skip", "Reverse"]]
dark_types = [["Wild", "Pickup"], ["Flip", "+5", "Redo", "Reverse"]]


class Card:

    def __init__(self, light_side, dark_side):
        self.light_side = light_side
        self.dark_side = dark_side


class Side:

    def __init__(self, data, type):
        self.side = data
        self.type = type


class Number(Side):

    def __init__(self, data):
        super().__init__(data, "Number")

    def behaviour():
        pass


class Flip(Side):
    def __init__(self, data):
        super().__init__(data, "Flip")

    def behaviour():
        flip = not flip


class Deck:

    def __init__(self):
        self.cards = [
            Card(Number(["1", "Yellow"]), Flip(["Red"])),
            Card(Flip(["Blue"]), Number(["9", "Pink"]))
        ]


deck = Deck()

print(deck.cards[0].light_side)
print(deck.cards[0].dark_side)
