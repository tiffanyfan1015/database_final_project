import mysql.connector # type: ignore
from db import get_db_connection
from datetime import datetime

def handle_group(group_id):
    # 連接到資料庫
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 查詢群組是否存在
    cursor.execute("SELECT * FROM `groups` WHERE group_id = %s", (group_id,))
    group = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if group:
        return True, group['group_name']  # 群組存在，返回群組名稱
    else:
        return False, None  # 群組不存在，返回 None


def create_group(group_id):
    # 連接到資料庫
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 創建新的群組
    group_name = str(group_id)  # 根據你的需求設定群組名稱
    cursor.execute("INSERT INTO `groups` (group_id, group_name) VALUES (%s, %s)", (group_id, group_name))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_community_by_group_id(group_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `groups` WHERE group_id = %s", (group_id,))
    community = cursor.fetchone()  # 只取一個結果
    cursor.close()
    conn.close()
    return community

def get_posts_by_group_id(group_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM post_table WHERE group_id = %s", (group_id,))
    posts = cursor.fetchall()  # 取得多個結果
    cursor.close()
    conn.close()
    return posts

def get_chat_by_group(group_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM group_chat WHERE group_id = %s ORDER BY time_stamp", (group_id,))
    chats = cursor.fetchall()
    cursor.close()
    conn.close()
    return chats

def send_message_to_chat(group_id, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO group_chat (group_id, message_, time_stamp) VALUES (%s, %s, %s)",
        (group_id, message, time_stamp)
    )
    conn.commit()
    cursor.close()
    conn.close()
