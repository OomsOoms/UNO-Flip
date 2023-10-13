import uuid
from random import randint

from deck import *
from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)

# Create a Player class that has a hand of cards and a game object
class Player:

    def __init__(self, game, name):
        # Assign the player a hand of cards from the deck
        self.name = name
        self.game = game
        self.hand = game.deck.deal_hand()


class Game:
    
    game_direction = 1  # 1 for normal, -1 for reverse
    cards_to_draw = 0 # Only used if I add stacking draw cards
    players = {}
    current_player_index = 0
    prerequisite_func = lambda self: logger.debug("Running default prerequisite_func")
    game_id = randint(10000000, 99999999)

    def __init__(self):
        self.deck = Deck(self)
        logger.debug("Game created")

    def add_player(self, name):
        player_id = str(uuid.uuid4())
        self.players[player_id] = Player(self, name)
        logger.debug(f"Player {player_id} added")
        return player_id

    def start_game(self):
        # Keep selecting and discarding cards until a number card is selected
        while True:
            start_card = self.deck.pick_card(self)
            self.deck.discard.append(start_card)
            if start_card.light.type == "Number":
                logger.debug(f"Selected start card {[start_card.light.side, start_card.dark.side][self.deck.flip]}")
                break
            
            logger.debug(f"Selecting new start card {[start_card.light.side, start_card.dark.side][self.deck.flip]}")

        self.current_player_index = randint(0, len(self.players)-1)
        self.current_player_id = list(self.players.keys())[self.current_player_index]
        logger.debug(f"Starting game with player index: {self.current_player_index}, player id: {self.current_player_id}")

        return start_card
    
    def get_game_sate(self, player_id):
        if len(self.deck.discard) == 0:
            self.start_game()
            logger.debug("start_game func not run, executing now")

        discard_side = [self.deck.discard[-1].light.side, self.deck.discard[-1].dark.side][self.deck.flip]
        player_object = self.players[player_id]

        if player_id == self.current_player_id:

            player_hand = {}
            for card in player_object.hand:
                card_side = [card.light.side, card.dark.side][self.deck.flip]
                is_playable = any(item in discard_side for item in card_side)
                player_hand[card] = is_playable
                
            logger.debug(f"Current player: {player_id}, Playable cards: {[card.light.side for card, is_playable in player_hand.items() if is_playable]}")
        else:
            # No cards are playable, not the current player turn
            player_hand = {card: False for card in self.players[player_id].hand}

        return discard_side, player_object, player_hand
    
    # Ends the turn when a card is placed, this function is skipped if a prerequisite_func calls the end_turn function
    def select_card(self, player_id, card):
        # Do another card check to prevent cheating from the client
        # Check if the user_id, specific to then users session, is the same as the current player
        if player_id == self.current_player_id and card in self.players[player_id].hand:
            discard_side = [self.deck.discard[-1].light.side, self.deck.discard[-1].dark.side][self.deck.flip]
            card_side = [card.light.side, card.dark.side][self.deck.flip]
            card_behaviour = [card.light.behaviour, card.dark.behaviour][self.deck.flip]
            # Only if the card is playable
            if any(item in discard_side for item in card_side):
                self.players[player_id].hand.remove(card)
                self.prerequisite_func = card_behaviour
                logger.debug(f"Player {player_id} selected card {card_side} removed adding prequisite_func to queue")
                self.end_turn()
                
    # This is called at the end of a turn
    def end_turn(self):
        # Update the current player index based on the direction of the game, kept in bounds with Modulo operator
        self.current_player_index  = (self.current_player_index  + self.game_direction) % len(self.players)
        self.current_player_id = list(self.players.keys())[self.current_player_index]

        self.prerequisite_func = lambda self=self: logger.debug("Running default prerequisite_func")

        logger.debug(f"Incrementing current player index to {self.current_player_index} and player id to {self.current_player_id} and running prerequisite_func")
