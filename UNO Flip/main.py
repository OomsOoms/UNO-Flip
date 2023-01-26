from cards import *


# Create a Player class
class Player:
    def __init__(self, deck):
        self.hand = deck.deal_hand()


class Game:
    def __init__(self):
        self.deck = Deck(self)
        self.players = {
            "P1": Player(self.deck),
            "P2": Player(self.deck),
            "P3": Player(self.deck)
        }

    def deal_hands(self):
        for player in self.players.values():
            player.hand = self.deck.deal_hand()

    def check_winner(self, player):
        return len(player.hand) == 0

    def start_card(self):
        while True:
            temp = self.deck.pick_card()
            self.deck.discard.append(temp)
            print(temp.light.type)

            if temp.light.type == "Number":
                break

    def play_game(self):
        self.deal_hands()
        self.start_card()

        player = self.players["P1"]

        while not self.check_winner(player):
            pass


Game().play_game()
