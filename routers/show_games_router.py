from flask import Blueprint, render_template, request
from controllers.show_games_controller import fetch_filtered_games, fetch_game_details
import time

game_bp = Blueprint('game_bp', __name__)

cache = {}
CACHE_TIMEOUT = 300

def get_from_cache(cache_key):
    """Retrieve data from cache if valid."""
    cached_data = cache.get(cache_key)
    if cached_data:
        data, timestamp = cached_data
        if time.time() - timestamp < CACHE_TIMEOUT:
            return data
    return None

def set_to_cache(cache_key, data):
    """Set data in cache with the current timestamp."""
    cache[cache_key] = (data, time.time())

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
    cache_key = f"game_details_{appid}"
    
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    game, requirements, reviews = fetch_game_details(appid)
    
    if not game:
        return "Game not found!", 404
    if not requirements:
        return "Requirements not found!", 404

    rendered_template = render_template(
        'games_detail.html',
        game=game,
        requirements=requirements,
        reviews=reviews
    )
    
    set_to_cache(cache_key, rendered_template)
    
    return rendered_template
