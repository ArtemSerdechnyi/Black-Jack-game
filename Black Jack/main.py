from Game import Game

if __name__ == '__main__':
    def start_game():
        Game().start_game()
        print('Game the end.')


    start = input('Start the game?(yes/not)\n')
    # todo Exceptions
    while start == 'yes':
        start_game()
        start = input('Play again?(yes/not)\n')
        # todo Exceptions
    exit(1)
