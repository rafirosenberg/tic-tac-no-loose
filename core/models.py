from django.db import models
from django.contrib.auth.models import User
import pickle


class Game(models.Model):
    user = 'X'
    computer = 'O'
    board = models.CharField(max_length=100,
                             default=pickle.dumps({0:'',1:'',2:'',
                                                   3:'',4:'',5:'',
                                                   6:'',7:'',8:''}))

    winning_rows = ((0, 1, 2),  (3, 4, 5),  (6, 7, 8),  # horizontal
                    (0, 3, 6),  (1, 4, 7),  (2, 5, 8),  # vertical
                    (0, 4, 8),  (2, 4, 6))  # diagonal

    corners = [0, 2, 6, 8]

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

    def all_equal(self, list):
        """
        Returns True if all the elements in a list are equal, or if
        the list is empty.
        """
        return not list or list == [list[0]] * len(list)

    def get_winner(self):
        """
        Determine if one player has won the game.
        Returns X, O, "" for Tie, or None
        """
        board = self.get_board()
        #winner present
        for row in self.winning_rows:
            if board[row[0]] != '' and self.all_equal([board[i] for i in row]):
                return board[row[0]]
        #tie
        if not self.get_valid_moves():
            return ""

        #game not over
        return None

    def defend(self):
        """
        Choose defensive moves for computer.
        """
        board = self.get_board()
        #go for the win
        for row in self.winning_rows:
            trouble = [board[pos] for pos in row]
            if trouble.count('O') == 2:
                if trouble.count('X') == 0:
                    move = row[trouble.index('')]
                    break
            else:
                move = None
        if not move:
            #check for need to defend
            for row in self.winning_rows:
                trouble = [board[pos] for pos in row]
                if trouble.count('X') == 2:
                    if trouble.count('O') == 0:
                        move = row[trouble.index('')]
                        break
        if not move:
            #force a move in this special case
            if board == {0:'X',1:'',2:'',
                        3:'',4:'O',5:'',
                        6:'',7:'',8:'X'}:
                move = 1
        if not move:
            #force a move in this special case
            if board == {0:'',1:'',2:'X',
                        3:'',4:'O',5:'',
                        6:'X',7:'',8:''}:
                move = 1
        if not move:
            #force a move in this special case
            if board == {0:'',1:'X',2:'',
                        3:'X',4:'O',5:'',
                        6:'',7:'',8:''}:
                move = 0
        if not move:
            #force a move in this special case
            if board == {0:'',1:'X',2:'',
                        3:'',4:'O',5:'X',
                        6:'X',7:'',8:''}:
                move = 2
        if not move:
            #force a move in this special case
            if board == {0:'',1:'',2:'',
                        3:'X',4:'O',5:'',
                        6:'',7:'X',8:''}:
                move = 6
        if not move:
            #force a move in this special case
            if board == {0:'',1:'',2:'',
                        3:'',4:'O',5:'X',
                        6:'',7:'X',8:''}:
                move = 8
        if not move:
            # get center
            if 4 in (self.get_valid_moves()):
                move = 4
        if not move:            
            # get a corner
            if len([m for m in self.corners if m in self.get_valid_moves()]) > 0:
                move = [m for m in self.corners if m in self.get_valid_moves()][0]
            #choose from what is left
            else:
                move = self.get_valid_moves()[0]
        self.make_move(self.computer, move)
        return(move)

