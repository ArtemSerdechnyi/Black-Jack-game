
from Player import Bot, Human, Dealer, Player
from Deck import Deck
from typing import Callable, Union


class Game:

    def __init__(self):
        self.human_plrs: list[Human] = []
        self.bot_plrs: list[Bot] = []
        self.dealer: Dealer = Dealer(name='Dealer')
        self.deck_inst: Deck

    class __Round:

        def __init__(self, human_plrs: list[Human],
                     bot_plrs: list[Bot],
                     dealer: Dealer,
                     deck_inst: Deck):
            self.human_plrs: list[Human] = human_plrs
            self.bot_plrs: list[Bot] = bot_plrs
            self.dealer: Dealer = dealer
            self.deck_inst: Deck = deck_inst
            self.game_round()

        def remove_player(self: Union['__Round', 'Game'], player: Player):
            player.cards.clear()
            match player:
                case Dealer() as dealer:
                    [self.dealer].remove(dealer)
                case Human() as human:
                    self.human_plrs.remove(human)
                case Bot() as bot:
                    self.bot_plrs.remove(bot)

        def hand_analysis(self, player: Human | Bot):
            dealer = self.dealer
            bet = player.bet
            player_hand_value = player.hand_value()  # player_hand_value <= 21
            dealer_hand_value = dealer.hand_value()
            assert player_hand_value <= 21, 'in def hand_analysis player_hand_value must be <=21'

            def player_win_bj():
                print(f'{player} Blackjack, win {bet * 3 / 2} $')
                player.money += bet + bet * 3 / 2

            def player_win():
                print(f'{player}, win {bet * 2} $')
                player.money += bet + bet

            def player_lost():
                print(f'{player} lost {bet} $')

            def draw():
                print(f'Draw. {player} gets {bet} $ back')
                player.money += bet

            player.print_card()
            dealer.print_card()
            print(f'{player} score: {player_hand_value} vs'
                  f' {dealer} score: {dealer_hand_value}')
            if dealer_hand_value > 21:
                if player_hand_value == 21:
                    player_win_bj()
                elif player_hand_value < 21:
                    player_win()
            elif dealer_hand_value == 21:
                if player_hand_value == 21:
                    draw()
                else:
                    player_lost()
            elif dealer_hand_value < 21:
                if player_hand_value == 21:
                    player_win_bj()
                elif player_hand_value > dealer_hand_value:
                    player_win()
                elif player_hand_value < dealer_hand_value:
                    player_lost()
                elif player_hand_value == dealer_hand_value:
                    draw()

            print(f'{player} money: {player.money}')
            self.remove_player(player=player)

        @staticmethod
        def move_dealer(dealer: Dealer):
            if dealer.hand_value() < 16:
                print("Dealer get the cards: ")
                while dealer.hand_value() < 17:
                    dealer.get_number_of_cards(number_of_cards=1)
                    print(f'Dealer get {dealer.cards[-1]}')
                dealer.print_card()

        def move_activation(self, player: Human | Bot):
            match player.choose:
                case 'hit':
                    player.get_number_of_cards(number_of_cards=1)
                    if player.hand_value() > 21:
                        print(f'{player} lost. Hand value {player.hand_value()}', *player.cards)
                        self.remove_player(player=player)
                    else:
                        player.get_choose(dealer_bj=self.dealer.blackjack_check())
                        self.move_activation(player=player)
                case 'stand':
                    print(f'{player} stand.')
                case 'surrender':
                    print(f'{player} got half of the bet back.')
                    player.money += player.bet / 2
                    print(f'{player} money: {player.money}')
                    self.remove_player(player=player)

        def choose_move_player(self, player: Human | Bot):
            hand_value: int = player.hand_value()
            if hand_value <= 21:
                player.get_choose(dealer_bj=self.dealer.blackjack_check())
            elif hand_value > 21:
                print(f'{player} lose this round: -{player.bet}$')
                self.remove_player(player=player)

        def print_card_player(self, player: Player):
            match player:
                case Dealer() as dealer:
                    if not dealer.blackjack_check():
                        print(f'{dealer}: {dealer.firs_card}, and one card is face down.')
                    else:
                        print('Dealer Blackjack')
                        dealer.print_card()
                case Human() as human:
                    human.print_card()
                    if human.blackjack_check() and self.dealer.firs_card.rank == 'A':
                        print(f'{human} Blackjack!')
                        while True:
                            choice = input(f'{human} you want to take the win 1 to 1 (yes/no): ')
                            if choice == 'yes':
                                print(f'{human} win {human.bet * 2} $')
                                human.money += human.bet * 2
                                print(f'{human} money {human.money}')
                                self.remove_player(player=human)
                                break
                            elif choice == 'no':
                                print('Game continues win 3/2 bet')
                                break
                            else:
                                print("Try again.")
                case Bot() as bot:
                    bot.print_card()

        @staticmethod
        def apply_method(players: list[Human | Bot], method: Callable, **kwargs):
            for player in players.copy():
                method(player, **kwargs)

        def game_round(self):
            humans: list[Human] = self.human_plrs
            bots: list[Bot] = self.bot_plrs
            dealer: Dealer = self.dealer

            self.apply_method(players=humans, method=Human.place_bet)
            self.apply_method(players=bots, method=Bot.place_bet)

            self.apply_method(players=humans, method=Human.get_number_of_cards,
                              number_of_cards=2)
            self.apply_method(players=bots, method=Bot.get_number_of_cards,
                              number_of_cards=2)
            dealer.get_number_of_cards(number_of_cards=2)

            self.print_card_player(player=dealer)
            self.apply_method(players=humans, method=self.print_card_player)
            self.apply_method(players=bots, method=self.print_card_player)

            self.apply_method(players=humans, method=self.choose_move_player)
            self.apply_method(players=bots, method=self.choose_move_player)

            self.apply_method(players=bots, method=self.move_activation)
            self.apply_method(players=humans, method=self.move_activation)
            self.move_dealer(dealer=dealer)

            self.apply_method(players=humans, method=self.hand_analysis)
            self.apply_method(players=bots, method=self.hand_analysis)

    @staticmethod
    def endgame():
        print('Game the end.')

    def poor_remove(self, player: Human | Bot):
        if player.money < 1:
            print(f'{player} out of money')
            self.__Round.remove_player(self=self, player=player)  # attention fake self!

    def gnrt_deck(self):
        # while True:
        #     deck_count = int(input('Deck count: '))
        #     if isinstance(deck_count, int):
        #         break
        #     print('Deck count be integer. Try again.')
        self.deck_inst = Deck()

    def gnrt_player(self, player_type):
        match player_type:
            case 'Human':
                human_count = int(input('Write, human players count: '))
                # todo Exceptions
                for num in range(1, human_count + 1):
                    # name = input(f'Write name player{num}: ') # do this when finished
                    name = f'test{num}'  # del this when finished
                    # todo Exceptions
                    h = Human(name=name)
                    self.human_plrs.append(h)
            case 'Bot':
                bot_count = int(input('Write, bot players count: '))
                # todo Exceptions
                for num in range(1, bot_count + 1):
                    name = f'Bot{num}'
                    b = Bot(name=name)
                    self.bot_plrs.append(b)

    def start_game(self):
        self.gnrt_player(player_type='Human')
        self.gnrt_player(player_type='Bot')
        self.gnrt_deck()

        while self.human_plrs or self.bot_plrs:
            self.__Round(human_plrs=self.human_plrs.copy(),
                         bot_plrs=self.bot_plrs.copy(),
                         dealer=self.dealer,
                         deck_inst=self.deck_inst)
            self.__Round.apply_method(players=self.human_plrs, method=self.poor_remove)
            self.__Round.apply_method(players=self.bot_plrs, method=self.poor_remove)
            self.__Round.remove_player(self=self, player=self.dealer)  # attention fake self!

        self.endgame()
