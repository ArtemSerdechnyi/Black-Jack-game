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

        def hand_analysis(self, players: list[Human | Bot]):
            dealer = self.dealer
            for player in players.copy():
                money = player.money
                bet = player.bet
                player_hand_value = player.hand_value()
                dealer_hand_value = dealer.hand_value()
                print(f'{player} card: {player.print_card()} vs'
                      f' {dealer} card: {dealer.print_card()}')
                print(f'{player} score: {player_hand_value} vs'
                      f' {dealer} score: {dealer_hand_value}')
                if dealer_hand_value > 21:
                    if player_hand_value > 21:
                        print(f'Draw. {player} gets {bet} back')
                        print(f'{player} money: {player.money}')

                if player_hand_value > dealer_hand_value:
                    print(f'{player} win {bet * 3 / 2} $')
                    money += bet
                    money += bet * 3 / 2
                    print(f'{player} money: {player.money}')
                    players.remove(player)
                elif player_hand_value < dealer_hand_value:
                    print(f'{player} lost {bet} $')
                    players.remove(player)
                else:
                    print(f'Draw. {player} gets {bet} back')
                    print(f'{player} money: {player.money}')
                    players.remove(player)

        def move_dealer(self, dealer: Dealer):
            if dealer.hand_value() < 16:
                print("Dealer get the card")
                while not dealer.hand_value() >= 17:
                    dealer.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=1)
                dealer.print_card()

        def move_activation(self, players: list[Human | Bot]):
            for player in players:
                match player.choose:
                    case 'hit':
                        player.get_number_of_cards(deck_inst=self.deck_inst,
                                                   number_of_cards=1)
                    case 'stand':
                        pass
                    case 'surrender':
                        print(f'{player} got half of the bet back.')
                        player.money += player.bet / 2
                        print(f'{player} money: {player.money}')

        @staticmethod
        def check_all_move_finish(humans: list[Human], bots: list[Bot]) -> bool:
            for human in humans:
                if human.choose == 'hit':
                    break
            else:
                for bot in bots:
                    if bot.choose == 'hit':
                        break
                else:
                    return False
            return True

        def choose_move_player(self, players: list[Human | Bot]):
            for player in players.copy():
                hand_value: int = player.hand_value()
                if hand_value < 21:
                    player.get_choose()
                elif hand_value > 21:
                    print(f'{player} lose this round: -{player.bet}$')
                    players.remove(player)

        def print_card_player(self, player_type):
            match player_type:
                case 'Dealer':
                    self.dealer.print_card()
                case 'Human':
                    for human in self.human_plrs:
                        human.print_card()
                case 'Bot':
                    for bot in self.bot_plrs:
                        bot.print_card()

        def give_cards_to_players(self, players_or_dealer: list[Player] | Dealer):
            if isinstance(players_or_dealer, list):
                for player in players_or_dealer:
                    player.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)
            else:
                players_or_dealer.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)

        @staticmethod
        def create_bet_players(players: list[Player]):
            for player in players:
                player.place_bet()

        def game_round(self, humans: list[Human], bots: list[Bot], dealer: Dealer):
            self.create_bet_players(players=humans)
            self.create_bet_players(players=bots)

            self.give_cards_to_players(players_or_dealer=humans)
            self.give_cards_to_players(players_or_dealer=bots)
            self.give_cards_to_players(players_or_dealer=dealer)

            self.print_card_player(player_type='Dealer')
            self.print_card_player(player_type='Human')
            self.print_card_player(player_type='Bot')

            while self.check_all_move_finish(humans=humans, bots=bots):
                self.choose_move_player(players=humans)
                self.choose_move_player(players=bots)
                self.move_activation(players=humans)
                self.move_activation(players=bots)
            self.move_dealer(dealer=dealer)

            self.hand_analysis(players=humans)
            self.hand_analysis(players=bots)

    @staticmethod
    def call_method_on_each_player(players: list[Player], methode):
        for player in players:
            player.methode()
            print(player.print_card())


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

        while True:
            round = Game.Round(human_plrs=self.human_plrs.copy(), bot_plrs=self.bot_plrs.copy(),
                               dealer=self.dealer, deck_inst=self.deck_inst)
            # round.game_round(humans=round.human_plrs, bots=round.bot_plrs, dealer=self.dealer)
