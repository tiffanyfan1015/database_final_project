import hashlib
from db import get_db_connection

def get_groups():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `Groups`")
        groups = cursor.fetchall()
        return {"data": groups, "status_code": 200}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_group_by_id(group_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `Groups` WHERE group_name = %s", (group_name,))
        group = cursor.fetchone()
        if group:
            return {"data": group, "status_code": 200}
        else:
            return {"message": "Group not found", "status_code": 404}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def create_group(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO `Groups` (group_name, group_info)
            VALUES (%s, %s)
        """
        cursor.execute(query,(data["group_name"], data["group_info"]))
        conn.commit()

        return {"message": "Group create successfully", "status_code": 201}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def update_group(group_name, group_info):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE `Groups` SET group_info = %s WHERE group_name = %s"
        cursor.execute(query, (group_info, group_name))
        conn.commit()
        return {"message": "Group updated successfully", "status_code": 200}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def delete_group(group_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM `Groups` WHERE group_name = %s"
        cursor.execute(query, (group_name,))
        conn.commit()
        return {"message": "Group deleted successfully", "status_code": 200}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
