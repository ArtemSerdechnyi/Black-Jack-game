from abc import ABC, abstractmethod
from Deck import Deck, Card
from random import randint
from typing import Iterator, Dict, Callable
from itertools import product


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


class Dealer(Player):

    def __init__(self, name='Dealer'):
        super().__init__(name)
        self.firs_card: Card

    def get_number_of_cards(self, number_of_cards: int) -> None:
        super().get_number_of_cards(number_of_cards)
        self.firs_card: Card = self.cards[0]


class ActivePlayer(Player):
    money: float = 100
    bet: int
    choose: str

    def __del__(self):
        print(f"{self} leave the game")

    @abstractmethod
    def place_bet(self) -> None:
        pass

    @abstractmethod
    def get_choose(self, dealer_bj: bool):
        pass

    def __printer(self, comparison_keyword: str, dealer: Dealer,
                  player_hand_value: int, dealer_hand_value: int) -> None:

        self.print_card()
        dealer.print_card()
        print(f'{self} score: {player_hand_value} vs'
              f' {dealer} score: {dealer_hand_value}')

        def player_win_bj() -> None:
            print(f'{self} Blackjack, win {self.bet * 3 / 2} $')
            self.money += self.bet + self.bet * 3 / 2

        def player_win() -> None:
            print(f'{self}, win {self.bet * 2} $')
            self.money += self.bet + self.bet

        def player_lost() -> None:
            print(f'{self} lost {self.bet} $')

        def draw() -> None:
            print(f'Draw. {self} gets {self.bet} $ back')
            self.money += self.bet

        keywords: Dict[str, Callable] = {'win': player_win, 'win_bj': player_win_bj,
                                         'lost': player_lost, 'draw': draw}
        assert comparison_keyword in keywords.keys(), \
            f'{comparison_keyword} not in {tuple(keywords.keys())}'
        keywords.get(comparison_keyword)()
        print(f'{self} money: {self.money}')

    def analyzer(self, dealer: Dealer,
                 player_hand_value: int,
                 dealer_hand_value: int) -> None:
        kwargs = {'dealer': dealer,
                  'player_hand_value': player_hand_value,
                  'dealer_hand_value': dealer_hand_value}
        if dealer_hand_value > 21:
            if player_hand_value == 21:
                self.__printer(comparison_keyword='win_bj', **kwargs)
            elif player_hand_value < 21:
                self.__printer(comparison_keyword='win', **kwargs)
        elif dealer_hand_value == 21:
            if player_hand_value == 21:
                self.__printer(comparison_keyword='draw', **kwargs)
            else:
                self.__printer(comparison_keyword='lost', **kwargs)
        elif dealer_hand_value < 21:
            if player_hand_value == 21:
                self.__printer(comparison_keyword='win_bj', **kwargs)
            elif player_hand_value > dealer_hand_value:
                self.__printer(comparison_keyword='win', **kwargs)
            elif player_hand_value < dealer_hand_value:
                self.__printer(comparison_keyword='lost', **kwargs)
            elif player_hand_value == dealer_hand_value:
                self.__printer(comparison_keyword='draw', **kwargs)


class Human(ActivePlayer):

    def place_bet(self) -> None:
        print(f'{self} money: {self.money}')
        while True:
            self.bet = int(input(f'{self} place your bet: '))
            if isinstance(self.bet, int):
                break
        self.money -= self.bet
        if self.money < 0:
            print('Not enough money for a bet. Try again.')
            self.money += self.bet
            self.place_bet()

    # # code for autogame
    # def place_bet(self) -> None:
    #     self.bet = 10
    #     self.money -= self.bet
    #     print(f'{self} betting {self.bet}')

    def get_choose(self, dealer_bj: bool):
        self.print_card()
        print(f'{self} hand value: {self.hand_value()}')
        if dealer_bj or self.blackjack_check():
            print('Stand')
            self.choose = 'stand'
        else:
            choose: set[str] = {'hit', 'stand', 'surrender'}
            while True:
                if len(self.cards) > 2:
                    choose: set[str] = {'hit', 'stand'}
                player_choose: str = input(f'{self.name} choose actions {choose}: ')
                if player_choose in choose:
                    self.choose = player_choose
                    break
                else:
                    print('Invalid choice! Try again.')

    # # for autogame
    # def get_choose(self, dealer_bj: bool):
    #     hand_value = self.hand_value()
    #     if dealer_bj:
    #         print('Stand')
    #         self.choose = 'stand'
    #     else:
    #         if hand_value < 16:
    #             self.choose = 'hit'
    #         elif hand_value in (16, 17) and len(self.cards) == 2:
    #             self.choose = 'surrender'
    #         else:
    #             self.choose = 'stand'


class Bot(ActivePlayer):

    def place_bet(self) -> None:
        self.bet = randint(1, 10)
        self.money -= self.bet
        print(f'{self} betting {self.bet}')

    def get_choose(self, dealer_bj: bool):
        hand_value: int = self.hand_value()
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
