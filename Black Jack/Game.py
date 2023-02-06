from Player import Bot,Human,Dealer
from Deck import Deck
from typing import Type


class Game:

    def __init__(self):
        self.human_plrs: list[Human] = []
        self.bot_plrs: list[Bot] = []
        self.dlr: Dealer
        self.deck_inst: Deck

    def print_card(self, player_type):
        match player_type:
            case 'Dealer':
                print('Dealer card: ',end='')

                for ind, card in enumerate(self.dlr.cards):
                    if not ind:
                        if card.rank == 'A' or card.rank == '10':
                            print(card.rank, card.suit, sep='', end=', ')
                            continue
                        print(card.rank, card.suit,sep='')
                        break
                    elif self.dlr.hand_value() == 21:
                        print(card.rank, card.suit)



                    print(card.rank,card.suit, sep='')

            case 'Human':
                pass



    def get_card_for_player(self,player_type):
        match player_type:
            case 'Human':
                for human in self.human_plrs:
                    human.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)
            case 'Bot':
                for bot in self.bot_plrs:
                    bot.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)
            case 'Dealer':
                self.dlr.get_number_of_cards(deck_inst=self.deck_inst, number_of_cards=2)


    def get_bet(self,player_type):
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
                for _ in range(human_count):
                    # name = input('Write name player: ')
                    name = 'test'
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



        # self.print_card(player_type='Dealer')











