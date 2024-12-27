import re
import json
from db import get_db_connection

def fetch_all_games():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.name, m.header_image, s.appid
        FROM Game AS s
        JOIN Media AS m ON s.appid = m.appid
    """)
    games = cursor.fetchall()

    cursor.close()
    conn.close()
    return games

def fetch_game_details(appid):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Game.name, Media.header_image, Description.detailed_description
        FROM Game
        JOIN Media ON Game.appid = Media.appid
        JOIN Description ON Game.appid = Description.appid
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

    if not game or not requirements:
        return None, None

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
