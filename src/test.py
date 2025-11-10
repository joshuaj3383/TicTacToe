from src.ttt_logic import ttt_logic

'''
program to test the ttt_logic class without having to worry about the GUI
allows the user to play against the ai through the terminal
asks them to choose X or O
'''

def print_board(board):
    for i in range(9):
        print(board[i], end=" ")
        if (i + 1) % 3 == 0:
            print()

if __name__ == "__main__":
    game = ttt_logic()
    game.play_best_move()
    print_board(game.board)

    while game.getWinner() is None:
        n = int(input("enter n: ")) - 1
        r, c = n // 3, n % 3
        game.play(int(r), int(c))
        game.play_best_move()
        print_board(game.board)

    print(game.getWinner())