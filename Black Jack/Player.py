import abc
from Deck import Deck, Card
from random import randint
from typing import Iterator
from itertools import product


class Player(abc.ABC):

    def __init__(self, name):
        self.name: str = name
        self.cards: list[Card] = []
        self.money: float = 100.0

    def __str__(self) -> str:
        return self.name

    def get_number_of_cards(self, deck_inst: Deck, number_of_cards: int) -> None:
        for _ in range(number_of_cards):
            self.cards.append(deck_inst.get_card())

    def hand_value(self) -> int:
        value_list: Iterator[tuple[float, ...]] = map(
            lambda card: card.get_card_value(), self.cards
        )
        sum_each_version = tuple(map(sum, product(*value_list)))
        filtered_version = tuple(filter(lambda value: value <= 21, sum_each_version))
        if filtered_version:
            return max(filtered_version)
        else:
            return max(sum_each_version)

    @abc.abstractmethod
    def place_bet(self):
        pass

    def blackjack_check(self) -> bool:
        if self.hand_value() == 21:
            return True
        else:
            return False


class Human(Player):

    def place_bet(self):
        self.bet = float(input(f'{self.name} place your bet: '))  # todo Exceptions
        self.money -= self.bet

    def get_human_choose(self) -> str:
        while True:
            choose: set[str] = {'hit', 'stand', 'double', 'surrender'}
            human_choose: str = input(f'{self.name} choose actions (hit, stand, double, surrender): ')
            if human_choose in choose:
                return human_choose
            else:
                print('Invalid choice! Try again.')

    def double_bet(self):
        self.money -= self.bet
        self.bet *= 2


class Dealer(Player):

    def __init__(self, name):
        super().__init__(name)
        self._money = float('inf')

    def place_bet(self):
        pass


class Bot(Player):

    def place_bet(self):
        bet = randint(1, 10)
        self.money -= bet
        print(f'{self.name} betting {bet}')
