from django.shortcuts import render
from django.http import HttpResponse

from core.models import Game

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
    game = Game.objects.get(pk=game_id)
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

def new_game(request):
    """
    Renders a tic tac toe board to be played for a specific game
    """
    last_game = Game.objects.all().last()
    game = Game.objects.create(pk=int(last_game.id) + 1)
    game_id = game.id
    return view_game(request, game_id)
