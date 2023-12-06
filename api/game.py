"""This module defines the classes for a game and player in the UNO Flip API."""

from uuid import uuid4
from random import randint
from enum import Enum

from api.deck import *
from api.cards import *
from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)


class Player:
    """Represents a player in the game.

    Attributes:
        name (str): The name of the player.
        game (Game): The game the player is in.
        hand (list): A list of cards in the player's hand.

    Properties:
        score (int): The score of the player's hand.
    """

    def __init__(self, name, game):
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


class Players:

    def __init__(self, game):
        self.game = game
        self.players = {}
        self.current_player_index = 0

    @property
    def current_player_id(self) -> str:
        return list(self.players.keys())[self.current_player_index]

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_id]

    def increment_turn(self) -> None:
        self.current_player_index = (
            self.current_player_index + self.game.direction) % len(self.players)

    def add_player(self, player_name: str) -> str:
        logger.info(f"Adding {player_name} to game {self.game.game_id}")
        player_id = str(uuid4())
        self.players[player_id] = Player(player_name, self.game)
        return player_id

    def remove_player(self, player_id: str) -> None:
        logger.info(f"Removing {player_id} from game {self.game.game_id}")

        player_object = self.players.get(player_id)

        if self.game.direction:
            if list(self.players.keys()).index(player_id) < self.current_player_index:
                self.current_player_index -= 1
            if self.current_player_index >= len(self.players)-1:
                self.current_player_index = 0

        # TODO: do the same logic when it is a negative game direction
        # TODO: wild cards colour should be reset to None
        self.game.deck.cards += player_object.hand
        del self.players[player_id]


class GameState(Enum):
    """An enum to represent the state of the game.

    The values are sent though the API as JSON.

    Attributes:
        LOBBY (str): The game is in the lobby state.
        GAME (str): The game is in the game state.
        GAME_OVER (str): The game is in the game over state.
    """
    LOBBY = "lobby"
    GAME = "game"
    GAME_OVER = "gameOver"


class Game:

    def __init__(self) -> None:
        """Initialises a game of UNO Flip."""
        self.game_id = randint(100000, 999999)
        logger.info(f"Creating game {self.game_id}")

        self.deck = Deck(self)
        self.players = Players(self)
        self.direction = 1  # clockwise: 1, anti-clockwise: -1
        self.state = GameState.LOBBY
        self.prerequisite_func = lambda self: logger.debug(
            f"Running default prerequisite_func for game {self.game_id}")

    def start_game(self) -> None:
        """Starts the game, selecting the starting card and determining the initial player.

        This method continues to select and discard cards until a number card is selected.
        It then sets the current player for the game.

        If a non-number card is selected as the start card, it keeps selecting new start cards until a number card is chosen.

        If a player is added after the game has started, the `add_player` is method overwritten so it will do nothing.
        """
        logger.info(f"Starting game {self.game_id}")

        # Keep selecting and discarding cards until a number card is selected
        while True:
            start_card = self.deck.pick_card()
            self.deck.discard_pile.append(start_card)
            logger.debug(
                f"Selected start card {start_card.colour} {start_card.action}")
            if start_card.card_type == Number:
                break

        self.players.current_player_index = randint(
            0, len(self.players.players)-1)
        self.state = GameState.GAME

    def get_game_state(self, player_id) -> dict:
        """Returns the current state of the game for a given player,
        from their 'view' of the game only showing the back of other players cards

        Args:
            player_id (str): The ID of the player to get the game state for.

        Returns:
            A dict containing the game state for the player that requested it,
            this data changes depending if the game has started or not.

            dict: The game state for the player.
        """
        is_host = next(iter(self.players.players)) == player_id
        discard = self.deck.discard_pile[-1] if self.deck.discard_pile else None
        player_object = self.players.players.get(player_id)
        player_names = [
            player.name for player in self.players.players.values()]
        player_hand = [
            {
                "colour": card.colour,
                "action": card.action,
                "isPlayable":
                    (card.colour == discard.colour or
                     card.action == discard.action) and
                    player_id == self.players.current_player_id
                    if discard else False
            }
            for card in player_object.hand
        ]
        opponent_hands = [
            {
                "playerName": opponent.name,
                "score": opponent.score,
                "cards": [
                    {
                        "colour": [card.light.colour, card.dark.colour][(self.deck.flip + 1) % 2],
                        "action": [card.light.action, card.dark.action][(self.deck.flip + 1) % 2]
                    }
                    for card in opponent.hand
                ]
            }
            for opponent_id, opponent in self.players.players.items()
            if opponent_id != player_id
        ]
        return {
            "type": self.state.value,
            "gameId": self.game_id,
            "discard": self.deck.discard_pile[-1].face_value if discard else None,
            "currentPlayerName": self.players.current_player.name,
            "opponentHands": opponent_hands,
            "playerNames": player_names,

            "playerId": player_id,
            "playerName": self.players.players[player_id].name,
            "playerHand": player_hand,
            "isHost": is_host,
            "isTurn": player_id == self.players.current_player_id,
        }

    def play_card(self, player_id, card_index) -> bool:
        """Plays a card from the player's hand.

        Args:
            player_id (int): The ID of the player who is playing the card.
            card_index (int): The index of the card in the player's hand.

        Returns:
            bool: True if the card pick was valid and the game state should be broadcasted, False otherwise.
        """
        player_object = self.players.players.get(player_id)
        card = player_object.hand[card_index]
        discard = self.deck.discard_pile[-1]

        # Checks if the card is playable to prevent cheating from the client
        is_playable = (card.colour == discard.colour or card.action ==
                       discard.action) and player_id == self.players.current_player_id

        if player_id == self.players.current_player_id and is_playable:
            logger.debug(
                f"Playing card {card_index} for player {player_id} in game {self.game_id}")

            # Remove the card from the player hand and add it to the discard pile
            self.players.players[player_id].hand.remove(card)
            self.deck.discard_pile.append(card)

            # Set the prerequisite_func to the behaviour of the card that was played
            self.prerequisite_func = card.behaviour
            self.end_turn()
            return True

    def pick_card(self, player_id) -> bool:
        """Picks a card from the deck.

        Returns:
            bool: True if the card pick was valid and the game state should be broadcasted, False otherwise.
        """

        if player_id == self.players.current_player_id:
            logger.debug(
                f"Picking up card for player {player_id} in game {self.game_id}")
            # Pick a card from the deck and add it to the player's hand
            self.players.players[player_id].hand.append(self.deck.pick_card())
            self.end_turn()
            return True

    def end_turn(self) -> None:
        """Ends the current player's turn and sets the next player as the current player."""
        if len(self.players.players[self.players.current_player_id].hand) == 0:
            logger.info(
                f"Player {self.players.current_player_id} has won game {self.game_id}")
            self.state = GameState.GAME_OVER
            return

        logger.debug(
            f"Ending turn for game {self.game_id}, current player is {self.players.current_player_id}")

        self.players.increment_turn()

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
