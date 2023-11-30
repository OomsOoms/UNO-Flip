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
        # Dictionary to store player objects with their IDs as keys
        self.players = {}
        self.deck = Deck(self)  # Create a copy of the deck object
        logger.debug(len(self.deck.cards))
        # 1 for clockwise, -1 for anti-clockwise
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
        Removes a player from the game and adds their cards back to the deck. if its their turn it runs the end_turn function.

        :param player_id: ID of the player to remove.
        :type player_id: str
        """
        player_object = self.players.get(player_id)
                
        # If the player being removed comes before the current player
        if self.game_direction:
            if list(self.players.keys()).index(player_id) < self.current_player_index:
                # Decrement the current player index to account for the player being removed
                self.current_player_index -= 1
            # Removing a player does the same as incrementing player_index by 1
            if self.current_player_index >= len(self.players)-1:
                # If the player_index is out of bounds, reset it to 0
                self.current_player_index = 0

        # TODO: do the same logic when it is a negative game direction
        # TODO: wild cards colour should be reset to None
        self.deck.cards += player_object.hand
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
        while True:
            # Keep selecting and discarding cards until a number card is selected
            start_card = self.deck.pick_card(self)
            self.deck.discard.append(start_card)
            if start_card.light.type == "Number":
                logger.debug(f"Selected start card {[start_card.light.side, start_card.dark.side][self.deck.flip]}")
                break
            logger.debug(f"Selecting new start card {[start_card.light.side, start_card.dark.side][self.deck.flip]}")

        self.current_player_index = randint(0, len(self.players)-1)
        self.started = True 
        logger.info(f"Game started {self.game_id}")

    def get_game_state(self, player_id):
        """
        Returns the current state of the game for a given player, from their 'view' of the game only showing the back of other players cards

        :param player_id: ID of the player
        :type player_id: str
        :return: Dictionary containing the discard pile, the player's hand, and the back of the opponent's hands
        :rtype: dict
        """
        logger.info(f"fetching game state for player {player_id} in game {self.game_id} {len(self.players)} players")

        if self.started:   

            discard_side = [self.deck.discard[-1].light.side, self.deck.discard[-1].dark.side][self.deck.flip]
            player_object = self.players.get(player_id)

            player_hand = []
            for card in player_object.hand:
                card_side = [card.light.side, card.dark.side][self.deck.flip]
                is_playable = (card_side["colour"] == discard_side["colour"] or card_side["action"] == discard_side["action"]) and player_id == self.current_player_id
                player_hand.append(
                        {
                        "colour": card_side["colour"],
                        "action": card_side["action"],
                        "isPlayable": is_playable
                    }
                )

            opponent_hands = []
            for opponent_id, opponent in self.players.items():
                if opponent_id != player_id:
                    cards = []
                    for card in opponent.hand:
                        card_side = [card.light.side, card.dark.side][(self.deck.flip + 1) % 2]
                        cards.append(
                            {
                                "colour": card_side["colour"],
                                "action": card_side["action"]
                            }
                        )
                    opponent_hands.append(
                        {
                            "playerName": opponent.name,
                            "cards": cards
                        }
                    )

            return {
                "type": "game",
                "discard": discard_side,
                "playerHand": player_hand,
                "opponentHands": opponent_hands,
                "playerName": player_object.name,
                "currentPlayerName": self.players[self.current_player_id].name,
                "gameId": self.game_id,
            }

        else:
            is_host = next(iter(self.players)) == player_id
            player_names = [player.name for player in self.players.values()]
            return ({"type": "lobby", "playerNames": player_names, "isHost": is_host, "gameId": self.game_id, "playerId": player_id})

    def play_card(self, player_id, card_index):

        # Checks if the card is playable to prevent cheating from the client
        player_object = self.players.get(player_id)
        card = player_object.hand[card_index]

        if player_id == self.current_player_id:

            # TODO: check if the request comes from the correct player and if the card is a valid playable card

            # Remove the card from the player hand and add it to the discard pile
            self.players[player_id].hand.remove(card)
            self.deck.discard.append(card)

            #self.prerequisite_func = card_behaviour
            card_side = [card.light, card.dark][self.deck.flip]
            logger.debug(f"Player {player_id} selected card {card_side} removed adding prequisite_func to queue")
            
            self.end_turn()

        # When true is returned it tells the API to broadcast the gamestate as the card play was valid
        return True
                
    def end_turn(self):

        # Update the current player index based on the direction of the game, kept in bounds with Modulo operator
        self.current_player_index  = (self.current_player_index  + self.game_direction) % len(self.players)

        self.prerequisite_func = lambda self=self: logger.debug("Running default prerequisite_func")

        logger.debug(f"Incrementing current player index to {self.current_player_index} and player id to {self.current_player_id} and running prerequisite_func")
