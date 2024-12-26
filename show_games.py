from flask import Flask, render_template
import mysql.connector
import os
import json
import re

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv("DB_USERS"),
        password=os.getenv("DB_PASSWORD"),
        database="steams"
    )
    return conn

@app.route("/")
def menu():
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.name, m.header_image, s.appid
        FROM Steam AS s
        JOIN Media AS m ON s.appid = m.appid
    """)
    
    games = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template("index.html", games=games)

@app.route('/game/<int:appid>')
def game_details(appid):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Steam.name, Media.header_image, Description.detailed_description
        FROM Steam
        JOIN Media ON Steam.appid = Media.appid
        JOIN Description ON Steam.appid = Description.appid
        WHERE Steam.appid = %s;
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
    
    def parse_requirements(req_string):
        if req_string and req_string != '[]':
            clean_string = req_string.replace("'", '"')
            clean_string = re.sub(r'[\r\n\t]', '', clean_string)
            try:
                return json.loads(clean_string)
            except json.JSONDecodeError as e:
                return None
        return None

    parsed_requirements = {
        "pc": parse_requirements(requirements[0]),
        "mac": parse_requirements(requirements[1]),
        "linux": parse_requirements(requirements[2]),
    }

    return render_template(
        'detail.html',
        game=game,
        requirements=parsed_requirements
    )
if __name__ == '__main__':
    app.run(debug=True)