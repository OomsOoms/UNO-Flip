from .uno import Colours
from .uno import cards as uno_cards
from .uno_flip import Colours
from .uno_flip import cards as uno_flip_cards

game_modes = {
    "uno": {
        "name": "UNO",
        "cards": uno_cards,
        "wild_colours": Colours,
    },
    "uno_flip": {
        "name": "UNO Flip",
        "cards": uno_flip_cards,
        "wild_colours": Colours,
    },
}
