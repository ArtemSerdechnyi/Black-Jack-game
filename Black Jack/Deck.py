
from config import suits, ranks
from itertools import product
from random import shuffle
from dataclasses import dataclass


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
    ranks: list = ranks
    suits = suits.values()
    deck: list[Card] = []

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            print('NEW DECK')
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def __init__(cls, deck_count):
        cls.__deck_count = deck_count
        cls.create_shuffle_deck()


    @classmethod
    def create_shuffle_deck(cls) -> None:
        """Creates a new deck of cards."""
        for _ in range(cls.__deck_count):
            cls.deck.extend([Card(**{'rank': card[0], 'suit': card[1]})
                             for card in product(cls.ranks, cls.suits)])
        shuffle(cls.deck)

    @classmethod
    def deck_is_over(cls) -> None:
        print('Deck is over. Get new.')
        cls.create_shuffle_deck()

    @classmethod
    def get_card(cls) -> Card:
        """Returns a top card from the deck."""
        if cls.deck:
            return cls.deck.pop()
        else:
            cls.deck_is_over()
        return cls.deck.pop()

