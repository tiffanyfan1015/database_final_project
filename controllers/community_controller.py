import mysql.connector # type: ignore
from db import get_db_connection
from datetime import datetime

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
    cursor.execute("SELECT * FROM PostTable WHERE group_name = %s", (group_name,))
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
