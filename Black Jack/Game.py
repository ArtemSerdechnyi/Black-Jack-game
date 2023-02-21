from Player import Bot, Human, Dealer, Player
from Deck import Deck


class Game:

    def __init__(self):
        self.human_plrs: list[Human] = []
        self.bot_plrs: list[Bot] = []
        self.dealer: Dealer = Dealer(name='Dealer')
        self.deck_inst: Deck

    class Round:
        def __init__(self, human_plrs: list[Human],
                     bot_plrs: list[Bot],
                     dealer: Dealer,
                     deck_inst: Deck):
            self.human_plrs: list[Human] = human_plrs
            self.bot_plrs: list[Bot] = bot_plrs
            self.dealer: Dealer = dealer
            self.deck_inst: Deck = deck_inst
            self.game_round(humans=self.human_plrs,
                            bots=self.bot_plrs,
                            dealer=self.dealer)

        @staticmethod
        def remove_player(players: list[Player], player: Player):
            player.cards.clear()
            players.remove(player)

        def hand_analysis(self, players: list[Human | Bot]):
            dealer = self.dealer
            for player in players.copy():
                bet = player.bet
                player_hand_value = player.hand_value()
                dealer_hand_value = dealer.hand_value()
                player.print_card()
                dealer.print_card()
                print(f'{player} score: {player_hand_value} vs'
                      f' {dealer} score: {dealer_hand_value}')
                if dealer_hand_value > 21:
                    if player_hand_value == 21:
                        print(f'{player} Blackjack, win {bet * 3 / 2} $')
                        player.money += bet + bet * 3 / 2
                        print(f'{player} money: {player.money}')
                    elif player_hand_value < 21:
                        print(f'{player}, win {bet} $')
                        player.money += bet + bet
                        print(f'{player} money: {player.money}')
                elif dealer_hand_value == 21:
                    if player_hand_value == 21:
                        print(f'Draw. {player} gets {bet} $ back')
                        player.money += bet
                        print(f'{player} money: {player.money}')
                    else:
                        print(f'{player} lost {bet} $')
                elif dealer_hand_value < 21:
                    if player_hand_value == 21:
                        print(f'{player} Blackjack, win {bet * 3 / 2} $')
                        player.money += bet + bet * 3 / 2
                        print(f'{player} money: {player.money}')
                    elif player_hand_value > dealer_hand_value:
                        print(f'{player} win {bet * 2} $')
                        player.money += bet + bet
                        print(f'{player} money: {player.money}')
                    elif player_hand_value < dealer_hand_value:
                        print(f'{player} lost {bet} $')
                    elif player_hand_value == dealer_hand_value:
                        print(f'Draw. {player} gets {bet} back')
                        player.money += bet
                        print(f'{player} money: {player.money}')

                self.remove_player(players=players, player=player)

        def move_dealer(self, dealer: Dealer):
            if dealer.hand_value() < 16:
                print("Dealer get the cards: ")
                while dealer.hand_value() < 17:
                    dealer.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=1)
                    print(f'Dealer get {dealer.cards[-1]}')
                dealer.print_card()

        def move_activation(self, players: list[Human | Bot]):
            def activate_move(player):
                match player.choose:
                    case 'hit':
                        player.get_number_of_cards(deck_inst=self.deck_inst,
                                                   number_of_cards=1)
                        if player.hand_value() > 21:
                            print(f'{player} lost. Hand value {player.hand_value()}')
                            self.remove_player(players=players, player=player)
                        else:
                            player.get_choose(dealer_bj=self.dealer.blackjack_check())
                            activate_move(player=player)
                    case 'stand':
                        print(f'{player} stand.')
                    case 'surrender':
                        print(f'{player} got half of the bet back.')
                        player.money += player.bet / 2
                        print(f'{player} money: {player.money}')
                        self.remove_player(players=players, player=player)

            for player in players.copy():
                activate_move(player=player)

        def choose_move_player(self, players: list[Human | Bot]):
            for player in players.copy():
                hand_value: int = player.hand_value()
                if hand_value <= 21:
                    player.get_choose(dealer_bj=self.dealer.blackjack_check())
                elif hand_value > 21:
                    print(f'{player} lose this round: -{player.bet}$')
                    self.remove_player(players=players, player=player)

        def print_card_player(self, players: list[Player]):
            for player in players.copy():
                match player:
                    case Dealer():
                        if not self.dealer.blackjack_check():
                            print(f'{self.dealer}: {self.dealer.firs_card}, and one card is face down.')
                        else:
                            self.dealer.print_card()
                            print('Blackjack')
                    case Human() as human:
                        players: list[Human]
                        player: Human
                        human.print_card()
                        if human.blackjack_check() and self.dealer.firs_card.rank == 'A':
                            print(f'{human} Blackjack!')
                            while True:
                                choice = input(f'{human} you want to take the win 1 to 1 (yes/no): ')
                                if choice == 'yes':
                                    print(f'{human} win {human.bet * 2} $')
                                    human.money += human.bet * 2
                                    print(f'{human} money {human.money}')
                                    self.remove_player(players=players, player=human)
                                    break
                                elif choice == 'no':
                                    print('Game continues win 3/2 bet')
                                    break
                                else:
                                    print("Try again.")
                    case Bot() as bot:
                        bot.print_card()

        def give_cards_to_players(self, players_or_dealer: list[Player] | Dealer):
            if isinstance(players_or_dealer, list):
                for player in players_or_dealer:
                    player.get_number_of_cards(deck_inst=self.deck_inst,
                                               number_of_cards=2)
            else:
                players_or_dealer.get_number_of_cards(deck_inst=self.deck_inst,
                                                      number_of_cards=2)

        # @staticmethod
        # def create_bet_players(players: list[Human | Bot]):
        #     for player in players:
        #         player.place_bet()

        @staticmethod
        def apply_method(players: list[Human | Bot | Dealer], method):
            for player in players:
                method(self=player)

        def game_round(self, humans: list[Human], bots: list[Bot], dealer: Dealer):
            # self.create_bet_players(players=humans)
            # self.create_bet_players(players=bots)
            self.apply_method(players=humans, method=Human.place_bet)
            self.apply_method(players=bots, method=Bot.place_bet)
            # self.apply_method(players=humans, method=Human.place_bet(self=Human)

            self.give_cards_to_players(players_or_dealer=humans)
            self.give_cards_to_players(players_or_dealer=bots)
            self.give_cards_to_players(players_or_dealer=dealer)

            self.print_card_player(players=[dealer])
            self.print_card_player(players=humans)
            self.print_card_player(players=bots)

            self.choose_move_player(players=humans)
            self.choose_move_player(players=bots)
            self.move_activation(players=humans)
            self.move_activation(players=bots)
            self.move_dealer(dealer=dealer)

            self.hand_analysis(players=humans)
            self.hand_analysis(players=bots)

    @staticmethod
    def poor_remove(players: list[Player]):
        for player in players.copy():
            if player.money < 1:
                print(f'{player} out of money')
                Game.Round.remove_player(players=players, player=player)

    def gnrt_deck(self):
        d = Deck()
        d.create_deck()
        self.deck_inst = d

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
            self.Round(human_plrs=self.human_plrs.copy(),
                       bot_plrs=self.bot_plrs.copy(),
                       dealer=self.dealer,
                       deck_inst=self.deck_inst)

            self.poor_remove(players=self.human_plrs)
            self.poor_remove(players=self.bot_plrs)
            self.Round.remove_player(players=[self.dealer], player=self.dealer)
