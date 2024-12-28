from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
from show_games import get_db_connection

app = Flask(__name__)

# Load data from the database
def load_data():
    conn = get_db_connection()
    query = """
        SELECT s.appid, s.name, s.price, s.genres, s.release_date, s.platforms, 
               s.developer, s.publisher, s.language, s.age_requirement, s.categories
        FROM Steam AS s
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Filter games
def filter_games(df, platforms=None, age_requirements=None, categories=None):
    filtered_df = df.copy()

    if platforms:
        filtered_df = filtered_df[filtered_df['platforms'].apply(lambda x: any(platform in x for platform in platforms) if pd.notna(x) else False)]

    if age_requirements:
        filtered_df = filtered_df[filtered_df['age_requirement'].apply(lambda x: x in age_requirements if pd.notna(x) else False)]

    if categories:
        filtered_df = filtered_df[filtered_df['categories'].apply(lambda x: any(category in x for category in categories) if pd.notna(x) else False)]

    return filtered_df

# Flexible search with scoring
def flexible_search(filtered_df, queries=None, max_output=None):
    filtered_df['score'] = 0
    if queries:
        if isinstance(queries, str):
            queries = [queries]
        filtered_df['release_date'] = pd.to_datetime(filtered_df['release_date'], errors='coerce')
        for query in queries:
            try:
                date_query = pd.to_datetime(query)
                filtered_df['score'] += filtered_df['release_date'].eq(date_query).astype(int)
            except ValueError:
                query_lower = query.lower()
                filtered_df['score'] += (
                    filtered_df['name'].str.contains(query_lower, case=False, na=False) |
                    filtered_df['genres'].str.contains(query_lower, case=False, na=False) |
                    filtered_df['platforms'].str.contains(query_lower, case=False, na=False) |
                    filtered_df['developer'].str.contains(query_lower, case=False, na=False) |
                    filtered_df['publisher'].str.contains(query_lower, case=False, na=False) |
                    filtered_df['categories'].str.contains(query_lower, case=False, na=False)
                ).astype(int)
    matched_df = filtered_df[filtered_df['score'] > 0].sort_values(by='score', ascending=False).drop(columns=['score'])
    if max_output is not None:
        unmatched_df = filtered_df[~filtered_df.index.isin(matched_df.index)].drop(columns=['score'])
        combined_df = pd.concat([matched_df, unmatched_df], ignore_index=True).head(max_output)
    else:
        combined_df = matched_df
    return combined_df

@app.route("/filter", methods=["POST"])
def filter_route():
    languages = request.form.getlist("languages")
    platforms = request.form.getlist("platforms")
    age_requirements = request.form.getlist("age_requirements")
    genres = request.form.getlist("genres")
    categories = request.form.getlist("categories")

    # Load data from the database
    df = load_data()

    # Apply filters
    filtered_games = filter_games(
        df,
        languages=languages,
        platforms=platforms,
        age_requirements=age_requirements,
        genres=genres,
        categories=categories
    )

    if filtered_games.empty:
        return render_template("filter_results.html", games=[], message="No games match the filter criteria.")
    return render_template("filter_results.html", games=filtered_games.to_dict(orient="records"))

@app.route("/search", methods=["POST"])
def search_route():
    queries = request.form.get("queries")
    if not queries:
        return render_template("search_results.html", games=[], message="No search queries provided.")
    queries = queries.split(",")
    max_output = int(request.form.get("max_output", 15))

    # Load data from the database
    df = load_data()

    # Perform flexible search
    search_results = flexible_search(df, queries=queries, max_output=max_output)

    if search_results.empty:
        return render_template("search_results.html", games=[], message="No games match the search criteria.")
    return render_template("search_results.html", games=search_results.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)