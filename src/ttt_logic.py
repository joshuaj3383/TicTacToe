import random
'''
Class which simulates and holds logic behind tic tac toe
Constructor allows user to choose X or O
The AI will then use the minimax algorithm to pick the best move 
'''
class ttt_logic:
    # initializer for who goes first (you always play as x)
    def __init__(self):
        self.board = [i + 1 for i in range(9)]
        self.turn = "X"

    # Returns whether the space is free to play in
    def isFree(self, idx):
        return 0 <= idx < 9 and self.board[idx] not in ("X", "O")

    # Changes the turn to the next
    def nextTurn(self):
        self.turn = "O" if self.turn == "X" else "X"

    # Return the next turn based on input
    @staticmethod
    def getNextTurn(turn):
        return "O" if turn == "X" else "X"

    # Returns the winner of a board, None if the game is in progress
    def getWinner(self):
        # Indexes for win
        win_conditions = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Row
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Column
            (0, 4, 8), (2, 4, 6) #Diagonal
        )

        # If all three conditions match, and it is not blank return who won
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] and self.board[condition[0]]:
                return self.board[condition[0]]

        # If there are still empty squares, the game is still continuing
        for val in self.board:
            if val != "X" and val != "O":
                return None

        # If the game has ended and no one has won it is a tie
        return 'T'

    # This function use recursion to calculate the value of a given position
    # It is given the current turn of the player as well as the player who
    # it is trying to maximize the score
    def minimax(self, alpha, beta, maxPlayer, turn):
        # Base case: Returns evaluation of the board
        winner = self.getWinner()
        if winner == maxPlayer:
            return 1
        if winner == self.getNextTurn(maxPlayer):
            return -1
        if winner == 'T':
            return 0

        # If it is the turn of maximizing player maximize the score
        if maxPlayer == turn:
            maxEval = -10
            # For each child move
            for i in range(9):
                if self.isFree(i):
                    # Play move, get score, revert move
                    self.board[i] = turn
                    testEval = self.minimax(alpha, beta, maxPlayer, self.getNextTurn(turn))
                    maxEval = max(maxEval, testEval)
                    self.board[i] = i + 1

                    # Trim for excess
                    alpha = max(alpha, testEval)
                    if beta <= alpha:
                        break

            return maxEval
        else: # If it is the minimizing player, minimize the score
            minEval = 10

            # For each child move
            for i in range(9):
                if self.isFree(i):
                    self.board[i] = turn
                    testEval = self.minimax(alpha, beta,
                                       maxPlayer, self.getNextTurn(turn))
                    minEval = min(minEval, testEval)
                    self.board[i] = i + 1

                    beta = min(beta, testEval)
                    if beta <= alpha:
                        break

            return minEval

    # Plays the best move and returns the row and column of it
    def play_best_move(self):
        if self.getWinner() is not None:
            return None

        move_list = []
        # Try out each legal move and get the evaluation
        for i in range(9):
            if self.isFree(i):
                self.board[i] = self.turn
                score = self.minimax(-100, 100, self.turn, self.getNextTurn(self.turn))
                move_list.append((i,score))
                self.board[i] = i + 1

        # Get the list of best moves and pick a random one
        max_val = max(x[1] for x in move_list)
        best_move_list = [x[0] for x in move_list if x[1] == max_val]

        # If it is the first turn (nothing has been played)
        # Then there is a 1/3 change to play in the middle
        # Otherwise there would only be 1/9 chance despite middle
        # Being the best move
        if not self.board.__contains__("X") and not self.board.__contains__("O"):
            if random.random() < 0.33:
                self.board[4] = self.turn
                self.nextTurn()
                return 1,1

        choice_idx = random.choice(best_move_list)

        self.board[choice_idx] = self.turn

        # Next turn
        self.nextTurn()

        # Get the row and column on best move
        r, c = divmod(choice_idx, 3)

        return r, c

    # Allows the user to enter a move
    def play(self, row: int, column: int) -> bool:
        idx = 3 * row + column

        if self.isFree(idx):
            self.board[idx] = self.turn

            self.nextTurn()
            return True
        else:
            return False