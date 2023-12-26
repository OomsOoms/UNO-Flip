from .cards import Colour, Type, Card, FlipCard
from .card_lists import build_uno_cards, build_flip_cards

game_modes = {
    "uno": {
        "name": "UNO",
        "card_builder": build_uno_cards,
    },
    "uno_flip": {
        "name": "UNO Flip",
        "card_builder": build_flip_cards,
    },
}
