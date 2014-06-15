from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
import pickle
from core.models import Game
from core.views import create_move


class TestTicTacToeBoard(TestCase):
    def setUp(self):
        self.player = User.objects.create(username='X')

        self.player.save()

    def test_finds_winner(self):
        """
        Tests that getting a winner works properly
        """
        board = pickle.dumps(['X', 'X', 'X', '', '', '', '', '', ''])
        game = Game(player=self.player,
                    board=board)
        winner = game.get_winner()

        self.assertEqual(winner, 'X')

    def test_doesnt_find_winner(self):
        board = pickle.dumps(['', '', '', '', '', '', '', '', ''])
        game = Game(player=self.player,
                    board=board)
        winner = game.get_winner()

        self.assertEqual(winner, None)

    def test_find_tie(self):
        """
        Tests that you get a tie when the board is full
        """
        board = pickle.dumps(['X', 'X', 'O',
                              'O', 'O', 'X',
                              'X', 'O', 'X'])

        game = Game(player=self.player,
                    board=board)
        winner = game.get_winner()

        self.assertEqual(winner, '')

    def test_make_move(self):
        """
        Tests that you can make moves
        """
        board = pickle.dumps(['', '', '', '', '', '', '', '', ''])

        game = Game(player=self.player,
                    board=board)

        game.make_move('X', 0)
        board = pickle.dumps(['X', '', '', '', '', '', '', '', ''])

        self.assertEqual(board, game.board)

    def test_gets_valid_moves(self):
        """
        Tests that getting valid moves works properly
        """
        board = pickle.dumps(['', '', '', '', '', '', '', '', ''])
        game = Game(player=self.player,
                    board=board)
        moves = game.get_valid_moves()

        self.assertEqual(len(moves), 9)

    def test_doesnt_gets_valid_moves(self):
        """
        Tests that getting valid moves works properly
        """
        board = pickle.dumps(['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'])
        game = Game(player=self.player,
                    board=board)
        moves = game.get_valid_moves()

        self.assertEqual(len(moves), 0)

    # def test_center(self):
    #     """
    #     Tests that center works properly
    #     """
    #     board = pickle.dumps(['', '', '', '', '', '', '', '', ''])
    #     game = Game(player=self.player,
    #                 board=board)
    #     game.center()
    #     self.assertEqual(game.board,
    #                      pickle.dumps(['', '', '', '', 'O', '', '', '', '']))

    # def test_corner(self):
    #     """
    #     Tests that corner works properly
    #     """
    #     board = pickle.dumps(['', '', '', '', '', '', '', '', ''])
    #     game = Game(player=self.player,
    #                 board=board)
    #     game.corner()
    #     game.corner()
    #     game.corner()
    #     game.corner()
    #     self.assertEqual(pickle.loads(str(game.board)),
    #                      ['O', '', 'O', '', '', '', 'O', '', 'O'])
    def test_defend(self):
        """
        Tests that defend works properly
        """
        board = pickle.dumps(['X', '', '', '', '', '', '', '', ''])
        game = Game(player=self.player,
                    board=board)
        d = game.defend()
        self.assertEqual(d,4)
        board = pickle.dumps(['X', '', 'X', '', 'O', '', '', '', ''])
        game = Game(player=self.player,
                    board=board)
        d = game.defend()
        self.assertEqual(d,1)
        board = pickle.dumps(['X', 'X', '', '', 'O', '', '', '', ''])
        game = Game(player=self.player,
                    board=board)
        d = game.defend()
        self.assertEqual(d,2)
        board = pickle.dumps(['X', '', '', '', 'O', '', 'X', '', 'X'])
        game = Game(player=self.player,
                    board=board)
        d = game.defend()
        self.assertEqual(d,2)
        board = pickle.dumps(['X', 'O', 'X', 'X', 'O', '', 'O', '', 'X'])
        game = Game(player=self.player,
                    board=board)
        d = game.defend()
        self.assertEqual(d,5)


    # def test_computer_move(self):
    #     """
    #     Tests that computer_move works properly
    #     """
    #     board = pickle.dumps(['X', '', '', '', '', '', '', '', ''])
    #     game = Game(player=self.player, board=board)
    #     d = game.computer_move()
    #     self.assertEqual(d,'center')

