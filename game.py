from deck import *
from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)

# Create a Player class that has a hand of cards and a game object
class Player:

    def __init__(self, game):
        # Assign the player a hand of cards from the deck
        self.game = game
        self.hand = game.deck.deal_hand()

        logger.debug("Player created")


class Game:
    
    game_direction = 1  # 1 for normal, -1 for reverse
    current_player_turn = -1
    players = {}

    def __init__(self):
        self.deck = Deck(self)

        logger.debug("Game created")

    def add_player(self, player_name):
        self.players[player_name] = Player(self)
        
        logger.debug(f"Player {player_name} added")

    def generate_start_card(self):
        # Pick up a card and check if it's a number card
        while True:
            start_card = self.deck.pick_card(self)
            # This adds it to the discard pile which is what the user can see
            self.deck.discard.append(start_card)
            # If it's a number card, break out of the loop
            if start_card.light.type == "Number":
                logger.debug(f"Selected start card {[start_card.light.side, start_card.dark.side][self.deck.flip]}")
                break
            
            logger.debug("Selecting new start card")
    
    #check prerequisites
    def check_prerequisites(self):
        pass

    # This is called at the end of a turn
    def end_turn(self):
        # Update the current player index based on the direction of the game, kept in bounds with Modulo operator
        self.current_player_turn = (self.current_player_turn + self.game_direction) % len(self.players_names)
        
        logger.debug("Incrementing current player index")

    def get_game_sate(self):
        # Get the current player name and object for this turn/loop
        current_player_name = list(self.players.keys())[self.current_player_turn]
        current_player_object = self.players[current_player_name]
        player_hand = {}
        discard_card = [self.deck.discard[-1].light.side, self.deck.discard[-1].dark.side][self.deck.flip]
        for card in current_player_object.hand:
            card_side = [card.light.side, card.dark.side][self.deck.flip]
            is_playable = any(item in self.deck.discard[-1] for item in card_side)
            player_hand[card] = is_playable

        logger.debug(f"Current player: {current_player_name}, Playable cards: {[card.light.side for card, is_playable in player_hand.items() if is_playable]}")

        return current_player_object, player_hand
        