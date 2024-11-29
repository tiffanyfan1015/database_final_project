from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests

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
        FROM steams AS s
        JOIN steam_media_data AS m ON s.appid = m.steam_appid
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
        SELECT steams.name, steam_media_data.header_image, steam_description_data.detailed_description
        FROM steams
        JOIN steam_media_data ON steams.appid = steam_media_data.steam_appid
        JOIN steam_description_data ON steams.appid = steam_description_data.steam_appid
        WHERE steams.appid = %s;
    """, (appid,))
    game = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not game:
        return "Game not found!", 404

    return render_template('detail.html', game=game)

if __name__ == '__main__':
    app.run(debug=True)