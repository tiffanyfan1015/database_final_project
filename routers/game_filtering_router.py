# from flask import Blueprint, request, jsonify
# from controllers.game_filtering_controller import get_filtered_games

# game_filtering_bp = Blueprint('game_filtering', __name__, url_prefix='/games')

# @game_filtering_bp.route('/filter', methods=['GET'])
# def filter_games():
#     """
#     Endpoint to filter and search games.
#     Query Parameters:
#         - name_keyword: Keyword to search in game names.
#         - genres: Comma-separated list of genres (e.g., Action,Adventure).
#         - min_price: Minimum price of games.
#         - max_price: Maximum price of games.
#         - start_date: Start of the release date range (YYYY-MM-DD).
#         - end_date: End of the release date range (YYYY-MM-DD).
#         - queries: Comma-separated list of search terms for flexible search.
#         - max_output: Maximum number of games to return.
#     """
#     try:
#         params = request.args
#         name_keyword = params.get('name_keyword')
#         genres = params.get('genres')
#         if genres:
#             genres = genres.split(',')
#         min_price = float(params.get('min_price', 0))
#         max_price = float(params.get('max_price', 100))
#         start_date = params.get('start_date')
#         end_date = params.get('end_date')
#         queries = params.get('queries')
#         if queries:
#             queries = queries.split(',')
#         max_output = int(params.get('max_output', 15))
        
#         # Get filtered games
#         filtered_games = get_filtered_games(name_keyword, genres, min_price, max_price, start_date, end_date, queries, max_output)
#         return jsonify(filtered_games), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400
