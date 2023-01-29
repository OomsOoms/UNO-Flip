from deck import *


# Create a Player class
class Player:
    def __init__(self, game):
        # Assign the player a hand of cards from the deck
        self.game = game
        self.hand = game.deck.deal_hand()

    def get_playable_cards(self, discard_card, hand):
        # Check which side of the card is facing up (light or dark) based on the direction of the game
        sides = (discard_card.light.side, discard_card.dark.side)
        side_to_check = set(
            sides[::self.game.flip][0])

        # Get a list of cards that can be played based on the side of the discard card that is facing up
        playable_cards = [card for card in hand if side_to_check.intersection(
            set([card.light.side, card.dark.side][::self.game.flip][0])) or set([card.light.side, card.dark.side][::self.game.flip][0]) == set(["Black"])]

        # Return the list of playable cards
        return playable_cards


class Game:
    def __init__(self):
        # Create a new deck of cards and assign it to the game
        self.deck = Deck(self)
        # Create 3 players and assign them to the game
        self.players = {
            "P1": Player(self),
            "P2": Player(self)
        }

        # Set the direction of the game to normal (1) or reverse (-1)
        self.direction = 1  # 1 for normal, -1 for reverse

        self.flip = 1  # 1 for light, -1 for dark

    def deal_hands(self):
        # Deal a hand of cards to all players
        for player in self.players.values():
            player.hand = self.deck.deal_hand()

    def check_winner(self, player):
        # Check if the player has won by checking if their hand is empty
        return len(player.hand) == 0

    def start_card(self):
        # Pick up a card and check if it's a number card
        while True:
            temp = self.deck.pick_card()
            print(temp.light.side)
            self.deck.discard.append(temp)

            if temp.light.type == "Number":
                break

    def play_game(self):
        # Deal initial hands to all players
        self.deal_hands()
        # Pick up a card and check if it's a number card
        self.start_card()

        players_list = list(self.players.keys())

        # Create an index variable to keep track of the current player, starts at -1 becuase of prerequisites
        self.current_player_index = -1

        self.prerequisite = None

        # Main game loop
        while True:
            if self.prerequisite != "SkipEveryone":
                # Update the current player index based on the direction of the game. Modulo operator is used to keep the index within the bounds of the players_list.
                self.current_player_index = (
                    self.current_player_index + self.direction) % len(players_list)
                
            if self.prerequisite == "WildDrawColour":
                print(WildDrawColour)
                while True:
                    card = self.deck.pick_card()
                    sides = (card.light, card.dark)
                    colour = sides[::self.flip][0]

                    sides = (discard_card.light, discard_card.dark)
                    discard_colour = sides[::self.flip][0]
                    
                    current_player.hand.append(card)

                    print(discard_colour.side) 
                    print(colour.side)
                    if colour.side[-1] == discard_colour.side[-1]:
                        break
                
            self.prerequisite = None
            

            # Get the current player name and object
            self.current_player_name = players_list[self.current_player_index]  # String
            current_player = self.players[self.current_player_name]  # Player object

            # Get the last card in the discard pile. self.flip == 1 when light and -1 when dark. Then combares all cards to the top card and returns all the playable ones.
            discard_card = self.deck.discard[-1]

            playable_cards = current_player.get_playable_cards(
                discard_card, current_player.hand)
            
            ###
            ###
            ###
               # Command-line interface
            print(f"\nPlayer: {self.current_player_name}")
            print(
                f"Discard pile: {(None, discard_card.light.side, discard_card.dark.side)[self.flip]}")

            # Prints the light or dark side of the players hand depending on self.flip
            print(
                f"Hand: {[set((x.light.side, x.dark.side)[::self.flip][0]) for x in current_player.hand]}")

            # Prints all of the playable cards where at least one item in card.light/dark.side is a subset of the discard
            print(
                f"Playable cards: {[set((x.light.side, x.dark.side)[::self.flip][0]) for x in playable_cards]}")
            
            ###
            ###
            ###

            card_index = input("Position of card to play or p to pick up ")
            try:
                print(playable_cards[int(card_index)-1].light.type)
                print(playable_cards[int(card_index)-1].dark.type)
            except:
                pass

            if card_index == "p":
                current_player.hand.append(self.deck.pick_card())
            else:
                self.deck.place_card(playable_cards[int(card_index)-1])
                current_player.hand.remove(playable_cards[int(card_index)-1])

            # Win condition
            if self.check_winner(current_player):
                print(f"Player {self.current_player_name} wins!")
                break

Game().play_game()