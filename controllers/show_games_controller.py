import re
import json
from db import get_db_connection

def fetch_all_games():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT s.name, m.header_image, s.appid
        FROM Game AS s
        JOIN Media AS m ON s.appid = m.appid
    """)
    games = cursor.fetchall()

    cursor.close()
    conn.close()
    return games

def fetch_filtered_games(filters):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT Game.appid, Game.name, Media.header_image, Game.genres, Game.platforms
        FROM Game
        LEFT JOIN Media ON Game.appid = Media.appid
        WHERE 1=1
    """
    params = []
    if filters.get("genres"):
        query += " AND Game.genres LIKE %s"
        params.append(f"%{filters['genres']}%")
    if filters.get("platforms"):
        query += " AND Game.platforms LIKE %s"
        params.append(f"%{filters['platforms']}%")
    if filters.get("name"):
        query += " AND Game.name LIKE %s"
        params.append(f"%{filters['name']}%")
    cursor.execute(query, params)
    games = cursor.fetchall()
    cursor.close()
    conn.close()
    return games

def fetch_game_details(appid):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            Game.name AS game_name,
            Media.header_image AS header_image,
            Description.detailed_description AS detailed_description,
            Game.genres AS genres,
            Game.platforms AS platforms,
            Game.release_date AS release_date,
            Game.developer AS developer
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

    return game, parsed_requirements

def parse_requirements(req_string):
    if req_string and req_string != '[]':
        clean_string = req_string.replace("'", '"')
        clean_string = re.sub(r'[\r\n\t]', '', clean_string)
        try:
            return json.loads(clean_string)
        except json.JSONDecodeError as e:
            return None
    return None
