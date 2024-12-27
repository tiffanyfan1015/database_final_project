from db import get_db_connection

def get_filtered_games(name_keyword=None, genres=None, min_price=0, max_price=float('inf'), 
                       start_date=None, end_date=None, queries=None, max_output=None):
    """
    Filters and searches games based on provided parameters, using the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # 使用字典格式方便處理
    
    query = """
        SELECT appid, name, release_date, genres, platforms, category, developer, owner_count, `2d_or_3d`
        FROM Game
        WHERE 1=1
    """
    params = []

    # Filter by name keyword
    if name_keyword:
        query += " AND name LIKE %s"
        params.append(f"%{name_keyword}%")
    
    # Filter by genres
    if genres:
        genre_conditions = " OR ".join(["genres LIKE %s"] * len(genres))
        query += f" AND ({genre_conditions})"
        params.extend([f"%{genre}%" for genre in genres])
    
    # Filter by price (假設資料表中有 `price` 欄位，否則需移除此段)
    query += " AND owner_count BETWEEN %s AND %s"
    params.extend([min_price, max_price])

    # Filter by release date
    if start_date and end_date:
        query += " AND release_date BETWEEN %s AND %s"
        params.extend([start_date, end_date])
    
    # Execute the query
    cursor.execute(query, params)
    results = cursor.fetchall()

    # Flexible search with scoring
    if queries:
        for row in results:
            row['score'] = 0  # Initialize score
            for query in queries:
                query_lower = query.lower()
                if query_lower in row['name'].lower():
                    row['score'] += 1
                if row['genres'] and query_lower in row['genres'].lower():
                    row['score'] += 1
                if row['platforms'] and query_lower in row['platforms'].lower():
                    row['score'] += 1
                if row['developer'] and query_lower in row['developer'].lower():
                    row['score'] += 1

        # Sort by score
        results = [row for row in results if row['score'] > 0]
        results.sort(key=lambda x: x['score'], reverse=True)

    # Limit the results
    if max_output:
        results = results[:max_output]

    cursor.close()
    conn.close()

    return results


if __name__ == "__main__":
    # Example usage
    filtered_games = get_filtered_games(
        name_keyword="Counter",
        genres=["Action", "Adventure"],
        min_price=0,
        max_price=1000000,
        start_date="2005-01-01",
        end_date="2015-12-31",
        queries=["Valve", "Counter"],
        max_output=10
    )
    for game in filtered_games:
        print(game)
