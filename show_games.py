from flask import Flask, render_template
from flask_caching import Cache
import mysql.connector
import os
import json
import re
from db import get_db_connection

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)

@app.route("/")
def menu():
    
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
    
    return render_template("games_index.html", games=games)

@app.route('/game/<int:appid>')
def game_details(appid):
    @cache.memoize(timeout=300)
    def get_game_details(appid):
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

        cursor.execute("""
            SELECT app_name, review_score, review_votes
            FROM SteamReview
            WHERE appid = %s
            LIMIT 5;
        """, (appid,))
        reviews = cursor.fetchall()
        reviews = [list(review) for review in reviews]

        if reviews[0][2] == -1:
            reviews[0][2] = 1

        cursor.close()
        conn.close()

        if not game:
            return None, "Game not found!", 404
        if not requirements:
            return None, "Not found!", 404

        def parse_requirements(req_string):
            if req_string and req_string != '[]':
                clean_string = req_string.replace("'", '"')
                clean_string = re.sub(r'[\r\n\t]', '', clean_string)
                try:
                    return json.loads(clean_string)
                except json.JSONDecodeError:
                    return None
            return None

        parsed_requirements = {
            "pc": parse_requirements(requirements[0]),
            "mac": parse_requirements(requirements[1]),
            "linux": parse_requirements(requirements[2]),
        }

        return {
            "game": game,
            "requirements": parsed_requirements,
            "reviews": reviews
        }, None, None

    data, error_message, error_status = get_game_details(appid)

    if error_message:
        return error_message, error_status

    return render_template(
        'games_detail.html',
        game=data["game"],
        requirements=data["requirements"],
        reviews=data["reviews"]
    )
if __name__ == '__main__':
    app.run(debug=True)