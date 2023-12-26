from .cards import Card, FlipCard, Colour

def build_uno_cards(deck) -> list[Card]:

    # Numbers: 0-9 (2 of each colour) = 80 total
    cards = [Card.number(col, num) for col in Colour.colours(deck) for num in range(1, 10) for _ in range(2)] 
    cards += [Card.number(col, 0) for col in Colour.colours(deck)]
    # Skip: (2 of each colour) = 8 total
    cards += [Card.skip(col) for col in Colour.colours(deck) for _ in range(2)]
    # Draw Two: (2 of each colour) = 8 total
    cards += [Card.draw(col, 2) for col in Colour.colours(deck) for _ in range(2)]
    # Reverse: (2 of each colour) = 8 total
    cards += [Card.reverse(col) for col in Colour.colours(deck) for _ in range(2)]
    # Wild: 4 total
    cards += [Card.wild() for _ in range(4)]
    # Wild Draw Four: 4 total
    cards += [Card.wild_draw(4) for _ in range(4)]

    return cards

def build_flip_cards(deck) -> list[Card]:
    cards = [
        FlipCard(Card.number(Colour.YELLOW, 1), Card.skip_everyone(Colour.PINK)),
        FlipCard(Card.number(Colour.YELLOW, 1), Card.wild()),
        FlipCard(Card.number(Colour.YELLOW, 2), Card.number(Colour.TURQUOISE, 1)),
        FlipCard(Card.number(Colour.YELLOW, 2), Card.number(Colour.TURQUOISE, 8)),
        FlipCard(Card.number(Colour.YELLOW, 3), Card.number(Colour.PURPLE, 1)),
        FlipCard(Card.number(Colour.YELLOW, 3), Card.draw(Colour.PINK, 5)),
        FlipCard(Card.number(Colour.YELLOW, 4), Card.draw(Colour.PINK, 5)),
        FlipCard(Card.number(Colour.YELLOW, 4), Card.flip(Colour.PURPLE)),
        FlipCard(Card.number(Colour.YELLOW, 5), Card.number(Colour.TURQUOISE, 8)),
        FlipCard(Card.number(Colour.YELLOW, 5), Card.number(Colour.PURPLE, 9)),
        FlipCard(Card.number(Colour.YELLOW, 6), Card.skip_everyone(Colour.ORANGE)),
        FlipCard(Card.number(Colour.YELLOW, 6), Card.wild_draw_colour()),
        FlipCard(Card.number(Colour.YELLOW, 7), Card.number(Colour.ORANGE, 2)),
        FlipCard(Card.number(Colour.YELLOW, 7), Card.number(Colour.PURPLE, 6)),
        FlipCard(Card.number(Colour.YELLOW, 8), Card.number(Colour.PINK, 1)),
        FlipCard(Card.number(Colour.YELLOW, 8), Card.number(Colour.ORANGE, 2)),
        FlipCard(Card.number(Colour.YELLOW, 9), Card.number(Colour.PURPLE, 4)),
        FlipCard(Card.number(Colour.YELLOW, 9), Card.number(Colour.TURQUOISE, 5)),

        FlipCard(Card.number(Colour.RED, 1), Card.number(Colour.PURPLE, 2)),
        FlipCard(Card.number(Colour.RED, 1), Card.number(Colour.PINK, 3)),
        FlipCard(Card.number(Colour.RED, 2), Card.draw(Colour.PURPLE, 5)),
        FlipCard(Card.number(Colour.RED, 2), Card.reverse(Colour.ORANGE)),
        FlipCard(Card.number(Colour.RED, 3), Card.number(Colour.PINK, 7)),
        FlipCard(Card.number(Colour.RED, 3), Card.wild_draw_colour()),
        FlipCard(Card.number(Colour.RED, 4), Card.draw(Colour.PURPLE, 5)),
        FlipCard(Card.number(Colour.RED, 4), Card.flip(Colour.ORANGE)),
        FlipCard(Card.number(Colour.RED, 5), Card.number(Colour.PINK, 2)),
        FlipCard(Card.number(Colour.RED, 5), Card.number(Colour.TURQUOISE, 5)),
        FlipCard(Card.number(Colour.RED, 6), Card.number(Colour.ORANGE, 9)),
        FlipCard(Card.number(Colour.RED, 6), Card.skip_everyone(Colour.PINK)),
        FlipCard(Card.number(Colour.RED, 7), Card.number(Colour.ORANGE, 1)),
        FlipCard(Card.number(Colour.RED, 7), Card.number(Colour.PURPLE, 5)),
        FlipCard(Card.number(Colour.RED, 8), Card.number(Colour.TURQUOISE, 7)),
        FlipCard(Card.number(Colour.RED, 8), Card.reverse(Colour.PURPLE)),
        FlipCard(Card.number(Colour.RED, 9), Card.number(Colour.PURPLE, 5)),
        FlipCard(Card.number(Colour.RED, 9), Card.reverse(Colour.TURQUOISE)),

        FlipCard(Card.number(Colour.BLUE, 1), Card.skip_everyone(Colour.PURPLE)),
        FlipCard(Card.number(Colour.BLUE, 1), Card.skip_everyone(Colour.PURPLE)),
        FlipCard(Card.number(Colour.BLUE, 2), Card.number(Colour.ORANGE, 8)),
        FlipCard(Card.number(Colour.BLUE, 2), Card.number(Colour.PINK, 6)),
        FlipCard(Card.number(Colour.BLUE, 3), Card.number(Colour.TURQUOISE, 2)),
        FlipCard(Card.number(Colour.BLUE, 3), Card.number(Colour.PURPLE, 8)),
        FlipCard(Card.number(Colour.BLUE, 4), Card.draw(Colour.TURQUOISE, 5)),
        FlipCard(Card.number(Colour.BLUE, 4), Card.number(Colour.PURPLE, 1)),
        FlipCard(Card.number(Colour.BLUE, 5), Card.number(Colour.PINK, 9)),
        FlipCard(Card.number(Colour.BLUE, 5), Card.reverse(Colour.ORANGE)),
        FlipCard(Card.number(Colour.BLUE, 6), Card.reverse(Colour.PURPLE)),
        FlipCard(Card.number(Colour.BLUE, 6), Card.skip_everyone(Colour.TURQUOISE)),
        FlipCard(Card.number(Colour.BLUE, 7), Card.number(Colour.ORANGE, 3)),
        FlipCard(Card.number(Colour.BLUE, 7), Card.skip_everyone(Colour.ORANGE)),
        FlipCard(Card.number(Colour.BLUE, 8), Card.number(Colour.TURQUOISE, 4)),
        FlipCard(Card.number(Colour.BLUE, 8), Card.reverse(Colour.TURQUOISE)),
        FlipCard(Card.number(Colour.BLUE, 9), Card.number(Colour.ORANGE, 5)),
        FlipCard(Card.number(Colour.BLUE, 9), Card.flip(Colour.PURPLE)),

        FlipCard(Card.number(Colour.GREEN, 1), Card.number(Colour.ORANGE, 5)),
        FlipCard(Card.number(Colour.GREEN, 1), Card.flip(Colour.ORANGE)),
        FlipCard(Card.number(Colour.GREEN, 2), Card.skip_everyone(Colour.TURQUOISE)),
        FlipCard(Card.number(Colour.GREEN, 2), Card.draw(Colour.TURQUOISE, 5)),
        FlipCard(Card.number(Colour.GREEN, 3), Card.number(Colour.PURPLE, 2)),
        FlipCard(Card.number(Colour.GREEN, 3), Card.flip(Colour.PINK)),
        FlipCard(Card.number(Colour.GREEN, 4), Card.number(Colour.TURQUOISE, 9)),
        FlipCard(Card.number(Colour.GREEN, 4), Card.number(Colour.PINK, 8)),
        FlipCard(Card.number(Colour.GREEN, 5), Card.number(Colour.TURQUOISE, 4)),
        FlipCard(Card.number(Colour.GREEN, 5), Card.number(Colour.ORANGE, 7)),
        FlipCard(Card.number(Colour.GREEN, 6), Card.number(Colour.PINK, 5)),
        FlipCard(Card.number(Colour.GREEN, 6), Card.wild_draw_colour()),
        FlipCard(Card.number(Colour.GREEN, 7), Card.number(Colour.TURQUOISE, 2)),
        FlipCard(Card.number(Colour.GREEN, 7), Card.number(Colour.ORANGE, 6)),
        FlipCard(Card.number(Colour.GREEN, 8), Card.number(Colour.TURQUOISE, 9)),
        FlipCard(Card.number(Colour.GREEN, 8), Card.reverse(Colour.PINK)),
        FlipCard(Card.number(Colour.GREEN, 9), Card.draw(Colour.PINK, 5)),
        FlipCard(Card.number(Colour.GREEN, 9), Card.reverse(Colour.ORANGE)),

        FlipCard(Card.draw(Colour.YELLOW, 1, score=10), Card.number(Colour.PINK, 1)),
        FlipCard(Card.draw(Colour.YELLOW, 1, score=10), Card.number(Colour.PURPLE, 8)),
        FlipCard(Card.draw(Colour.RED, 1, score=10), Card.number(Colour.PINK, 3)),
        FlipCard(Card.draw(Colour.RED, 1, score=10), Card.number(Colour.PINK, 4)),
        FlipCard(Card.draw(Colour.BLUE, 1, score=10), Card.number(Colour.PINK, 6)),
        FlipCard(Card.draw(Colour.BLUE, 1, score=10), Card.number(Colour.TURQUOISE, 6)),
        FlipCard(Card.draw(Colour.GREEN, 1, score=10), Card.number(Colour.ORANGE, 6)),
        FlipCard(Card.draw(Colour.GREEN, 1, score=10), Card.number(Colour.TURQUOISE, 6)),

        FlipCard(Card.reverse(Colour.YELLOW), Card.flip(Colour.TURQUOISE)),
        FlipCard(Card.reverse(Colour.YELLOW), Card.wild()),
        FlipCard(Card.reverse(Colour.RED), Card.number(Colour.PURPLE, 3)),
        FlipCard(Card.reverse(Colour.RED), Card.number(Colour.TURQUOISE, 7)),
        FlipCard(Card.reverse(Colour.BLUE), Card.number(Colour.ORANGE, 4)),
        FlipCard(Card.reverse(Colour.BLUE), Card.wild()),
        FlipCard(Card.reverse(Colour.GREEN), Card.number(Colour.ORANGE, 1)),
        FlipCard(Card.reverse(Colour.GREEN), Card.number(Colour.PINK, 7)),

        FlipCard(Card.flip(Colour.YELLOW), Card.number(Colour.PINK, 4)),
        FlipCard(Card.flip(Colour.YELLOW), Card.number(Colour.ORANGE, 8)),
        FlipCard(Card.flip(Colour.RED), Card.number(Colour.PURPLE, 3)),
        FlipCard(Card.flip(Colour.RED), Card.number(Colour.PINK, 8)),
        FlipCard(Card.flip(Colour.BLUE), Card.number(Colour.PURPLE, 6)),
        FlipCard(Card.flip(Colour.BLUE), Card.number(Colour.PURPLE, 7)),
        FlipCard(Card.flip(Colour.GREEN), Card.number(Colour.TURQUOISE, 3)),
        FlipCard(Card.flip(Colour.GREEN), Card.wild_draw_colour()),

        FlipCard(Card.skip(Colour.YELLOW), Card.number(Colour.ORANGE, 3)),
        FlipCard(Card.skip(Colour.YELLOW), Card.flip(Colour.TURQUOISE)),
        FlipCard(Card.skip(Colour.RED), Card.draw(Colour.ORANGE, 5)),
        FlipCard(Card.skip(Colour.RED), Card.wild()),
        FlipCard(Card.skip(Colour.BLUE), Card.number(Colour.TURQUOISE, 1)),
        FlipCard(Card.skip(Colour.BLUE), Card.number(Colour.PINK, 9)),
        FlipCard(Card.skip(Colour.GREEN), Card.number(Colour.PURPLE, 4)),
        FlipCard(Card.skip(Colour.GREEN), Card.number(Colour.ORANGE, 9)),

        FlipCard(Card.wild(), Card.number(Colour.TURQUOISE, 3)),
        FlipCard(Card.wild(), Card.number(Colour.PINK, 5)),
        FlipCard(Card.wild(), Card.number(Colour.PURPLE, 7)),
        FlipCard(Card.wild(), Card.flip(Colour.PINK)),

        FlipCard(Card.wild_draw(2), Card.number(Colour.PINK, 2)),
        FlipCard(Card.wild_draw(2), Card.number(Colour.ORANGE, 4)),
        FlipCard(Card.wild_draw(2), Card.number(Colour.ORANGE, 7)),
        FlipCard(Card.wild_draw(2), Card.number(Colour.PURPLE, 9)),
    ]

    for card in cards:
        card.deck = deck

    return cards
