from Player import Bot, Human, Dealer, Player, ActivePlayer
from Deck import Deck
from typing import Callable, Union


class Game:

    def __init__(self):
        self.human_plrs: list[Human] = []
        self.bot_plrs: list[Bot] = []
        self.dealer: Dealer = Dealer()
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

        @staticmethod
        def round_end():
            print('Round over. -------------------------------------')

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
            """Analyzes a player's hand and determines if they won or lost."""
            dealer: Dealer = self.dealer
            player_hand_value: int = player.hand_value()  # player_hand_value must be <= 21
            assert player_hand_value <= 21, 'in def hand_analysis player_hand_value must be <=21'
            dealer_hand_value: int = dealer.hand_value()
            player.analyzer(dealer=self.dealer,
                            player_hand_value=player_hand_value,
                            dealer_hand_value=dealer_hand_value)

        @staticmethod
        def move_dealer(dealer: Dealer) -> None:
            if dealer.hand_value() < 16:
                print("Dealer get the cards: ")
                while dealer.hand_value() < 17:
                    dealer.get_number_of_cards(number_of_cards=1)
                    print(f'Dealer get {dealer.cards[-1]}')
                dealer.print_card()

        def move_activation(self, player: ActivePlayer) -> None:
            match player.choose:
                case 'hit':
                    if player.hit(dealer=self.dealer):
                        self.remove_player(player=player)
                    else:
                        player.get_choose(dealer_bj=self.dealer.blackjack_check())
                        self.move_activation(player=player)
                case 'stand':
                    player.stand()
                case 'surrender':
                    if player.surrender():
                        self.remove_player(player=player)

        def choose_move_player(self, player: Human | Bot) -> None:
            hand_value: int = player.hand_value()
            if hand_value <= 21:
                player.get_choose(dealer_bj=self.dealer.blackjack_check())
                if player.choose == 'hit':
                    self.move_activation(player=player)
            elif hand_value > 21:
                print(f'{player} lose this round: -{player.bet}$')
                self.remove_player(player=player)

        def showing_dealt_cards(self, player: Player) -> None:
            match player:
                case Dealer() as dealer:
                    dealer._show_dealt_cards()
                case Human() as human:
                    player: Human
                    if human._show_dealt_cards(dealer=self.dealer):
                        if human.blackjack_check() and not self.dealer.blackjack_check():
                            human._player_win_bj()
                            # self.hand_analysis(player=player)
                        self.remove_player(player=human)
                case Bot() as bot:
                    if bot._show_dealt_cards(dealer=self.dealer):
                        self.remove_player(player=bot)

        @staticmethod
        def apply_method(players: list[Human | Bot], method: Callable[..., None], **kwargs) -> None:
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

            self.showing_dealt_cards(player=dealer)
            self.apply_method(players=humans, method=self.showing_dealt_cards)
            self.apply_method(players=bots, method=self.showing_dealt_cards)

            self.apply_method(players=humans, method=self.choose_move_player)
            self.apply_method(players=bots, method=self.choose_move_player)

            print('Players decisions.')
            self.apply_method(players=bots, method=self.move_activation)
            self.apply_method(players=humans, method=self.move_activation)
            self.move_dealer(dealer=dealer)

            self.apply_method(players=humans, method=self.hand_analysis)
            self.apply_method(players=bots, method=self.hand_analysis)

            self.apply_method(players=humans, method=self.remove_player)
            self.apply_method(players=bots, method=self.remove_player)

            self.round_end()

    @staticmethod
    def endgame():
        Deck.del_deck()
        print('Game the end.')

    def poor_remove(self, player: Human | Bot):
        if player.money < 1:
            print(f'{player} out of money')
            self.__Round.remove_player(self=self, player=player)  # attention fake self!

    def gnrt_deck(self):
        self.deck_inst = Deck()

    def gnrt_player(self, player_type):
        match player_type:
            case 'Human':
                human_count = 1
                while True:
                    try:
                        human_count = int(input('Write, human players count: '))
                    except ValueError:
                        print('You need to enter a int number')
                        continue
                    break
                for num in range(1, human_count + 1):
                    while True:
                        name = input(f'Write name player{num}: ')
                        if name.isalpha():
                            break
                        print('Name can contain only letters. Try again')
                    # name = f'test{num}'  # for autogame
                    h = Human(name=name)
                    self.human_plrs.append(h)
            case 'Bot':
                bot_count = 1
                while True:
                    try:
                        bot_count = int(input('Write, bot players count: '))
                    except ValueError:
                        print('You need to enter a int number')
                        continue
                    break
                for num in range(1, bot_count + 1):
                    name = f'Bot{num}'
                    b = Bot(name=name)
                    self.bot_plrs.append(b)

    def start_game(self):
        self.gnrt_player(player_type='Human')
        self.gnrt_player(player_type='Bot')
        self.gnrt_deck()

        # play rounds
        while self.human_plrs or self.bot_plrs:
            self.__Round(human_plrs=self.human_plrs.copy(),
                         bot_plrs=self.bot_plrs.copy(),
                         dealer=self.dealer,
                         deck_inst=self.deck_inst)
            self.__Round.apply_method(players=self.human_plrs, method=self.poor_remove)
            self.__Round.apply_method(players=self.bot_plrs, method=self.poor_remove)
            self.__Round.remove_player(self=self, player=self.dealer)  # attention fake self!

        self.endgame()
