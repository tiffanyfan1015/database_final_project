from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import ast
import json

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
        SELECT s.name, m.header_image, s.appid, r.pc_requirements
        FROM steams AS s
        JOIN steam_media_data AS m ON s.appid = m.steam_appid
        LEFT JOIN steam_requirement AS r ON s.appid = r.appid
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
        SELECT steams.name, steam_media_data.header_image, 
               steam_description_data.short_description,
               steam_requirement.pc_requirements,
               steam_requirement.mac_requirements,
               steam_requirement.linux_requirements
        FROM steams
        JOIN steam_media_data ON steams.appid = steam_media_data.steam_appid
        JOIN steam_description_data ON steams.appid = steam_description_data.steam_appid
        JOIN steam_requirement ON steams.appid = steam_requirement.appid
        WHERE steams.appid = %s;
    """, (appid,))

    game = cursor.fetchone()

    if not game:
        return "Game not found!", 404

    def clean_and_parse(req_string):
        if req_string:
            try:
                cleaned = req_string.replace("'", '"').replace("\r\n", "").strip()
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return {"minimum": "Invalid data", "recommended": "Invalid data"}
        return {}

    pc_requirements = clean_and_parse(game[3])
    mac_requirements = clean_and_parse(game[4])
    linux_requirements = clean_and_parse(game[5])

    game = list(game[:3]) + [pc_requirements, mac_requirements, linux_requirements]

    cursor.close()
    conn.close()

    return render_template('detail.html', game=game)

if __name__ == '__main__':
    app.run(debug=True)