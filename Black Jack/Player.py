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

    @abstractmethod
    def _show_dealt_cards(self, dealer: 'Dealer' = None) -> bool:
        """Shows dealt cards. If return True player must be removed."""
        pass

    def print_card(self, end: str = '\n') -> None:
        print(f'{self} card:', *(card for card in self.cards), end=end)

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
            return min(sum_each_version)

    def blackjack_check(self) -> bool:
        return self.hand_value() == 21


class Dealer(Player):

    def __init__(self, name='Dealer'):
        super().__init__(name)
        self.firs_card: Card

    def get_number_of_cards(self, number_of_cards: int) -> None:
        super().get_number_of_cards(number_of_cards)
        self.firs_card: Card = self.cards[0]

    def _show_dealt_cards(self, dealer: 'Dealer' = None) -> bool:
        if not self.blackjack_check():
            print(f'{self}: {self.firs_card}, and one card is face down.')
        else:
            print('Dealer Blackjack')
            self.print_card()
        return False


class ActivePlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.money: float = 100
        self.bet: float
        self.choose: str

    def __del__(self) -> None:
        print(f"{self} leave the game")

    @abstractmethod
    def place_bet(self) -> None:
        pass

    @abstractmethod
    def get_choose(self, dealer_bj: bool) -> None:
        pass

    def hit(self, dealer: Dealer) -> bool:
        """Adds a card to the player's hand and returns
        a boolean indicating whether the player
        should be removed from the game."""

        self.get_number_of_cards(number_of_cards=1)
        print(f'{self} get {self.cards[-1]}')
        if self.hand_value() > 21:
            print(f'{self} lost. Hand value {self.hand_value()}')
            return True
        else:
            return False

    def stand(self):
        """Prints a message to indicate that the player has chosen to stand."""
        print(f'{self} stand.')

    def surrender(self) -> bool:
        """Allows the player to surrender and returns a boolean indicating
        whether the player should be removed from the game."""

        print(f'{self} got half of the bet back.')
        self.money += self.bet / 2
        print(f'{self} money: {self.money}')
        return True

    def _player_win_bj(self) -> None:
        """Allows the player to surrender and returns a boolean indicating
        whether the player should be removed from the game."""

        print(f'{self} Blackjack, win {self.bet * 3 / 2} $')
        self.money += self.bet + self.bet * 3 / 2

    def _player_win(self) -> None:
        """Prints a message to indicate the player has won and increases
        their money by the bet amount plus the bet."""

        print(f'{self}, win {self.bet * 2} $')
        self.money += self.bet + self.bet

    def _player_lost(self) -> None:
        """Prints a message to indicate the player has lost."""

        print(f'{self} lost {self.bet} $')

    def _draw(self) -> None:
        """Prints a message to indicate a draw and
        increases the player's money by the bet amount."""

        print(f'Draw. {self} gets {self.bet} $ back')
        self.money += self.bet

    def __printer(self, comparison_keyword: str, dealer: Dealer,
                  player_hand_value: int, dealer_hand_value: int) -> None:
        """Prints a message based on the comparison keyword provided."""
        self.print_card(end=' ')
        dealer.print_card()
        print(f'{self} score: {player_hand_value} vs'
              f' {dealer} score: {dealer_hand_value}')

        keywords: Dict[str, Callable] = {'win': self._player_win, 'win_bj': self._player_win_bj,
                                         'lost': self._player_lost, 'draw': self._draw}
        assert comparison_keyword in keywords.keys(), \
            f'{comparison_keyword} not in {tuple(keywords.keys())}'
        keywords.get(comparison_keyword)()
        print(f'{self} money: {self.money}')

    def __analyzer_dealer_over_21(self, player_hand_value: int, **kwargs):
        """Analyzes the game when the dealer has gone over 21"""

        kwargs = {'player_hand_value': player_hand_value, **kwargs}
        if player_hand_value == 21:
            self.__printer(comparison_keyword='win_bj', **kwargs)
        elif player_hand_value < 21:
            self.__printer(comparison_keyword='win', **kwargs)

    def __analyzer_dealer_exactly_21(self, player_hand_value: int, **kwargs):
        """Analyzes the game when the dealer has exactly 21."""

        kwargs = {'player_hand_value': player_hand_value, **kwargs}
        if player_hand_value == 21:
            self.__printer(comparison_keyword='draw', **kwargs)
        else:
            self.__printer(comparison_keyword='lost', **kwargs)

    def __analyzer_dealer_below_21(self, player_hand_value: int,
                                   dealer_hand_value: int, **kwargs):
        """Analyzes the game when the dealer has a score below 21."""

        kwargs = {'player_hand_value': player_hand_value,
                  'dealer_hand_value': dealer_hand_value, **kwargs}
        if player_hand_value == 21:
            self.__printer(comparison_keyword='win_bj', **kwargs)
        elif player_hand_value > dealer_hand_value:
            self.__printer(comparison_keyword='win', **kwargs)
        elif player_hand_value < dealer_hand_value:
            self.__printer(comparison_keyword='lost', **kwargs)
        elif player_hand_value == dealer_hand_value:
            self.__printer(comparison_keyword='draw', **kwargs)

    def analyzer(self, dealer: Dealer,
                 player_hand_value: int,
                 dealer_hand_value: int) -> None:
        """Analyzes the game and calls the appropriate
        method based on the dealer's hand value."""

        kwargs = {'dealer': dealer,
                  'player_hand_value': player_hand_value,
                  'dealer_hand_value': dealer_hand_value}

        if dealer_hand_value > 21:
            self.__analyzer_dealer_over_21(**kwargs)
        elif dealer_hand_value == 21:
            self.__analyzer_dealer_exactly_21(**kwargs)
        elif dealer_hand_value < 21:
            self.__analyzer_dealer_below_21(**kwargs)


