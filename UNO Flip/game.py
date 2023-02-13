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
<<<<<<< HEAD
        # Place the starting card, deal player hands
        self.start_card()
        
        # Keep track of players
        self.players_list = list(self.players.keys())
        # Start with player 1
        self.current_player_index = -1

        # Prerequisites for a turn
        self.prerequisite = None
        # Number of cards to pick up
=======
        # Places the starting card, player hands are dealt when player object is created
        self.start_card()
        
        # List of player
        self.players_list = list(self.players.keys())
        # 1 is added at the start for every go to increment, must start on 0 for player 1
        self.current_player_index = -1

        # Code checks these before a turn and runs code depending on what they are, for example skipping everyone
        self.prerequisite = None
>>>>>>> c1bd3a597ac5b1448635ecbf48828abc9e160456
        self.num_pickup = 0
        # Flag for UNO call
        uno_called = False

        # Main game loop
        while True:
<<<<<<< HEAD
=======
            print(len(self.deck.cards))
            print(self.prerequisite)
            print(self.num_pickup)
>>>>>>> c1bd3a597ac5b1448635ecbf48828abc9e160456
            # Get the last placed card in the discard pile and check the side that self.flip is currently on
            discard_card = self.deck.discard[-1]
            discard_side = (discard_card.light, discard_card.dark)[::self.flip][0]

<<<<<<< HEAD
            # Update the current player index based on the direction of the game, kept in bounds with Modulo operator
            if self.prerequisite != "SkipEveryone":
                self.current_player_index = (self.current_player_index + self.direction) % len(self.players_list)

            # Get the current player name and object for this turn/loop
            self.current_player_name = self.players_list[self.current_player_index] # String
            current_player = self.players[self.current_player_name] # Player object

=======
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
>>>>>>> c1bd3a597ac5b1448635ecbf48828abc9e160456
            if self.prerequisite == "WildDrawColour":
                # Picks up cards until the colour specified is picked up
                while True:
                    card = self.deck.pick_card(self)
                    current_player.hand.append(card)
                    print([card.light.side, card.dark.side][::self.flip][0])

<<<<<<< HEAD
                    # Check if the dark side of the card matches the color of the discard card
=======
                    # Only needs to be for the dark side as WildDrawColour is a dark side card
>>>>>>> c1bd3a597ac5b1448635ecbf48828abc9e160456
                    if card.dark.side[-1] == discard_side.side[-1]:
                        self.deck.place_card(card)
                        self.prerequisite = None
                        break
<<<<<<< HEAD
                # Skip the turn after picking up
                continue

            # Reset prerequisites for next turn
            self.prerequisite = None

            # Check if there are cards to pickup or playable cards can be checked normally
            if self.num_pickup == 0:
                # Get a list of playable cards depending on current `discard_side` and `self.flip`
=======
                # Skips the turn after picking up
                continue

            # Resets the prerequisites for the next turn
            self.prerequisite = None

            # If there are no cards to pickup, playable cards are checked normally
            if self.num_pickup == 0:
                # Get a list of cards that can be played depending on self.flip
>>>>>>> c1bd3a597ac5b1448635ecbf48828abc9e160456
                playable_cards = [card for card in current_player.hand if set(discard_side.side).intersection(set(
                    [card.light.side, card.dark.side][::self.flip][0]))
                    or None == [card.light.side, card.dark.side][::self.flip][0][-1]]

<<<<<<< HEAD
                # If current discard card is a wild, all cards in player's hand are playable
                if None in discard_side.side:
                    playable_cards = current_player.hand
=======
                # If card is a wild, can occours when the deck is flipped for the first time
                if None in discard_side.side:
                    playable_cards = current_player.hand

                if None == discard_side.type[-1]:
                    playable_cards = current_player.hand

            # If there are cards to pickup, playable are only draw cards
>>>>>>> c1bd3a597ac5b1448635ecbf48828abc9e160456
            else:
                # Get a list of playable cards based on the current "Draw" card in discard pile
                playable_cards = []
                # Draw cards can only be placed if the color or number is the same or lower
                for card in current_player.hand:
                    if "DrawOne" in [card.light.type, card.dark.type][::self.flip][0]:
                        if "DrawOne" in discard_side.type:
                            playable_cards.append(card)
                    elif "DrawTwo" in [card.light.type, card.dark.type][::self.flip][0]:
                        if "DrawOne" in discard_side.type or "DrawTwo" in discard_side.type:
                            playable_cards.append(card)
                    elif "DrawFive" in [card.light.type, card.dark.type][::self.flip][0]:
                        playable_cards.append(card)

