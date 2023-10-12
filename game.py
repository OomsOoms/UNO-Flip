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
    players = {}
    current_player_index = 0
    prerequisite_func = lambda self: logger.debug("Running default prerequisite_func")

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
    
    def play_card(self, card):
        self.deck.place_card(card)
    
    # This is called at the end of a turn
    def end_turn(self):
        # Update the current player index based on the direction of the game, kept in bounds with Modulo operator
        self.current_player_index  = (self.current_player_index  + self.game_direction) % len(self.players)
        self.current_player_id = list(self.players.keys())[self.current_player_index]

        self.prerequisite_func = lambda self: logger.debug("Running default prerequisite_func")  # Reset the function to do nothing

        logger.debug(f"Incrementing current player index to {self.current_player_index} and player id to {self.current_player_id} and running prerequisite_func")

        