from config import suits, ranks
from itertools import product
from random import shuffle


class Card:
    __slots__ = ('rank', 'suit')

    def __init__(self, card: dict):
        self.rank: str | int = card.get('rank')
        self.suit: str = card.get('suit')

    def __str__(self) -> str:
        return f'{self.rank}{self.suit}'

    def get_card_value(self) -> tuple[float, ...]:
        if isinstance(self.rank, int):
            return float(self.rank),
        elif self.rank == 'A':
            return 1.0, 11.0
        elif isinstance(self.rank, str):
            return 10.0,


class Deck:
    __slots__ = ('ranks', 'suits', 'deck', 'deck_count')

    def __init__(self):
        self.ranks: list = ranks
        self.suits = suits.values()
        self.deck: list[Card] = []
        self.deck_count = int(input('Deck count: '))

    def create_deck(self):
        for _ in range(self.deck_count):
            self.deck.extend([Card({'rank': card[0], 'suit': card[1]}) for card in product(self.ranks, self.suits)])
        shuffle(self.deck)

    def get_card(self):
        if self.deck:
            return self.deck.pop()
        else:
            print('Deck is over. Get new.')
            self.create_deck()
            return self.deck.pop()
