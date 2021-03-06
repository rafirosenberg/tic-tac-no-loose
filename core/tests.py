from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
import pickle
from core.models import Game
from core.views import create_move

#From https://github.com/sontek-archive/django-tictactoe ----------------------


class TestTicTacToeBoard(TestCase):
    def setUp(self):
        self.player = User.objects.create(username='Joe')
        self.player.save()

    def test_finds_winner(self):
        """
        Tests that getting a winner works properly
        """
        board = pickle.dumps(['X', 'X', 'X', '', '', '', '', '', ''])
        game = Game(board=board)
        winner = game.get_winner()
        self.assertEqual(winner, 'X')

    def test_doesnt_find_winner(self):
        board = pickle.dumps(['', '', '', '', '', '', '', '', ''])
        game = Game(board=board)
        winner = game.get_winner()

        self.assertEqual(winner, None)

    def test_find_tie(self):
        """
        Tests that you get a tie when the board is full
        """
        board = pickle.dumps(['X', 'X', 'O',
                              'O', 'O', 'X',
                              'X', 'O', 'X'])

        game = Game(board=board)
        winner = game.get_winner()

        self.assertEqual(winner, '')

    def test_make_move(self):
        """
        Tests that you can make moves
        """
        board = pickle.dumps(['', '', '', '', '', '', '', '', ''])

        game = Game(board=board)

        game.make_move('X', 0)
        board = pickle.dumps(['X', '', '', '', '', '', '', '', ''])
        self.assertEqual(board, game.board)

    def test_gets_valid_moves(self):
        """
        Tests that getting valid moves works properly
        """
        board = pickle.dumps(['', '', '', '', '', '', '', '', ''])
        game = Game(board=board)
        moves = game.get_valid_moves()

        self.assertEqual(len(moves), 9)

    def test_doesnt_gets_valid_moves(self):
        """
        Tests that getting valid moves works properly
        """
        board = pickle.dumps(['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'])
        game = Game(board=board)
        moves = game.get_valid_moves()

        self.assertEqual(len(moves), 0)
# end From https://github.com/sontek-archive/django-tictactoe -----------------

    def test_win(self):
        '''
        tests that winning is first choice
        '''
        board = pickle.dumps({0: 'X', 1: '', 2: 'O',
                              3: '', 4: '', 5: '',
                              6: 'X', 7: '', 8: 'O'})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 5)

        board = pickle.dumps({0: 'X', 1: 'O', 2: 'X',
                              3: '', 4: 'O', 5: '',
                              6: 'O', 7: '', 8: 'X'})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 7)

        board = pickle.dumps({0: 'X', 1: 'O', 2: 'X',
                              3: '', 4: 'O', 5: '',
                              6: 'X', 7: '', 8: ''})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 7)

        board = pickle.dumps({0: 'X', 1: '', 2: 'X',
                              3: '', 4: 'O', 5: '',
                              6: '', 7: '', 8: ''})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 1)

    def test_defend(self):
        """
        random defence tests
        """
        board = pickle.dumps({0: 'X', 1: '', 2: 'X',
                              3: '', 4: 'O', 5: '',
                              6: '', 7: '', 8: ''})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 1)

        board = pickle.dumps({0: 'X', 1: '', 2: 'O',
                              3: '', 4: 'O', 5: '',
                              6: '', 7: '', 8: 'X'})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 6)

        board = pickle.dumps({0: 'X', 1: 'O', 2: 'X',
                              3: '', 4: 'O', 5: '',
                              6: 'O', 7: 'X', 8: 'X'})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 5)

    def test_defend_special(self):
        '''
        tests first of the special cases
        '''
        board = pickle.dumps({0: 'X', 1: '', 2: '',
                              3: '', 4: 'O', 5: '',
                              6: '', 7: '', 8: 'X'})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 1)

    def test_block_el_6(self):
        '''
        checks a random additional el pattern
        '''
        board = pickle.dumps({0: 'X', 1: '', 2: '',
                              3: '', 4: 'O', 5: '',
                              6: '', 7: 'X', 8: ''})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 6)

    def test_block_el_8(self):
        '''
        checks all three possibilities of lower right corner el
        '''
        board = pickle.dumps({0: '', 1: '', 2: '',
                              3: '', 4: 'O', 5: 'X',
                              6: '', 7: 'X', 8: ''})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 8)

        board = pickle.dumps({0: '', 1: '', 2: 'X',
                              3: '', 4: 'O', 5: '',
                              6: '', 7: 'X', 8: ''})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 8)

        board = pickle.dumps({0: '', 1: '', 2: '',
                              3: '', 4: 'O', 5: 'X',
                              6: 'X', 7: '', 8: ''})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 8)

    def test_defend_center(self):
        """
        Tests that first choice is center if no other issues
        to be taken care of
        """
        board = pickle.dumps({0: 'X', 1: '', 2: '',
                              3: '', 4: '', 5: '',
                              6: '', 7: '', 8: ''})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 4)

    def test_defend_corner(self):
        """
        Tests that first choice is corner if center is taken
        and no other issues.
        """
        board = pickle.dumps({0: 'X', 1: '', 2: '',
                              3: '', 4: 'O', 5: 'X',
                              6: '', 7: '', 8: ''})
        game = Game(board=board)
        d = game.defend()
        self.assertEqual(d, 2)