<<<<<<< HEAD
                # If there is no playable card, pick up cards for the number specified
=======
                # If there is no playable card they pick up
>>>>>>> c1bd3a597ac5b1448635ecbf48828abc9e160456
                if len(playable_cards) == 0:
                    for i in range(self.num_pickup):
                        current_player.hand.append(self.deck.pick_card(self))
                    self.num_pickup = 0
                    continue

            # Command-line interface
            print(f"\nPlayer: {self.current_player_name}")
            print(f"Discard pile: {discard_side.side}")
<<<<<<< HEAD
            print(f"Hand {len(current_player.hand)}: {[(x.light.side, x.dark.side)[::self.flip][0] for x in current_player.hand]}")
            print(f"Playable cards: {[(x.light.side, x.dark.side)[::self.flip][0] for x in playable_cards]}")

            # Player turn handling
            player_choice = input("Position of card to play, enter to pick up ")

            # If player chooses to play a card
            if player_choice.isdigit():
                # Place the specified card
                chosen_card = playable_cards[int(player_choice) - 1]
                self.deck.place_card(chosen_card)
                current_player.hand.remove(chosen_card)

                # Check for win condition
                if len(current_player.hand) == 0:
                    print(f"Player {self.current_player_name} wins!")
                    break

                # Check if player wants to call UNO, this is before they place the card
                call_uno = input("Before card, player name of uno-caller, or enter to skip ")
                if call_uno == self.current_player_name:
                    if len(current_player.hand) > 1:
                        # Penalties for not calling UNO in time
                        uno_called = True
                        for i in range(2):
                            current_player.hand.append(self.deck.pick_card(self))

                elif call_uno != "":
                    for x in range(2):
                        self.players[call_uno].hand.append(self.deck.pick_card(self))
                
            # If player chooses to pick up a card
=======

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

>>>>>>> c1bd3a597ac5b1448635ecbf48828abc9e160456
            else:
                # Pick up either 1 or stacked pickup amount of cards
                pickup_amount = 1 if self.num_pickup < 2 else self.num_pickup
                for _ in range(pickup_amount):
                    card = self.deck.pick_card(self)
                    current_player.hand.append(card)
<<<<<<< HEAD
                    
                    # Check if newly picked up card is playable
                    card_side = [card.light.side, card.dark.side][::self.flip][0]
                    if set(discard_side.side).intersection(set(card_side)):
                        print(card_side)
                        player_choice = input("Enter to place, 1 to keep ")
                        if player_choice == "":
                            current_player.hand.remove(card)
                            self.deck.place_card(card)


            # Calling UNO, this concept doesn't work in command-line games, only current player can call before playing
            # It will make more sense when there is a GUI
            # There will be a button that can pressed after the players turn at any time
            # This is after they place the card

            call_uno = input("After card, player name of uno-caller, or enter to skip ")
            if not uno_called:
                if call_uno in self.players_list:
                        # If there is more than one card the player that calls it picks up
                        if len(current_player.hand) > 1:
                            print("1")
                            for x in range(2):
                                self.players[call_uno].hand.append(self.deck.pick_card(self))

                        # If there is one card and the current player called it
                        elif len(current_player.hand) == 1 and self.current_player_name == call_uno:
                            print("2")
                            pass
                        
                        # If it's the not the current player and there is one card the current player picks up
                        elif len(current_player.hand) == 1:
                            print("3")
                            for x in range(2):
                                current_player.hand.append(self.deck.pick_card(self))

            # If UNO already called not called 
            elif uno_called and call_uno != self.current_player_name and call_uno != "":
                for x in range(2):    
                    self.players[call_uno].hand.append(self.deck.pick_card(self))
    
=======

                    # Check if new card is playable
                    if set(discard_side.side).intersection(set([card.light.side, card.dark.side][::self.flip][0])):
                        print([card.light.side, card.dark.side][::self.flip][0])
                        # Enter to place, any character to keep
                        player_choice = input("enter to place, 1 to keep ")
                        if player_choice == "":
                            current_player.hand.remove(card)
                            self.deck.place_card(current_player.hand[-1])

            

>>>>>>> c1bd3a597ac5b1448635ecbf48828abc9e160456
Game().play_game()
