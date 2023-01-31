from deck import *


# Create a Player class
class Player:
    def __init__(self, game):
        # Assign the player a hand of cards from the deck
        self.game = game
        self.hand = game.deck.deal_hand()


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

        self.flip = -1  # 1 for light, -1 for dark

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
            temp = self.deck.pick_card(self)
            print(temp.light.side)
            self.deck.discard.append(temp)

            if temp.light.type == "Number":
                break

    def play_game(self):
        # Deal initial hands to all players
        self.deal_hands()
        # Pick up a card and check if it's a number card
        self.start_card()

        self.players_list = list(self.players.keys())

        # Create an index variable to keep track of the current player, starts at -1 becuase of prerequisites
        self.current_player_index = -1

        self.prerequisite = None

        self.num_pickup = 0

        # Main game loop
        while True:
            # Get the last card in the discard pile. self.flip == 1 when light and -1 when dark. Then combares all cards to the top card and returns all the playable ones.
            discard_card = self.deck.discard[-1]

            if self.prerequisite != "SkipEveryone":
                # Update the current player index based on the direction of the game. Modulo operator is used to keep the index within the bounds of the players_list.
                self.current_player_index = (
                    self.current_player_index + self.direction) % len(self.players_list)

            # Get the current player name and object
            self.current_player_name = self.players_list[self.current_player_index]  # String
            current_player = self.players[self.current_player_name]  # Player object
            
            # Picks up cards until the colour specified is picked up
            if self.prerequisite == "WildDrawColour":
                while True:
                    card = self.deck.pick_card(self)

                    # Card is only available on the dark side
                    print(card.dark.side[-1])
                    print(discard_card.dark.side[-1])
                    if card.dark.side[-1] == discard_card.dark.side[-1]:
                        break

            continue

            # Check which side of the card is facing up (light or dark) based on the direction of the game
            sides = (discard_card.light.side, discard_card.dark.side)
            side_to_check = sides[::self.flip][0]
            

            if self.num_pickup == 0:
                # Get a list of cards that can be played based on the side of the discard card that is facing up
                playable_cards = [card for card in current_player.hand if set(side_to_check).intersection(
                    set([card.light.side, card.dark.side][::self.flip][0])) or None == [card.light.side, card.dark.side][::self.flip][0][-1]]
                
                if None == [discard_card.light.type, discard_card.dark.type][::self.flip][0][-1]:
                    playable_cards = current_player.hand
                    
            else:
                # Get a list of cards that can be played based on if they can stack more "Draw" cards
                playable_cards = []
                # Draw cards can only be placed when the colour or number is the same or lower
                for card in current_player.hand:
                    if "DrawOne" in [card.light.type, card.dark.type][::self.flip][0]:
                        if "DrawOne" in [discard_card.light.type, discard_card.dark.type][::self.flip][0]:
                            playable_cards.append(card)
                    elif "DrawTwo" in [card.light.type, card.dark.type][::self.flip][0]:
                        if "DrawOne" in [discard_card.light.type, discard_card.dark.type][::self.flip][0] or "DrawTwo" in [discard_card.light.type, discard_card.dark.type][::self.flip][0]:
                            playable_cards.append(card)
                    elif "DrawFive" in [card.light.type, card.dark.type][::self.flip][0]:
                        playable_cards.append(card)
                
                # If there is no playable card they pick up
                if len(playable_cards) == 0:
                    for i in range(self.num_pickup):
                        current_player.hand.append(self.deck.pick_card(self))
                    self.num_pickup = 0
                    continue
                
            # Resets the prerequisite for the next special card placed
            self.prerequisite = None
        
            
            ###
            ###
            ###
               # Command-line interface
            print(f"\nPlayer: {self.current_player_name}")
            print(
                f"Discard pile: {(None, discard_card.light.side, discard_card.dark.side)[self.flip]}")

            # Prints the light or dark side of the players hand depending on self.flip
            print(
                f"Hand {len(current_player.hand)}: {[(x.light.side, x.dark.side)[::self.flip][0] for x in current_player.hand]}")

            # Prints all of the playable cards where at least one item in card.light/dark.side is a subset of the discard
            print(
                f"Playable cards: {[(x.light.side, x.dark.side)[::self.flip][0] for x in playable_cards]}")
            
            ###                        
            ###
            ###
            
            player_choice = input("Position of card to play or enter to pick up ")

            if player_choice != "":
                self.deck.place_card(playable_cards[int(player_choice)-1])
                current_player.hand.remove(playable_cards[int(player_choice)-1])
                
            else:
                # Pink one card unless there are more pickup stacked
                for i in range(1 if self.num_pickup < 2 else self.num_pickup):
                    card = self.deck.pick_card(self)
                    current_player.hand.append(card)

                    # Check if new card is playable
                    if set(side_to_check).intersection(set([card.light.side, card.dark.side][::self.flip][0])):
                        print(card.light.type)
                        print(card.dark.type)
                        player_choice = input("enter to place, 1 to keep") # Enter to place, any character to keep
                        if player_choice == "":
                            self.deck.place_card(current_player.hand[-1])

            # Win condition
            if self.check_winner(current_player):
                print(f"Player {self.current_player_name} wins!")
                break

Game().play_game()