"""This module defines the classes for a game and player in the UNO API."""

from enum import Enum
from random import randint

from cards import Type, Colour, build_uno_cards, build_flip_cards
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
        """Initialises a game of UNO.

        This is the default game configuration, but the user can change the settings when the game starts
        using the `start_game` method.

        Game Settings:
        - direction: The direction of play (1 for clockwise, -1 for counterclockwise).
        - hand_size: The number of cards each player starts with.
        - flip: The number of cards to draw when a flip card is played.
        - game_mode: The game mode (e.g., "uno").
        - name: The name of the game.

        Game State:
        - game_id: The unique ID of the game.
        - deck: The deck of cards.
        - players: The players in the game.
        - state: The current state of the game.
        - prerequisite_func: The function to be executed before each turn.
        """
        # Inital Game settings
        self.direction = 1
        self.hand_size = 7
        self.game_mode = "uno"
        self.name = "UNO"

        # Game state
        self.game_id = randint(100000, 999999)
        self.deck = Deck()
        self.players = Players(self)
        self.state = GameState.LOBBY
        self.prerequisite_func = lambda self: logger.debug(
            f"Running default prerequisite_func for game {self.game_id}")
        
        logger.info(f"Created game: {self.game_id}")

    def start_game(self, player_id: str):
        """Starts the game.

        The game can only be started by the host player, and only if there are at least 2 players in the game.

        Args:
            player_id (str): The ID of the player who is trying to start the game.
        """
        logger.info(f"Starting game {self.game_id}")

        if self.state == GameState.LOBBY and list(self.players.keys())[0] == player_id and len(self.players) >= 2:
            # Set the game state to GAME and select a random player to start
            self.state = GameState.GAME
            self.players.current_player_index = randint(0, len(self.players)-1)

            # Build the deck of cards
            # TODO: do this better
            # TODO: also deal with cases where the deck runs out of cards
            self.deck.flip = 0
            self.deck.cards = {"uno": build_uno_cards, "flip": build_flip_cards}[self.game_mode](self.deck)

            # Deal hands to players
            for player in self.players.values():
                player.assign_hand(self.hand_size)

            # Pick a card from the deck to start the discard pile
            while True:
                card = self.deck.pick_card()
                self.deck.discard_pile.append(card)
                if card.type == Type.NUMBER:
                    logger.debug(f"Start card {card.colour} {card.action_name}")
                    break

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

    def play_card(self, player_id: str, card_index: int, wild_colour: str) -> bool:
        """Plays a card from the player's hand.

        Args:
            player_id (str): The ID of the player who is playing the card.
            card_index (int): The index of the card in the player's hand.
            wild_colour (str): The colour chosen for a wild card.
        """
        player = self.players[player_id]
        card = player.hand[card_index]

        if card.is_playable(self.deck) and player_id == self.players.current_player_id:
            # Check if the card is a wild card and set the colour
            if not card.colour:
                if wild_colour in [colour.value for colour in Colour.colours(self.deck)]:
                    card.colour = Colour[wild_colour.upper()]
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

    def end_turn(self):
        """This method handles the end of a player's turn in the game.

        It checks for various conditions such as winning, updates player scores,
        and progresses the game state.
        """
        player = self.players[self.players.current_player_id]

        # Check if the current player has an empty hand/has won the game
        if len(player.hand) == 0:
            logger.info(f"Game({self.game_id}) won by {self.players.current_player_id}")

            # Update player scores based on remaining cards in hands
            for player_id, opponent in self.players.items():
                for card in opponent.hand:
                    player.score += card.score

            self.state = GameState.GAME_OVER
            return

        # Log the end of the turn and increment to the next player
        logger.debug(f"Ending {self.players.current_player_id}'s turn")
        self.players.increment_turn()

        # START OF NEXT TURN

        # Execute prerequisite_func after incrementing the turn, then reset it
        self.prerequisite_func(self)
        self.prerequisite_func = lambda self: logger.debug(
            f"Running default prerequisite_func for game {self.game_id}")

    def get_game_state(self, player_id: str) -> dict:
        """Returns the current state of the game for a given player,
        from their 'view' of the game only showing the back of other players cards

        Args:
            player_id (str): The ID of the player to get the game state for.

        Returns:
            dict: A dict containing the game state for the player that requested it,
            this data changes depending one the game state.
        """
        player = self.players[player_id]
        player_names = [player.name for player in self.players.values()]

        player_hand = [
            {
                "colour": card.colour.value if card.colour else None,
                "action": card.action_name,
                "isPlayable": card.is_playable(self.deck) and player_id == self.players.current_player_id
            }
            for card in player.hand
        ]

        # if the discard pile is empty then the discard is None
        if discard := self.deck.discard_pile[-1] if self.deck.discard_pile else None:
            discard = {
                # Wild cards with the colour None can appear
                "colour": discard.colour.value if discard.colour else None,
                "action": discard.action_name,
            }
        else:
            discard = {"colour": None, "action": None}

        return {
            "type": self.state.value,
            "name": self.name,
            "gameId": self.game_id,
            "discard": discard,
            "currentPlayerName": self.players.current_player.name,
            "playerNames": player_names,
            "wildColours": [colour.value for colour in Colour.colours(self.deck)],

            "playerId": player_id,
            "playerName": self.players[player_id].name,
            "playerHand": player_hand,
            "isHost": list(self.players.keys())[0] == player_id,
            "isTurn": player_id == self.players.current_player_id,
            "score": player.score,
        }
