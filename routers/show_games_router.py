from flask import Blueprint, render_template
from controllers.show_games_controller import fetch_all_games, fetch_game_details

game_bp = Blueprint('game_bp', __name__)

@game_bp.route("/game/")
def menu():
    games = fetch_all_games()
    return render_template("games_index.html", games=games)

@game_bp.route('/game/<int:appid>')
def game_details(appid):
    game, requirements = fetch_game_details(appid)
    
    if not game:
        return "Game not found!", 404
    if not requirements:
        return "Requirements not found!", 404

    return render_template(
        'games_detail.html',
        game=game,
        requirements=requirements
    )
