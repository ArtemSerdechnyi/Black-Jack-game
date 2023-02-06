from config import suits, ranks
from itertools import product
from random import shuffle
from typing import Union


class Card:
    def __init__(self, card:dict):
        self.rank: str | int = card.get('rank')
        self.suit: str = card.get('suit')

    def get_card_value(self):
        if isinstance(self.rank, int):
            return int(self.rank)
        elif self.rank == 'A':
            return 1,11
        elif isinstance(self.rank, str):
            return 10


class Deck():

    def __init__(self):
        self.ranks: list = ranks
        self.suits= suits.values()
        self.deck: list[Card, ...] = []
        self.deck_count = int(input('Deck count: '))

    def create_deck(self):
        for _ in range(self.deck_count):
            self.deck.extend([Card({'rank': card[0], 'suit': card[1]}) for card in product(self.ranks, self.suits)])
        shuffle(self.deck)

    def get_card(self):
        return self.deck.pop()
