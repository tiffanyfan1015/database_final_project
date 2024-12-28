from db import get_db_connection

def get_filtered_games(name=None, platform=None, required_age=None, category=None):
    """
    Filters games based on the provided parameters.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Build the query
        query = "SELECT * FROM Game WHERE 1=1"
        params = []
        
        if name:
            query += " AND name LIKE %s"
            params.append(f"%{name}%")
        if platform:
            query += " AND platforms LIKE %s"
            params.append(f"%{platform}%")
        if required_age:
            query += " AND required_age = %s"
            params.append(required_age)
        if category:
            query += " AND category LIKE %s"
            params.append(f"%{category}%")
        
        cursor.execute(query, params)
        games = cursor.fetchall()
        return {"data": games, "status_code": 200}
    except Exception as e:
        return {"message": str(e), "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
