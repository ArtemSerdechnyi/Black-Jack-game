from Player import Bot, Human, Dealer
from Deck import Deck



class Game:

    def __init__(self):
        self.human_plrs: list[Human] = []
        self.bot_plrs: list[Bot] = []
        self.dlr: Dealer
        self.deck_inst: Deck

    def player_reward(self, player: Human | Dealer | Bot):
        pass

    def caller_action_based_on_player_cards(self):
        pass


    def player_move(self, player: Human | Dealer | Bot, choose: str):
        match choose:
            case 'hit':
                player.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=1)
                if player.blackjack_check():
                    print(f'{player}, Black Jack')
                    # todo reward
            case 'stand':
                pass
            case 'double':
                if player.money - player.bet < 0:
                    print('Not enough money to double! Choose something else.')
                    choose = player.get_human_choose()
                    self.player_move(player=player, choose=choose)
                else:
                    player.double_bet()
            case 'surrender':
                pass

    def print_card_player(self, player_type):
        match player_type:
            case 'Dealer':
                self.dlr.print_card()
            case 'Human':
                for human in self.human_plrs:
                    human.print_card()
                    # print(f'{self} card: ', end='')
                    # print(*(card for card in self.cards))
                    if self.dlr.blackjack_check():
                        pass  # todo
                    elif human.blackjack_check():
                        print(f'{human}, Black Jack')
                        # todo reward
                    else:
                        choose: str = human.get_human_choose()
                        self.player_move(player=human, choose=choose)
            case 'Bot':
                for bot in self.bot_plrs:
                    bot.print_card()
                    if self.dlr.blackjack_check():
                        print(f'{bot}, Black Jack')
                        # todo reward
                    else:
                        pass  # todo bot logic
    def give_cards_to_players(self, player_type):
        match player_type:
            case 'Human':
                for human in self.human_plrs:
                    human.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)
            case 'Bot':
                for bot in self.bot_plrs:
                    bot.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)
            case 'Dealer':
                self.dlr.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)

    def create_bet_players(self, player_type):
        match player_type:
            case 'Human':
                for human in self.human_plrs:
                    human.place_bet()

            case 'Bot':
                for bot in self.bot_plrs:
                    bot.place_bet()

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
            case 'Dealer':
                self.dlr = Dealer(name='Dealer')

    def start_game(self):
        self.gnrt_player(player_type='Human')
        self.gnrt_player(player_type='Bot')
        self.gnrt_player(player_type='Dealer')
        self.gnrt_deck()

        self.create_bet_players(player_type='Human')
        self.create_bet_players(player_type='Bot')

        self.give_cards_to_players(player_type='Dealer')
        self.give_cards_to_players(player_type='Human')
        self.give_cards_to_players(player_type='Bot')

        self.print_card_player(player_type='Dealer')
        # self.print_card_player(player_type='Human')
        # self.print_card_player(player_type='Bot')


