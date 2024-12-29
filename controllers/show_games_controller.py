import re
import json
from db import get_db_connection



def fetch_filtered_games(filters):
    """
    Combines filtering and search functionality to fetch games.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Base query
        query = """
            SELECT Game.appid, Game.name, Game.platforms, Game.category, Game.required_age,
                   Media.header_image, Game.developer, Game.publisher
            FROM Game
            LEFT JOIN Media ON Game.appid = Media.appid
            WHERE 1=1
        """
        params = []

        # Add filtering logic
        if filters.get("platforms"):
            query += " AND Game.platforms LIKE %s"
            params.append(f"%{filters['platforms']}%")
        if filters.get("age"):
            query += " AND Game.required_age = %s"
            params.append(filters["age"])
        if filters.get("categories"):
            query += " AND Game.category LIKE %s"
            params.append(f"%{filters['categories']}%")

        # Add flexible search logic
        if filters.get("search"):
            search = filters["search"]
            query += """
                AND (
                    Game.name LIKE %s OR
                    Game.developer LIKE %s OR
                    Game.publisher LIKE %s OR
                    Game.category LIKE %s
                )
            """
            params.extend([f"%{search}%"] * 4)

        cursor.execute(query, params)
        games = cursor.fetchall()
        return games
    except Exception as e:
        print(f"Error fetching filtered/searched games: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def fetch_game_details(appid):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        Game.name AS game_name,
        Media.header_image AS header_image,
        Description.detailed_description AS detailed_description,
        Game.platforms AS platforms,
        Game.release_date AS release_date,
        Game.developer AS developer,
        Game.publisher AS publisher,
        Game.required_age AS required_age
    FROM Game
    LEFT JOIN Media ON Game.appid = Media.appid
    LEFT JOIN Description ON Game.appid = Description.appid
    WHERE Game.appid = %s;
""", (appid,))

    game = cursor.fetchone()

    cursor.execute("""
        SELECT pc_requirements, mac_requirements, linux_requirements
        FROM Requirements
        WHERE appid = %s;
    """, (appid,))
    requirements = cursor.fetchone()

    cursor.execute("""
        SELECT review_text
        FROM SteamReview
        WHERE appid = %s
        LIMIT 5;
    """, (appid,))
    texts = cursor.fetchall()
    review_text = []

    for text in texts: 
        review_text.append(text[0])
    
    cursor.execute("""
        SELECT AVG(review_score), SUM(review_votes)
        FROM SteamReview
        WHERE appid = %s
    """, (appid,))

    review = cursor.fetchone()
    
    cursor.execute("""
        SELECT username, comment AS text, created_at
        FROM Comments
        WHERE appid = %s
        ORDER BY created_at DESC;
    """, (appid,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    if not game:
        return "Game not found!", 404
    if not requirements:
        return "Not found !", 404

    parsed_requirements = {
        "pc": parse_requirements(requirements[0]),
        "mac": parse_requirements(requirements[1]),
        "linux": parse_requirements(requirements[2]),
    }

    reviews = {
        "review_text": review_text,
        "review_score": review[0],
        "review_vote": review[1],
    }

    return game, parsed_requirements, reviews, comments

def parse_requirements(req_string):
    if req_string and req_string != '[]':
        clean_string = req_string.replace("'", '"')
        clean_string = re.sub(r'[\r\n\t]', '', clean_string)
        try:
            return json.loads(clean_string)
        except json.JSONDecodeError as e:
            return None
    return None