from django.db import models
from django.contrib.auth.models import User
import pickle


class Game(models.Model):
    player = models.ForeignKey(User)
    computer = 'O'
    board = models.CharField(max_length=100,
                             default=pickle.dumps(['']*9))
    winning_rows = [[0, 1, 2],  [3, 4, 5],  [6, 7, 8],  # horizontal
                    [0, 3, 6],  [1, 4, 7],  [2, 5, 8],  # vertical
                    [0, 4, 8],  [2, 4, 6]]  # diagonal
    corners = [0, 2, 6, 8]
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
        if self.get_winner() is not None:
            return('youfailed!')
        else:
            for row in self.winning_rows:
                trouble = [board[pos] for pos in row]
                if trouble.count(self.player.username) == 2:
                    if trouble.count('O') < 1:
                        move = trouble.index('')
                        break
                else:
                    # get center
                    if board[4] == '':
                        move = 4
                        break
                    # get a corner
                    else:
                        if len([m for m in self.corners if m in self.get_valid_moves()]) > 0:
                            move = [m for m in self.corners if m in self.get_valid_moves()][0]
                            break
                        else:
                            move = self.get_valid_moves()[0]
                            break
            self.make_move(self.computer, move)
            return(move)
