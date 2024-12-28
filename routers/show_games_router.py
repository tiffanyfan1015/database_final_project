from flask import Blueprint, render_template, request
from controllers.show_games_controller import fetch_all_games, fetch_game_details, fetch_filtered_games

game_bp = Blueprint('game_bp', __name__)

@game_bp.route("/")
def menu():
    """
    Display the main page with all games or filtered games.
    Query Parameters:
        - name: Name keyword for game search.
        - genres: Genre(s) to filter games by.
        - platforms: Platform(s) to filter games by.
    """
    filters = {
        "name": request.args.get("name"),
        "genres": request.args.get("genres"),
        "platforms": request.args.get("platforms"),
    }
    if any(filters.values()):
        games = fetch_filtered_games(filters)
    else:
        games = fetch_all_games()
    return render_template("new_index.html", games=games)

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
