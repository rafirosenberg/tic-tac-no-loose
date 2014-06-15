from django.shortcuts import render
from django.http import HttpResponse

from core.models import Game


def create_move(request, game_id):
    game = Game.objects.get(pk=game_id)
    move = int(request.POST['move'])
    winner = game.get_winner()
    if winner:
        print('ho')
    return HttpResponse()


def view_game(request, game_id):
    """
    Renders a tic tac toe board to be played for a specific game
    """
    game = Game.objects.get(pk=game_id)
    board = game.get_board()
    winner = game.get_winner()
    context = { "game_id": game_id,
                'board': board,
                'player': game.player,
                'winner': winner,
                'game_over': False if winner is None else True
              }
    return render(request, 'core/view_game.html', context)
