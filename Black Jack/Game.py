from Player import Player, Bot, Human, Dealer
from Deck import Deck


class Game:

    def __init__(self):
        self.human_plrs: list[Human] = []
        self.bot_plrs: list[Bot] = []
        self.dlr: Dealer
        self.deck_inst: Deck

    def player_move(self, player_inst: Player, choose: str):
        match choose:
            case 'hit':
                player_inst.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=1)
            case 'stand':
                pass
            case 'double':
                pass
            case 'surrender':
                pass

    def print_card(self, player_type):
        match player_type:
            case 'Dealer':
                print('Dealer card: ', end='')
                for ind, card in enumerate(self.dlr.cards):
                    if not ind:
                        if card.rank == 'A' or card.rank == '10':
                            print(card.rank, card.suit, sep='', end=', ')
                            continue
                        print(f'{card.rank}{card.suit}, and one card is face down. ')
                        break
                    elif self.dlr.hand_value() == 21:
                        print(card.rank, card.suit, sep='', end=' BlACK JACK!')
                    else:
                        print('and one card is face down.')
            case 'Human':
                for human in self.human_plrs:
                    print(f'{human.name} card: ', end='')
                    for card in human.cards:
                        print(card.rank, card.suit, sep='', end=' ')
                    print()
                    if self.dlr.hand_value() == 21:
                        pass
                    else:
                        while True:
                            choose = {'hit', 'stand', 'double', 'surrender'}
                            human_choose = input('Choose actions: (hit, stand, double, surrender)')
                            if human_choose in choose:
                                break
                            else:
                                print('Invalid choice! Try again.')

    def get_card_for_player(self, player_type):
        match player_type:
            case 'Human':
                for human in self.human_plrs:
                    human.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)
            case 'Bot':
                for bot in self.bot_plrs:
                    bot.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)
            case 'Dealer':
                self.dlr.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)

    def get_bet(self, player_type):
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
                for num in range(1, human_count + 1):
                    # name = input(f'Write name player{num}: ') # do this when finished
                    name = f'test{num}'  # del this when finished
                    h = Human(name=name)
                    self.human_plrs.append(h)
            case 'Bot':
                bot_count = int(input('Write, bot players count: '))
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

        # self.get_bet(player_type='Human')
        # self.get_bet(player_type='Bot')

        self.get_card_for_player(player_type='Dealer')
        self.get_card_for_player(player_type='Human')
        self.get_card_for_player(player_type='Bot')

        self.print_card(player_type='Dealer')
        self.print_card(player_type='Human')