class Human(ActivePlayer):

    def place_bet(self) -> None:
        print(f'{self} money: {self.money}')
        while True:
            try:
                self.bet = float(input(f'{self} place your bet: '))
            except ValueError:
                print('Need to enter a number. Try again.')
                continue
            if isinstance(self.bet, float):
                break
        self.money -= self.bet
        if self.money < 0:
            print('Not enough money for a bet. Try again.')
            self.money += self.bet
            self.place_bet()

    # # code for autogame
    # def place_bet(self) -> None:
    #     self.bet: float = 10.0
    #     self.money -= self.bet
    #     print(f'{self} betting {self.bet}')

    def _show_dealt_cards(self, dealer: Dealer = None) -> bool:
        self.print_card()
        two_cards_blackjack_lst = {10, 'J', 'Q', 'K', 'A'}
        if self.blackjack_check():
            print(f'{self} Blackjack!')
            # maybe the dealer has blackjack too
            if (dealer.firs_card.rank in two_cards_blackjack_lst) \
                    and not dealer.blackjack_check():
                while True:
                    choice = input(f'{self} you want to take the win 1 to 1 (yes/no): ')
                    if choice == 'yes':
                        print(f'{self} win {self.bet * 2} $')
                        self.money += self.bet * 2
                        print(f'{self} money {self.money}')
                        return True
                    elif choice == 'no':
                        print('Game continues win 3/2 bet')
                        return False
                    else:
                        print("Try again.")
            else:
                return True

        return False

    def get_choose(self, dealer_bj: bool) -> None:
        self.print_card()
        print(f'{self} hand value: {self.hand_value()}')
        if dealer_bj:
            print('Stand')
            self.choose = 'stand'
        elif self.blackjack_check():
            print(f'{self} Blackjack')
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
        self.bet: float = float(randint(1, int(self.money // 10 + 1)))
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

    def _show_dealt_cards(self, dealer: Dealer = None) -> bool:
        self.print_card()
        if self.blackjack_check() and dealer.firs_card.rank == 'A':
            print(f'{self} Blackjack!')
            print(f'{self} win {self.bet * 2} $')
            self.money += self.bet * 2
            print(f'{self} money {self.money}')
            return True
        return False
