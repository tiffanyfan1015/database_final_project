import hashlib
from db import get_db_connection

def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return {"data": users, "status_code": 200}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return {"data": user, "status_code": 200}
        else:
            return {"message": "User not found", "status_code": 404}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def add_user(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        """
        cursor.execute(query,(data["username"], data["password"]))
        conn.commit()
        return {"message": "User added successfully", "status_code": 201}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def update_user(user_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(query, (data.get("password"),user_id))
        conn.commit()
        return {"message": "User updated successfully", "status_code": 200}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE username = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        return {"message": "User deleted successfully", "status_code": 200}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def login(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (data["username"], data["password"]))
        user = cursor.fetchone()
        if user:
            return {"message": "Login successful", "user": user, "status_code": 200}
        else:
            return {"message": "Invalid username or password", "status_code": 401}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()