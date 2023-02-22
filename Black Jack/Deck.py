from config import suits, ranks
from itertools import product
from random import shuffle
from dataclasses import dataclass


@dataclass(slots=True,frozen=True)
class Card:
    """A playing card."""

    rank: str | int
    suit: str

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def get_card_value(self) -> tuple[int] | tuple[int, int]:
        """Returns the value of the card, which can be a tuple of one or two integers."""
        if isinstance(self.rank, int):
            return int(self.rank),
        elif self.rank == "A":
            return 1, 11
        elif isinstance(self.rank, str):
            return 10,


class Deck:
    """A deck of playing cards."""

    __slots__ = ('ranks', 'suits', 'deck', 'deck_count')

    def __init__(self):
        self.ranks: list = ranks
        self.suits = suits.values()
        self.deck: list[Card] = []
        self.deck_count = int(input('Deck count: '))
        self.create_shuffle_deck()

    def create_shuffle_deck(self) -> None:
        """Creates a new deck of cards."""
        for _ in range(self.deck_count):
            self.deck.extend([Card(**{'rank': card[0], 'suit': card[1]}) for card in product(self.ranks, self.suits)])
        shuffle(self.deck)

    def deck_is_over(self) -> None:
        print('Deck is over. Get new.')
        self.create_shuffle_deck()

    def get_card(self) -> Card:
        """Returns a top card from the deck."""
        if self.deck:
            return self.deck.pop()
        else:
            self.deck_is_over()
        return self.deck.pop()
