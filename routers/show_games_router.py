from flask import Blueprint, render_template, request
from controllers.show_games_controller import fetch_filtered_games, fetch_game_details

game_bp = Blueprint('game_bp', __name__)

@game_bp.route("/")
def menu():
    """
    Display the main page with games filtered and searched.
    Query Parameters:
        - search: Flexible search keywords.
        - platforms: Platforms to filter games by.
        - age: Required age to filter games by.
        - categories: Categories to filter games by.
    """
    filters = {
        "search": request.args.get("search"),
        "platforms": request.args.get("platforms"),
        "age": request.args.get("age"),
        "categories": request.args.get("categories"),
    }
    
    games = fetch_filtered_games(filters)
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
