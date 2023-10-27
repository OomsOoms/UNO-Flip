import uuid
from random import randint

from api.deck import *
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

        def __init__(self) -> None:
            self.game_id = randint(100000, 999999)
            self.players = {}
            self.deck = Deck(self)
            self.game_direction = 1
            self.prerequisite_func = lambda self: logger.debug("Running default prerequisite_func")
            self.current_player_index = 0
            self.started = False

            logger.info(f"Game created {self.game_id}")

        @property
        def current_player_id(self) -> str:
            """
            Get the ID of the current player.

            :return: ID of the current player.
            :rtype: str
            """
            return list(self.players.keys())[self.current_player_index]

        def add_player(self, player_name: str) -> str:
            """
            Adds a player to the game.

            :param player_name: Name of the player.
            :type player_name: str
            :return: ID of the new player.
            :rtype: str
            """
            player_id = str(uuid.uuid4())
            self.players[player_id] = Player(self, player_name)
            logger.info(f"Added player: {player_name} {player_id} to game {self.game_id}")
            return player_id
        
        def remove_player(self, player_id: str) -> None:
            """
            Removes a player from the game.

            :param player_id: ID of the player to remove.
            :type player_id: str
            """
            del self.players[player_id]
            logger.info(f"Removed player: {player_id} from game {self.game_id}")

        def start_game(self):
            """
            Starts the game by selecting the starting card and determining the initial player.

            This method continues to select and discard cards until a number card is selected.
            It then sets the current player for the game.

            If a non-number card is selected as the start card, it keeps selecting new start cards until a number card is chosen.

            If a player is added after the game has started, the `add_player` is method overwritten so it will do nothing.
            """
            logger.info(f"Game started {self.game_id}")
            while True:
                # Keep selecting and discarding cards until a number card is selected
                start_card = self.deck.pick_card(self)
                self.deck.discard.append(start_card)
                if start_card.light.type == "Number":
                    logger.debug(f"Selected start card {[start_card.light.side, start_card.dark.side][self.deck.flip]}")
                    break
                logger.debug(f"Selecting new start card {[start_card.light.side, start_card.dark.side][self.deck.flip]}")

            self.current_player_index = randint(0, len(self.players)-1)
            logger.debug(f"Current player index: {self.current_player_index} and player id: {self.current_player_id}")
            self.started = True 

        def get_game_state(self, player_id):
            """
            Returns the current state of the game for a given player, from their 'view' of the game only showing the back of other players cards

            :param player_id: ID of the player
            :type player_id: str
            :return: Dictionary containing the discard pile, the player's hand, and the back of the opponent's hands
            :rtype: dict
            """
            discard_side = [self.deck.discard[-1].light.side, self.deck.discard[-1].dark.side][self.deck.flip]
            logger.debug(discard_side)
            player_object = self.players[player_id]

            player_hand = {}
            for index, card in enumerate(player_object.hand):
                card_side = [card.light.side, card.dark.side][self.deck.flip]
                is_playable = any(item in discard_side for item in card_side) and player_id == self.current_player_id
                player_hand[index] = {"side": card_side, "is_playable": is_playable}

            opponent_hands = {}
            for opponent_id, opponent in self.players.items():
                if opponent_id != player_id:
                    opponent_hand = []
                    for card in opponent.hand:
                        card_side = [card.light.side, card.dark.side][(self.deck.flip + 1) % 2]
                        opponent_hand.append(card_side)
                    opponent_hands[opponent.name] = opponent_hand

            return {"discard": discard_side, "player_hand": player_hand, "opponent_hands": opponent_hands}
        
        def select_card(self, player_id, card):
 
            # Do another card check to prevent cheating from the client
            # Check if the user_id, specific to then users session, is the same as the current player
            discard_side = [self.deck.discard[-1].light.side, self.deck.discard[-1].dark.side][self.deck.flip]
            card_side = [card.light.side, card.dark.side][self.deck.flip]
            card_behaviour = [card.light.behaviour, card.dark.behaviour][self.deck.flip]
            # Only if the card is playable
            if any(item in discard_side for item in card_side):
                self.players[player_id].hand.remove(card)
                self.prerequisite_func = card_behaviour
                logger.debug(f"Player {player_id} selected card {card_side} removed adding prequisite_func to queue")
                self.end_turn()
                    
        def end_turn(self):

            # Update the current player index based on the direction of the game, kept in bounds with Modulo operator
            self.current_player_index  = (self.current_player_index  + self.game_direction) % len(self.players)
            self.current_player_id = list(self.players.keys())[self.current_player_index]

            self.prerequisite_func = lambda self=self: logger.debug("Running default prerequisite_func")

            logger.debug(f"Incrementing current player index to {self.current_player_index} and player id to {self.current_player_id} and running prerequisite_func")
