from game import Game

from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)

if __name__ == "__main__":
    game = Game()
    game.add_player("Player 1")
    game.generate_start_card()
    game.get_game_sate()
    game.end_turn()

