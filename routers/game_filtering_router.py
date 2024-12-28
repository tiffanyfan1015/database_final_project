from flask import Blueprint, request, jsonify
from controllers.game_filtering_controller import get_filtered_games

game_filtering_bp = Blueprint('game_filtering', __name__, url_prefix='/games')

@game_filtering_bp.route('/filter', methods=['GET'])
def filter_games():
    """
    Endpoint to filter games.
    Query Parameters:
        - name: Keyword for game name.
        - platform: Platform to filter by.
        - required_age: Required age for filtering.
        - category: Category to filter by.
    """
    try:
        # Get query parameters
        name = request.args.get('name')
        platform = request.args.get('platform')
        required_age = request.args.get('required_age')
        category = request.args.get('category')

        # Get filtered games
        filtered_games = get_filtered_games(name, platform, required_age, category)
        return jsonify(filtered_games), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
