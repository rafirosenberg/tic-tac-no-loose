from django.shortcuts import render


def view_game(request, game_id):
    """
    Renders a tic tac toe board to be played for a specific game
    """
    board = game.get_board()
    winner = game.get_winner()
    context = { "game_id": game_id,
                'board': board,
                'player': game.player,
                'winner': winner,
                'game_over': False if winner is None else True
              }
    return render('core/view_game.html')
