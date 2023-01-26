import random

light_colours = ["Yellow", "Red", "Blue", "Green"]
dark_colours = ["Orange", "Pink", "Purple", "turquoise"]

light_types = [["Wild", "+2"], ["Flip", "+1", "Skip", "Reverse"]]
dark_types = [["Wild", "Pickup"], ["Flip", "+5", "Redo", "Reverse"]]


class Card:

    def __init__(self, light, dark, type):
        self.light = light
        self.dark = dark
        self.type = type


class Number(Card):

    def __init__(self, light, dark):
        super().__init__(light, dark, "Number")

    def behaviour():
        pass


class Flip(Card):
    def __init__(self, light, dark):
        super().__init__(light, dark, "Flip")

    def behaviour():
        flip = not flip


class DrawOne(Card):
    def __init__(self, light, dark):
        super().__init__(light, dark, "DrawOne")

    def behaviour():
        pass


class Deck:
    def __init__(self):

        self.discard = []

        self.cards = [
            Number(["1", "Yellow"], []),
            Number(["1", "Yellow"], []),
            Number(["2", "Yellow"], []),
            Number(["2", "Yellow"], []),
            Number(["3", "Yellow"], []),
            Number(["3", "Yellow"], []),
            Number(["4", "Yellow"], []),
            Number(["4", "Yellow"], []),
            Number(["5", "Yellow"], []),
            Number(["5", "Yellow"], []),
            Number(["6", "Yellow"], []),
            Number(["6", "Yellow"], []),
            Number(["7", "Yellow"], []),
            Number(["7", "Yellow"], []),
            Number(["8", "Yellow"], []),
            Number(["8", "Yellow"], []),
            Number(["9", "Yellow"], []),
            Number(["9", "Yellow"], []),
            Number(["1", "Red"], []),
            Number(["1", "Red"], []),
            Number(["2", "Red"], []),
            Number(["2", "Red"], []),
            Number(["3", "Red"], []),
            Number(["3", "Red"], []),
            Number(["4", "Red"], []),
            Number(["4", "Red"], []),
            Number(["5", "Red"], []),
            Number(["5", "Red"], []),
            Number(["6", "Red"], []),
            Number(["6", "Red"], []),
            Number(["7", "Red"], []),
            Number(["7", "Red"], []),
            Number(["8", "Red"], []),
            Number(["8", "Red"], []),
            Number(["9", "Red"], []),
            Number(["9", "Red"], []),
            Number(["1", "Blue"], []),
            Number(["1", "Blue"], []),
            Number(["2", "Blue"], []),
            Number(["2", "Blue"], []),
            Number(["3", "Blue"], []),
            Number(["3", "Blue"], []),
            Number(["4", "Blue"], []),
            Number(["4", "Blue"], []),
            Number(["5", "Blue"], []),
            Number(["5", "Blue"], []),
            Number(["6", "Blue"], []),
            Number(["6", "Blue"], []),
            Number(["7", "Blue"], []),
            Number(["7", "Blue"], []),
            Number(["8", "Blue"], []),
            Number(["8", "Blue"], []),
            Number(["9", "Blue"], []),
            Number(["9", "Blue"], []),
            Number(["1", "Green"], []),
            Number(["1", "Green"], []),
            Number(["2", "Green"], []),
            Number(["2", "Green"], []),
            Number(["3", "Green"], []),
            Number(["3", "Green"], []),
            Number(["4", "Green"], []),
            Number(["4", "Green"], []),
            Number(["5", "Green"], []),
            Number(["5", "Green"], []),
            Number(["6", "Green"], []),
            Number(["6", "Green"], []),
            Number(["7", "Green"], []),
            Number(["7", "Green"], []),
            Number(["8", "Green"], []),
            Number(["8", "Green"], []),
            Number(["9", "Green"], []),
            Number(["9", "Green"], []),

            DrawOne(["Yellow"], []),
            DrawOne(["Yellow"], []),
            DrawOne(["Red"], []),
            DrawOne(["Red"], []),
            DrawOne(["Blue"], []),
            DrawOne(["Blue"], []),
            DrawOne(["Green"], []),
            DrawOne(["Green"], []),

            Flip(["Yellow"], []),
            Flip(["Yellow"], []),
            Flip(["Red"], []),
            Flip(["Red"], []),
            Flip(["Blue"], []),
            Flip(["Blue"], []),
            Flip(["Green"], []),
            Flip(["Green"], []),
        ]

    def deal_hand(self):
        hand = []
        for x in range(7):
            card = random.choice(self.cards)
            self.cards.remove(card)
            hand.append(card)

        return hand

    def pick_card(self):
        card = random.choice(self.cards)
        self.cards.remove(card)

        return card
