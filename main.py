from game import Game

from utils.custom_logger import CustomLogger

logger = CustomLogger(__name__)

if __name__ == "__main__":
    game = Game()
    # Store in session data 
    player_id_1 = game.add_player("Player 1")
    player_id_2 = game.add_player("Player 2")

    game.start_game()

    while True:
        game.prerequisite_func()
        
        logger.info(f"Current player: {game.current_player_id}, Current player index: {game.current_player_index}")
        # Simulating the website where this all happens simultaneously
        discard, player_1_object, player_1_hand = game.get_game_sate(player_id_1)
        discard, player_2_object, player_2_hand = game.get_game_sate(player_id_2)

        # Simulating a website where the card would pass though the object
        true_indexes = [i for i, (key, value) in enumerate(player_1_hand.items()) if value]
        logger.info(f"Discard: {discard}, Player 1 playable indexes: {true_indexes}, Number of cards: {len(player_1_hand)}")
        card_object_list = list(player_1_hand.keys())
        card = card_object_list[int(input("Select a index: "))]
        game.select_card(player_id_1, card)

        # Simulating a website where the card would pass though the object
        true_indexes = [i for i, (key, value) in enumerate(player_2_hand.items()) if value]
        logger.info(f"Discard: {discard}, Player 2 playable indexes: {true_indexes}, Number of cards: {len(player_2_hand)}")
        card_object_list = list(player_2_hand.keys())
        card = card_object_list[int(input("Select a index: "))]
        game.select_card(player_id_2, card)
