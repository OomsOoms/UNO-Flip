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

        self.direction = 1  # 1 for normal, -1 for reverse
        self.flip = 1  # 1 for light, -1 for dark

    def deal_hands(self):
        # Deal a hand of cards to all players
        for player in self.players.values():
            player.hand = self.deck.deal_hand()

    def start_card(self):
        # Pick up a card and check if it's a number card
        while True:
            temp = self.deck.pick_card(self)
            print(temp.light.side)
            self.deck.discard.append(temp)

            if temp.light.type == "Number":
                break

    def play_game(self):
        # Places the starting card, player hands are dealt when player object is created
        self.start_card()
        
        # List of player
        self.players_list = list(self.players.keys())
        # 1 is added at the start for every go to increment, must start on 0 for player 1
        self.current_player_index = -1

        # Code checks these before a turn and runs code depending on what they are, for example skipping everyone
        self.prerequisite = None
        self.num_pickup = 0

        # Main game loop
        while True:
            print(len(self.deck.cards))
            print(self.prerequisite)
            print(self.num_pickup)
            # Get the last placed card in the discard pile and check the side that self.flip is currently on
            discard_card = self.deck.discard[-1]
            discard_side = (discard_card.light, discard_card.dark)[::self.flip][0]

            # Prerequisites are events that must happen before a players turn, like picking up cards
            if self.prerequisite != "SkipEveryone":
                # Update the current player index based on the direction of the game, kept in bounds with Modulo operator
                self.current_player_index = (self.current_player_index + self.direction) % len(self.players_list)

            # Get the current player name and object for this turn/loop
            # String
            self.current_player_name = self.players_list[self.current_player_index]
            # Player object
            current_player = self.players[self.current_player_name]

            # Picks up cards until the colour specified is picked up
            if self.prerequisite == "WildDrawColour":
                while True:
                    card = self.deck.pick_card(self)
                    current_player.hand.append(card)
                    print([card.light.side, card.dark.side][::self.flip][0])

                    # Only needs to be for the dark side as WildDrawColour is a dark side card
                    if card.dark.side[-1] == discard_side.side[-1]:
                        self.deck.place_card(card)
                        self.prerequisite = None
                        break
                # Skips the turn after picking up
                continue

            # Resets the prerequisites for the next turn
            self.prerequisite = None

            # If there are no cards to pickup, playable cards are checked normally
            if self.num_pickup == 0:
                # Get a list of cards that can be played depending on self.flip
                playable_cards = [card for card in current_player.hand if set(discard_side.side).intersection(set(
                    [card.light.side, card.dark.side][::self.flip][0]))
                    or None == [card.light.side, card.dark.side][::self.flip][0][-1]]

                # If card is a wild, can occours when the deck is flipped for the first time
                if None in discard_side.side:
                    playable_cards = current_player.hand

                if None == discard_side.type[-1]:
                    playable_cards = current_player.hand

            # If there are cards to pickup, playable are only draw cards
            else:
                # Get a list of cards that can be played based on if they can stack more "Draw" cards
                playable_cards = []
                # Draw cards can only be placed when the colour or number is the same or lower
                for card in current_player.hand:
                    if "DrawOne" in [card.light.type, card.dark.type][::self.flip][0]:
                        if "DrawOne" in discard_side.type:
                            playable_cards.append(card)
                    elif "DrawTwo" in [card.light.type, card.dark.type][::self.flip][0]:
                        if "DrawOne" in discard_side.type or "DrawTwo" in discard_side.type:
                            playable_cards.append(card)
                    elif "DrawFive" in [card.light.type, card.dark.type][::self.flip][0]:
                        playable_cards.append(card)

                # If there is no playable card they pick up
                if len(playable_cards) == 0:
                    for i in range(self.num_pickup):
                        current_player.hand.append(self.deck.pick_card(self))
                    self.num_pickup = 0
                    continue

            # Command-line interface
            print(f"\nPlayer: {self.current_player_name}")
            print(f"Discard pile: {discard_side.side}")

            # Prints the light or dark side of the players hand depending on self.flip
            print(f"Hand {len(current_player.hand)}: {[(x.light.side, x.dark.side)[::self.flip][0] for x in current_player.hand]}")

            # Prints all of the playable cards where at least one item in card.light/dark.side is a subset of the discard
            print(f"Playable cards: {[(x.light.side, x.dark.side)[::self.flip][0] for x in playable_cards]}")

            player_choice = input("Position of card to play, enter to pick up and UNO to call UNO ")

            # Win condition
            if len(current_player.hand) == 0:
                print(f"Player {self.current_player_name} wins!")
                break

            elif player_choice != "":
                # Places the card specified
                self.deck.place_card(playable_cards[int(player_choice)-1])
                current_player.hand.remove(
                    playable_cards[int(player_choice)-1])
            
            elif player_choice == "UNO":
                # If UNO is incorrectly called, pick 2
                if len(current_player.deck) > 1:
                    for x in range(1):
                        current_player.hand.append(self.deck.pick_card(self))

            else:
                # Pink one card unless there are more pickup stacked
                for i in range(1 if self.num_pickup < 2 else self.num_pickup):
                    card = self.deck.pick_card(self)
                    current_player.hand.append(card)

                    # Check if new card is playable
                    if set(discard_side.side).intersection(set([card.light.side, card.dark.side][::self.flip][0])):
                        print([card.light.side, card.dark.side][::self.flip][0])
                        # Enter to place, any character to keep
                        player_choice = input("enter to place, 1 to keep ")
                        if player_choice == "":
                            current_player.hand.remove(card)
                            self.deck.place_card(current_player.hand[-1])

            

Game().play_game()
