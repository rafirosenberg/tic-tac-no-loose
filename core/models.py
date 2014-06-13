from django.db import models
from django.contrib.auth.models import User

class Game(models.Model)
    player = models.ForeignKey(User)
    computer = 'X'
    board = models.CharField(max_length=100,
    default = pickle.dumps(['']*9))
    winning_rows = [[0,1,2], [3,4,5], [6,7,8], # horizontal
                    [0,3,6], [1,4,7], [2,5,8], # vertical
                    [0,4,8], [2,4,6]] # diagonal
    corners = [0,2,6,8]
    center = 4

    def get_board(self):
        return pickle.loads(str(self.board))

    def make_move(self, player, move):
        """
        player could be either computer or user, move is a number from 0-8
        """
        board = self.get_board()
        board[move] = player
        self.board = pickle.dumps(board)
        self.save()
    def get_valid_moves(self):
        """
        Returns a list of valid get_valid_moves ...
        """ 
        board = self.get_board()
        return [pos for pos in range(9) if board[pos] == '']

    def get_winner(self):
        """
        Determine if one player has won the game. Returns X, O, T for Tie, or None
        """ 
        board = self.get_board()
        #winner present
        for row in winning_rows:
            if board[row[0]] != '' and self.all_equal([board[i] for i in row]):
                return board[row[0]]
        #tie
        if not self.get_valid_moves():
            return "T"

        #game not over
        return None
        
    def get_corner(self):
        """
        computer gets a corner as part of strategy.
        """
        move = [m for m in corners if m in get_valid_moves()][0]
        make_move(computer, move)
    def get_center(self):
        make_move(computer, 4)

