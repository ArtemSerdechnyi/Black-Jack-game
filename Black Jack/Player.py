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
    def __init__(self, name):
        super().__init__(name)
        self.choose: str  # look def get_chose
        self.bet: int

    def place_bet(self) -> None:
        print(f'{self} money: {self.money}')
        self.bet = int(input(f'{self} place your bet: '))  # todo Exceptions
        self.money -= self.bet
        if self.money < 0:
            print('Not enough money for a bet. Try again.')
            self.money += self.bet
            self.place_bet()

    # def get_choose(self):
    #     choose: set[str] = {'hit', 'stand', 'surrender'}
    #     while not self.choose:
    #         if len(self.cards) > 2:
    #             choose: set[str] = {'hit', 'stand'}
    #         player_choose: str = input(f'{self.name} choose actions {choose}: ')
    #         if player_choose in choose:
    #             self.choose = player_choose
    #         else:
    #             print('Invalid choice! Try again.')
    def get_choose(self):
        hand_value = self.hand_value()
        if hand_value < 16:
            self.choose = 'hit'
        elif hand_value in (16, 17) and len(self.cards) == 2:
            self.choose = 'surrender'
        else:
            self.choose = 'stand'

class Dealer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.name = 'Dealer'
        self.money = float('inf')

    def place_bet(*args, **kwargs) -> NoReturn:
        raise Exception('Dealer does not bet')

    def print_card(self) -> None:
        if len(self.cards) == 2:
            print(f'{self.cards[0]}, and one card is face down. ')
        else:
            super().print_card()


class Bot(Player):

    def __init__(self, name):
        super().__init__(name)
        self.choose: str  # look def get_chose
        self.bet: int

    def place_bet(self) -> None:
        self.bet = randint(1, 10)
        self.money -= self.bet
        print(f'{self} betting {self.bet}')

    def get_choose(self):
        hand_value = self.hand_value()
        if hand_value < 16:
            self.choose = 'hit'
        elif hand_value in (16, 17) and len(self.cards) == 2:
            self.choose = 'surrender'
        else:
            self.choose = 'stand'
