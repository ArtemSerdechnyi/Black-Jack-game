from Game import Game

if __name__ == '__main__':
    def start_game():
        g = Game()
        g.start_game()


    start = input('Start the game?(yes/not)\n')
    # todo Exceptions
    while start == 'yes':
        start_game()
        start = input('Play again?(yes/not)\n')
        # todo Exceptions
    exit(1)
