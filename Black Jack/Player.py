import abc
from Deck import Deck, Card
from random import randint
from typing import Type, Iterator
from itertools import product, tee


class Player(abc.ABC):

    def __init__(self, name):
        self.name: str = name
        self.cards: list[Card] = []
        self.money: int = 100

    def get_number_of_cards(self, deck_inst: Deck, number_of_cards: int) -> None:
        for _ in range(number_of_cards):
            self.cards.append(deck_inst.get_card())

    def hand_value(self) -> int:
        value_list: Iterator[tuple] = map(
            lambda card: card.get_card_value()
            if isinstance(card.get_card_value(), tuple)
            else (card.get_card_value(),), self.cards
        )
        sum_each_version = tuple(map(sum, product(*value_list)))
        filtered_version = tuple(filter(lambda value: value <= 21, sum_each_version))
        if filtered_version:
            return max(filtered_version)
        else:
            return max(sum_each_version)


class Human(Player):

    def place_bet(self):
        bet = int(input(f'{self.name} place your bet: '))
        self.money -= bet


class Dealer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.money = float('inf')


class Bot(Player):

    def place_bet(self):
        bet = randint(1, 10)
        self.money -= bet
        print(f'{self.name} betting {bet}')
