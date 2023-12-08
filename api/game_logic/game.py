"""This module defines the classes for a game and player in the UNO API."""

from enum import Enum
from random import randint

from cards import game_modes
from utils.custom_logger import CustomLogger

from .deck import Deck
from .players import Players

logger = CustomLogger(__name__)


class GameState(Enum):
    """An enum to represent the state of the game.

    The values are sent though the API as JSON.

    """
    LOBBY = "lobby"
    GAME = "game"
    GAME_OVER = "gameOver"


class Game:

    def __init__(self) -> None:
        """Initialises a game of UNO."""
        self.game_id = randint(100000, 999999)
        logger.info(f"Creating game {self.game_id}")

        game_mode = game_modes["uno"]
        self.name = game_mode["name"]
        self.wild_colours = game_mode["wild_colours"]

        self.deck = Deck(self, game_mode["cards"])
        self.players = Players(self)
        self.state = GameState.LOBBY
        self.direction = 1  # clockwise: 1, anti-clockwise: -1
        self.prerequisite_func = lambda self: logger.debug(
            f"Running default prerequisite_func for game {self.game_id}")

    def start_game(self, player_id: str) -> None:
        """Starts the game.

        The game can only be started by the host player, and only if there are at least 2 players in the game.

        Args:
            player_id (str): The ID of the player who is trying to start the game.
        """
        logger.info(f"Starting game {self.game_id}")

        if self.state == GameState.LOBBY and list(self.players.keys())[0] == player_id and len(self.players) >= 2:
            self.state = GameState.GAME
            self.players.current_player_index = randint(0, len(self.players)-1)

            while True:
                card = self.deck.pick_card()
                self.deck.discard_pile.append(card)
                if card.__class__.__name__ == "Number":
                    logger.debug(f"Start card {card.colour} {card.action}")
                    break

            return True

    def play_card(self, player_id: str, card_index: int, wild_colour: str) -> bool:
        """Plays a card from the player's hand.

        Args:
            player_id (str): The ID of the player who is playing the card.
            card_index (int): The index of the card in the player's hand.
            wild_colour (str): The colour chosen for a wild card.
        """
        player_object = self.players[player_id]
        card = player_object.hand[card_index]

        if card.is_playable() and player_id == self.players.current_player_id:
            # Check if the card is a wild card and set the colour
            if not card.colour:
                if wild_colour in self.wild_colours.colours(self):
                    card.colour = wild_colour
                else:
                    return

            logger.debug(
                f"Playing card {card_index} for player {player_id} in game {self.game_id}")

            # Remove the card from the player hand and add it to the discard pile
            self.players[player_id].hand.remove(card)
            self.deck.discard_pile.append(card)
            self.prerequisite_func = card.behaviour
            self.end_turn()
            return True

    def pick_card(self, player_id) -> bool:
        """Picks a card from the deck for the player.

        Args:
            player_id (str): The ID of the player who is picking a card.
        """
        if player_id == self.players.current_player_id:
            logger.debug(f"Selecting card for {player_id}")
            # Pick a card from the deck and add it to the player's hand
            self.players[player_id].hand.append(self.deck.pick_card())
            self.end_turn()
            return True

    def end_turn(self) -> None:
        """This method handles the end of a player's turn in the game.

        It checks for various conditions such as winning, updates player scores,
        and progresses the game state.
        """
        player_object = self.players[self.players.current_player_id]

        # Check if the current player has an empty hand/has won the game
        if len(player_object.hand) == 0:
            logger.info(f"Game won by {self.players.current_player_id}")

            # Update player scores based on remaining cards in hands
            for player_id, player in self.players.items():
                for card in player.hand:
                    player_object.score += card.score

            self.state = GameState.GAME_OVER
            return

        # Log the end of the turn and increment to the next player
        logger.debug(f"Ending {self.players.current_player_id}'s turn")
        self.players.increment_turn()

        # Execute prerequisite_func after incrementing the turn, then reset it
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

    def get_game_state(self, player_id: str) -> dict:
        """Returns the current state of the game for a given player,
        from their 'view' of the game only showing the back of other players cards

        Args:
            player_id (str): The ID of the player to get the game state for.

        Returns:
            dict: A dict containing the game state for the player that requested it,
            this data changes depending one the game state.
        """
        player_object = self.players[player_id]
        player_names = [player.name for player in self.players.values()]
        player_hand = [
            {
                "colour": card.colour,
                "action": card.action,
                "isPlayable": card.is_playable() and player_id == self.players.current_player_id
            }
            for card in player_object.hand
        ]
        return {
            "type": self.state.value,
            "name": self.name,
            "gameId": self.game_id,
            "discard": self.deck.discard_pile[-1].face_value if self.deck.discard_pile else None,
            "currentPlayerName": self.players.current_player.name,
            "playerNames": player_names,
            "wildColours": self.wild_colours.colours(self),

            "playerId": player_id,
            "playerName": self.players[player_id].name,
            "playerHand": player_hand,
            "isHost": list(self.players.keys())[0] == player_id,
            "isTurn": player_id == self.players.current_player_id,
            "score": player_object.score,
        }
