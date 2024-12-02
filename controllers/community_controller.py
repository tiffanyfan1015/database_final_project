# controllers/community_controller.py

from db import get_db_connection

# 獲取社區的詳細資料
def get_community(group_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `group` WHERE group_id = %s", (group_id,))
        community = cursor.fetchone()
        return community
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 獲取特定社區的帖子
def get_posts(group_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM post_table WHERE group_id = %s", (group_id,))
        posts = cursor.fetchall()
        return posts
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
