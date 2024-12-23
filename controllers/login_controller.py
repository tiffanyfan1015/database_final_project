import hashlib
from db import get_db_connection
from flask import session

def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users")
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
        cursor.execute("SELECT * FROM Users WHERE username = %s", (user_id,))
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
            INSERT INTO Users (username, password)
            VALUES (%s, %s)
        """
        password = data["password"]
        password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(query,(data["username"], password))
        conn.commit()
        return {"message": "Signup successful. Please Login.", "status_code": 201}
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
        query = "UPDATE Users SET password = %s WHERE username = %s"
        password = data["password"]
        password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute(query, (password,user_id))
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
        query = "DELETE FROM Users WHERE username = %s"
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
        query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        password = data["password"]
        password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute(query, (data["username"], password))
        user = cursor.fetchone()
        if user:
            session['username'] = user['username']
            return {"message": "Login successful", "status_code": 200}
        else:
            return {"message": "Invalid username or password", "status_code": 401}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def logout():
    session.clear()
    return {"message": "Logout successful", "status_code": 200}