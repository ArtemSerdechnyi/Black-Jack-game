from abc import ABC, abstractmethod
from Deck import Deck, Card
from random import randint
from typing import Iterator, NoReturn
from itertools import product


class ActivePlayer(ABC):
    money: int = 100
    bet: int

    def __del__(self):
        print(f"{self} leave the game")

    @abstractmethod
    def place_bet(self) -> None:
        pass
        # # print(f'{self} money: {self.money}')
        # # self.bet = int(input(f'{self} place your bet: '))  # todo Exceptions
        # # self.money -= self.bet
        # # if self.money < 0:
        # #     print('Not enough money for a bet. Try again.')
        # #     self.money += self.bet
        # #     self.place_bet()
        #
        # self.bet = 10
        # self.money -= self.bet
        # print(f'{self} betting {self.bet}')


class Player(ABC):

    def __init__(self, name):
        self.name: str = name
        self.cards: list[Card] = []

    def __str__(self) -> str:
        return self.name

    def print_card(self) -> None:
        print(f'{self} card:', *(card for card in self.cards))

    def get_number_of_cards(self, number_of_cards: int) -> None:
        self.cards.extend([Deck.get_card() for _ in range(number_of_cards)])

    def hand_value(self) -> int:
        value_list: Iterator[tuple[int, ...]] = map(
            lambda card: card.get_card_value(), self.cards)
        sum_each_version = tuple(map(sum, product(*value_list)))
        filtered_version = tuple(filter(lambda value: value <= 21, sum_each_version))
        if filtered_version:
            return max(filtered_version)
        else:
            return max(sum_each_version)

    def blackjack_check(self) -> bool:
        return self.hand_value() == 21


class Human(Player, ActivePlayer):
    def __init__(self, name):
        super().__init__(name)
        self.choose: str  # look def get_chose
        self.bet: int

    def place_bet(self) -> None:
        # print(f'{self} money: {self.money}')
        # self.bet = int(input(f'{self} place your bet: '))  # todo Exceptions
        # self.money -= self.bet
        # if self.money < 0:
        #     print('Not enough money for a bet. Try again.')
        #     self.money += self.bet
        #     self.place_bet()
        self.bet = 10
        self.money -= self.bet
        print(f'{self} betting {self.bet}')

    # def get_choose(self, dealer_bj: bool):
    # todo dlr bj

    #     choose: set[str] = {'hit', 'stand', 'surrender'}
    #     while not self.choose:
    #         if len(self.cards) > 2:
    #             choose: set[str] = {'hit', 'stand'}
    #         player_choose: str = input(f'{self.name} choose actions {choose}: ')
    #         if player_choose in choose:
    #             self.choose = player_choose
    #         else:
    #             print('Invalid choice! Try again.')
    def get_choose(self, dealer_bj: bool):
        hand_value = self.hand_value()
        if dealer_bj:
            print('Stand')
            self.choose = 'stand'
        else:
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
        # del self.money
        self.firs_card: Card

    def place_bet(*args, **kwargs) -> NoReturn:
        raise Exception('Dealer does not bet')

    def get_number_of_cards(self, number_of_cards: int) -> None:
        super().get_number_of_cards(number_of_cards)
        self.firs_card: Card = self.cards[0]


class Bot(Player, ActivePlayer):

    def __init__(self, name):
        super().__init__(name)
        self.choose: str  # look def get_chose
        self.bet: int

    def place_bet(self) -> None:
        self.bet = randint(1, 10)
        self.money -= self.bet
        print(f'{self} betting {self.bet}')

    def get_choose(self, dealer_bj: bool):
        hand_value = self.hand_value()
        if dealer_bj:
            print('Stand')
            self.choose = 'stand'
        else:
            if hand_value < 16:
                self.choose = 'hit'
            elif hand_value in (16, 17) and len(self.cards) == 2:
                self.choose = 'surrender'
            else:
                self.choose = 'stand'
