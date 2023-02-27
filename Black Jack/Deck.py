from config import SUITS, RANKS
from itertools import product
from random import shuffle
from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True, frozen=True)
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

    __instance = None
    __deck_count: int
    ranks: list = RANKS
    suits: Iterable[str] = SUITS.values()
    deck: list[Card] = []

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.create_deck()
        return cls.__instance

    @classmethod
    def create_deck(cls) -> None:
        while True:
            cls.__deck_count = int(input('Deck count: '))
            if isinstance(cls.__deck_count, int):
                break
            print('Deck count be integer. Try again.')
        cls.create_shuffle_decks()

    @classmethod
    def create_shuffle_decks(cls) -> None:
        """Creates a new deck of cards."""
        for _ in range(cls.__deck_count):
            cls.deck.extend([Card(**{'rank': card[0], 'suit': card[1]})
                             for card in product(cls.ranks, cls.suits)])
        shuffle(cls.deck)

    @classmethod
    def deck_is_over(cls) -> None:
        print('Deck is over. Get new.')
        cls.create_shuffle_decks()

    @classmethod
    def get_card(cls) -> Card:
        """Returns a top card from the deck."""
        if cls.deck:
            return cls.deck.pop()
        else:
            cls.deck_is_over()
        return cls.deck.pop()

    @classmethod
    def del_deck(cls) -> None:
        cls.__instance = None
