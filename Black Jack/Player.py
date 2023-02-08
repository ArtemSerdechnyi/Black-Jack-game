from abc import ABC, abstractmethod
from Deck import Deck, Card
from random import randint
from typing import Iterator, NoReturn
from itertools import product


class Player(ABC):

    def __init__(self, name):
        self.name: str = name
        self.cards: list[Card] = []
        self.money: float = 100.0

    def __str__(self) -> str:
        return self.name

    @abstractmethod
    def place_bet(self):
        pass

    @abstractmethod
    def print_card(self) -> None:
        print(f'{self} card: ', end='')
        print(*(card for card in self.cards))

    def get_number_of_cards(self,
                            deck_inst: Deck,
                            number_of_cards: int) -> None:
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

    def blackjack_check(self) -> bool:
        if self.hand_value() == 21:
            return True
        else:
            return False


class Human(Player):

    def place_bet(self) -> None:
        self.bet = float(input(f'{self.name} place your bet: '))  # todo Exceptions
        self.money -= self.bet
        if self.money < 0:
            print('Not enough money for a bet. Try again.')
            self.money += self.bet
            self.place_bet()

    def print_card(self) -> None:
        super().print_card()

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
        self.name = 'Dealer'
        self.money = float('inf')

    def place_bet(self) -> NoReturn:
        raise Exception('Dealer does not bet')

    def print_card(self) -> None:
        print('Dealer card: ', end='')
        for ind, card in enumerate(self.cards):
            if not ind:
                if card.rank == 'A' or card.rank == '10':
                    print(card, end=', ')
                    continue
                print(f'{card}, and one card is face down. ')
                break
            elif self.blackjack_check():
                print(card, end=' BlACK JACK!')
            else:
                print('and one card is face down.')


class Bot(Player):

    def place_bet(self) -> None:
        bet = randint(1, 10)
        self.money -= bet
        print(f'{self.name} betting {bet}')

    def print_card(self) -> None:
        super().print_card()
