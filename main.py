from game import Game

from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)

if __name__ == "__main__":
    game = Game()
    player_id_1 = game.add_player("Player 1")
    player_id_2 = game.add_player("Player 2")
    logger.info(game.start_game())
    game.prerequisite_func()
    logger.info(game.get_game_sate(player_id_1))
    logger.info(game.get_game_sate(player_id_2))
    game.end_turn()
