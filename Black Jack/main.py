
from Game import Game



if __name__ == '__main__':
    def start_game():
        g = Game()
        g.start_game()


    start = input('Start the game?(yes/not)\n')
    while start == 'yes':
        start_game()
        start = input('Play again?(yes/not)\n')
    exit(1)