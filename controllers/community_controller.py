import mysql.connector # type: ignore
from db import get_db_connection
from datetime import datetime
from flask import session

def handle_group(group_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM `Groups` WHERE group_name = %s", (group_name,))
    group = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if group:
        return True, group['group_name'] 
    else:
        return False, None


def get_community_by_group_id(group_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `Groups` WHERE group_name = %s", (group_name,))
    community = cursor.fetchone()
    cursor.close()
    conn.close()
    return community

def get_posts_by_group_id(group_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT PostTable.*, Game.name AS game_name, Media.header_image
        FROM PostTable
        LEFT JOIN Game ON PostTable.appid = Game.appid
        LEFT JOIN Media ON Game.appid = Media.appid
        WHERE PostTable.group_name = %s
        ORDER BY PostTable.timestamp DESC
    """
    cursor.execute(query, (group_name,))
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts


def add_message_to_chat(group_name, user_name, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO GroupChatTable (group_name, user_name, message, timestamp) VALUES (%s, %s, %s, %s)",
        (group_name, user_name, message, time_stamp)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_chat_by_group_name(group_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT user_name, message, timestamp FROM GroupChatTable WHERE group_name = %s ORDER BY timestamp ASC",
        (group_name,)
    )
    chats = cursor.fetchall()
    cursor.close()
    conn.close()
    return chats


def search_game_by_name(game_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT Game.appid, Game.name, Media.header_image
        FROM Game
        LEFT JOIN Media ON Game.appid = Media.appid
        WHERE Game.name LIKE %s
    """
    cursor.execute(query, (f"%{game_name}%",))
    games = cursor.fetchall()
    cursor.close()
    conn.close()
    return games

def add_post_to_community(group_name, post_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO PostTable (group_name, user_name, tag, appid, content, timestamp)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """
    try:
        cursor.execute(query, (
            group_name,
            post_data['user_name'],
            post_data['post_type'],
            post_data['appid'],
            post_data['content']
        ))
        conn.commit()
    except Exception as e:
        print(f"Error inserting post: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

