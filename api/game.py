"""
This module defines the classes for a game and player in the UNO Flip API.

The module game.py defines the classes for a game and player in the UNO Flip API. It contains the following classes:

Player: Represents a player in the game. Each player has a name and a hand of cards.
Game: Represents a game of UNO Flip. It manages the players, deck, game direction, and game state.
The module also includes a start_game method in the Game class, which starts the game by selecting the starting card and determining the initial player.
"""

from uuid import uuid4
from random import randint

from api.deck import *
from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)


class Player:
    """Represents a player in the game.

    Attributes:
        name (str): The name of the player.
        game (Game): The game that the player is in.
        hand (list): The hand of cards that the player has.
    """

    def __init__(self, game, name):
        self.name = name
        self.game = game
        self.hand = game.deck.deal_hand()

    @property
    def score(self):
        """Calculates the score of the player's hand.

        Returns:
            int: The score of the player's hand.
        """
        total_score = 0
        for card in self.hand:
            card_side = [card.light, card.dark][self.game.deck.flip]
            total_score += card_side.score
        return total_score




class Game:
    """Represents a game of UNO Flip.

    The Game class manages the players, deck, game direction, and game state.

    Attributes:
        game_id (int): The ID of the game.
        players (dict): A dictionary of players in the game, with the player ID as the key.
        current_player_index (int): The index of the current player in the players list.
        deck (Deck): The deck of cards for the game.
        game_direction (int): The direction of the game, 1 for clockwise, -1 for anti-clockwise.
        started (bool): Whether the game has started or not.
        game_ended (bool): Whether the game has ended or not.
        uno_called (bool): Whether Uno has been called or not.
        prerequisite_func (func): The function that is run before the next player's turn.
    """

    def __init__(self) -> None:
        """Initialises a game of UNO Flip."""
        self.game_id = randint(100000, 999999)
        logger.info(f"Creating game {self.game_id}")

        self.players = {}
        self.current_player_index = 0
        self.deck = Deck(self)
        self.game_direction = 1  # 1 for clockwise, -1 for anti-clockwise
        self.started = False
        self.game_ended = False
        self.uno_called = False
        self.prerequisite_func = lambda self: logger.debug(
            f"Running default prerequisite_func for game {self.game_id}")

    @property
    def current_player_id(self) -> str:
        """Fetches the ID of the current player.

        Return:
            ID of the current player.
        """
        return list(self.players.keys())[self.current_player_index]

    def add_player(self, player_name: str) -> str:
        """Adds a player to the game.

        Args:
            player_name (str): The name of the player.

        Returns:
            str: The ID of the player that was added.
        """
        # Generate a random UUID for the player ID and add the player to the game
        player_id = str(uuid4())
        logger.info(
            f"Adding player {player_id} to game {self.game_id}")
        self.players[player_id] = Player(self, player_name)
        return player_id

    def remove_player(self, player_id: str) -> None:
        """Removes a player from the game.

        Args:
            player_id (str): The ID of the player to remove.
        """
        logger.info(f"Removing {player_id} from game {self.game_id}")

        player_object = self.players.get(player_id)

        # If the player being removed comes before the current player
        if self.game_direction:
            if list(self.players.keys()).index(player_id) < self.current_player_index:
                # Decrement the current player index to account for the player being removed
                self.current_player_index -= 1
            # Removing a player does the same as incrementing current_player_index by 1
            if self.current_player_index >= len(self.players)-1:
                # If the current_player_index is out of bounds, reset it to 0
                self.current_player_index = 0

        # TODO: do the same logic when it is a negative game direction
        # TODO: wild cards colour should be reset to None
        self.deck.cards += player_object.hand
        del self.players[player_id]

    def start_game(self) -> None:
        """Starts the game, selecting the starting card and determining the initial player.

        This method continues to select and discard cards until a number card is selected.
        It then sets the current player for the game.

        If a non-number card is selected as the start card, it keeps selecting new start cards until a number card is chosen.

        If a player is added after the game has started, the `add_player` is method overwritten so it will do nothing.
        """
        logger.info(f"Starting game {self.game_id}")

        while True:
            # Keep selecting and discarding cards until a number card is selected
            start_card = self.deck.pick_card()
            self.deck.discard.append(start_card)
            if start_card.light.type == "Number":
                break

        self.current_player_index = randint(0, len(self.players)-1)
        self.started = True

    def get_game_state(self, player_id) -> dict:
        """Returns the current state of the game for a given player, from their 'view' of the game only showing the back of other players cards

        Args:
            player_id (str): The ID of the player to get the game state for.

        Returns:
            A dict containing the game state for the player that requested it, this data changes depending if the game has started or not.

            dict: The game state for the player.
        """
        if self.game_ended:
            return {
                "type": "game_over",
                "gameId": self.game_id,
                "playerId": player_id,
                "playerScores": "player_scores",
            }

        elif self.started:
            player_object = self.players.get(player_id)
            discard_side = [self.deck.discard[-1].light.side,
                            self.deck.discard[-1].dark.side][self.deck.flip]
            player_hand = [
                {
                    "colour": [card.light.side, card.dark.side][self.deck.flip]["colour"],
                    "action": [card.light.side, card.dark.side][self.deck.flip]["action"],
                    "isPlayable":
                        ([card.light.side, card.dark.side][self.deck.flip]["colour"]
                         == discard_side["colour"] or [card.light.side, card.dark.side][self.deck.flip]["action"]
                         == discard_side["action"]) and player_id == self.current_player_id
                }
                for card in player_object.hand
            ]
            opponent_hands = [
                {
                    "playerName": opponent.name,
                    "cards": [
                        {
                            "colour": [card.light.side, card.dark.side][(self.deck.flip + 1) % 2]["colour"],
                            "action": [card.light.side, card.dark.side][(self.deck.flip + 1) % 2]["action"]
                        }
                        for card in opponent.hand
                    ]
                }
                for opponent_id, opponent in self.players.items()
                if opponent_id != player_id
            ]

            return {
                "type": "game",
                "gameId": self.game_id,
                "unoCalled": self.uno_called,
                "currentPlayerName": self.players[self.current_player_id].name,
                "discard": discard_side,
                "playerId": player_id,
                "playerName": player_object.name,
                "playerHand": player_hand,
                "isTurn": player_id == self.current_player_id,
                "opponentHands": opponent_hands,
            }

        else:
            is_host = next(iter(self.players)) == player_id
            player_names = [player.name for player in self.players.values()]
            return {
                "type": "lobby",
                "gameId": self.game_id,
                "playerId": player_id,
                "isHost": is_host,
                "playerNames": player_names,
            }

    def play_card(self, player_id, card_index) -> bool:
        """Plays a card from the player's hand.

        Args:
            player_id (int): The ID of the player who is playing the card.
            card_index (int): The index of the card in the player's hand.

        Returns:
            bool: True if the card pick was valid and the game state should be broadcasted, False otherwise.
        """
        player_object = self.players.get(player_id)
        card = player_object.hand[card_index]
        card_side = [card.light.side, card.dark.side][self.deck.flip]
        discard_side = [self.deck.discard[-1].light.side,
                        self.deck.discard[-1].dark.side][self.deck.flip]

        # Checks if the card is playable to prevent cheating from the client
        is_playable = (card_side["colour"] == discard_side["colour"] or card_side["action"]
                       == discard_side["action"]) and player_id == self.current_player_id
        if player_id == self.current_player_id and is_playable:
            logger.debug(
                f"Playing card {card_index} for player {player_id} in game {self.game_id}")

            # Remove the card from the player hand and add it to the discard pile
            self.players[player_id].hand.remove(card)
            self.deck.discard.append(card)

            # Set the prerequisite_func to the behaviour of the card that was played
            self.prerequisite_func = [card.light,
                                      card.dark][self.deck.flip].behaviour
            self.end_turn()
            return True

    def pick_card(self, player_id) -> bool:
        """Picks a card from the deck.

        Returns:
            bool: True if the card pick was valid and the game state should be broadcasted, False otherwise.
        """

        if player_id == self.current_player_id:
            logger.debug(
                f"Picking up card for player {player_id} in game {self.game_id}")
            # Pick a card from the deck and add it to the player's hand
            self.players[player_id].hand.append(self.deck.pick_card())
            self.end_turn()
            return True

    def end_turn(self) -> None:
        """Ends the current player's turn and sets the next player as the current player."""
        if len(self.players[self.current_player_id].hand) == 0:
            logger.info(
                f"Player {self.current_player_id} has won game {self.game_id}")
            self.game_ended = True
            return
        
        logger.debug(
            f"Ending turn for game {self.game_id}, current player is {self.current_player_id}")

        # Update the current player index based on the direction of the game, kept in bounds with Modulo operator
        self.current_player_index = (
            self.current_player_index + self.game_direction) % len(self.players)

        self.prerequisite_func(self)
        self.prerequisite_func = lambda self: logger.debug(
            f"Running default prerequisite_func for game {self.game_id}")

    def call_uno(self, player_id):
        """Calls Uno for the player.

        Args:
            player_id (int): The ID of the player who is calling Uno.   
        """

        # if the current player calls uno and has 1 card left nothing happpens
        # if any player calls uno and the current player has already called uno they draw 2 cards
        # if any player calls uno and the current player has more than 1 card left they draw 2 cards
        # if no one calls uno they have until the next player plays their turn to call uno
        # uno must still be able to be called for the current player and also call out the last player if they missed uno call? not sure about this one

        return False
