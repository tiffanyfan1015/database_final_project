# import pandas as pd
# from datetime import datetime
# import pytz

# # Load the dataset
# folder_path = '/content/drive/Shareddrives/Me and only me/DBMS_Data'
# file_path = folder_path + '/steam.csv'
# df = pd.read_csv(file_path)

# def get_filtered_games(name_keyword, genres, min_price, max_price, start_date, end_date, queries, max_output):
#     """
#     Filters and searches games based on provided parameters.
#     """
#     # Filter games
#     filtered_df = df.copy()
    
#     # Filter by name
#     if name_keyword:
#         filtered_df = filtered_df[filtered_df['name'].str.contains(name_keyword, case=False, na=False)]
    
#     # Filter by genres
#     if genres:
#         filtered_df = filtered_df[filtered_df['genres'].apply(lambda x: any(genre in x for genre in genres) if pd.notna(x) else False)]
    
#     # Filter by price
#     filtered_df = filtered_df[(filtered_df['price'] >= min_price) & (filtered_df['price'] <= max_price)]
    
#     # Filter by release date
#     if start_date and end_date:
#         filtered_df['release_date'] = pd.to_datetime(filtered_df['release_date'], errors='coerce')
#         filtered_df = filtered_df[(filtered_df['release_date'] >= pd.to_datetime(start_date)) & 
#                                   (filtered_df['release_date'] <= pd.to_datetime(end_date))]
    
#     # Flexible search with scoring
#     filtered_df['score'] = 0
#     if queries:
#         for query in queries:
#             try:
#                 date_query = pd.to_datetime(query)
#                 filtered_df['score'] += filtered_df['release_date'].eq(date_query).astype(int)
#             except ValueError:
#                 query_lower = query.lower()
#                 filtered_df['score'] += (
#                     filtered_df['name'].str.contains(query_lower, case=False, na=False) |
#                     filtered_df['genres'].str.contains(query_lower, case=False, na=False) |
#                     filtered_df['platforms'].str.contains(query_lower, case=False, na=False) |
#                     filtered_df['developer'].str.contains(query_lower, case=False, na=False) |
#                     filtered_df['publisher'].str.contains(query_lower, case=False, na=False)
#                 ).astype(int)
    
#     # Sort by score and limit output
#     filtered_df = filtered_df[filtered_df['score'] > 0].sort_values(by='score', ascending=False).drop(columns=['score'])
#     if max_output:
#         filtered_df = filtered_df.head(max_output)
    
#     return filtered_df.to_dict(orient='records')
