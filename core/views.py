from django.shortcuts import render
from django.http import HttpResponse

from core.models import Game
from django.http import HttpResponse

def create_move(request, game_id):
    game = Game.objects.get(pk=game_id)
    move = int(request.POST['move'])
    game.make_move('X', move)
    winner = game.get_winner()
    board=game.get_board()
    if winner == None:
        d = game.defend()
        winner = game.get_winner()
        board=game.get_board()
    context = { "game_id": game_id,
                'board': board.values(),
                'game': game,
                'player': 'X',
                'winner': winner,
                'game_over': False if winner is None else True
               }
    return render(request, 'core/view_game.html', context)
    


def view_game(request, game_id):
    """
    Renders a tic tac toe board to be played for a specific game
    """
    try:
        game = Game.objects.get(pk=game_id)
    except:
        game = Game.objects.create()
    board = game.get_board()
    winner = game.get_winner()
    context = { "game_id": game_id,
                'board': board.values(),
                'game': game,
                'player': 'X',
                'winner': winner,
                'game_over': False if winner is None else True
               }
    return render(request, 'core/view_game.html', context)

def new_game(request, game_id):
    """
    Renders a tic tac toe board to be played for a specific game
    """
    game = Game.objects.create(pk=int(game_id) + 1)
    board = game.get_board()
    winner = game.get_winner()
    context = { "game_id": game_id,
                'board': board.values(),
                'game': game,
                'player': 'X',
                'winner': winner,
                'game_over': False if winner is None else True
               }
    return render(request, 'core/view_game.html', context)
