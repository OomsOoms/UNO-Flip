from dict import *


class Player:
    def __init__(self, deck):
        self.hand = deck.deal_hand()


deck = Deck()

players = {
    "P1": [],
    "P2": []
}


for x in players:
    players[x] = Player(deck)

while True:

    card = deck.pick_card()
    print(card.light)
    input()

    deck.discard.append(card)

    while card.type != "number":
        card = deck.pick_card()
        print(card)

        deck.discard.append(card)
