from flask import Flask, request, render_template
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import re

app = Flask(__name__)

# Load the ratings dataset
ratings = pd.read_csv('ml-100k/u1.base', sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])
ratings['rating'] = pd.to_numeric(ratings['rating'], errors='coerce')

# Load the movies dataset
movies = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', header=None)

# Load genres mapping
genres_mapping = pd.read_csv('ml-100k/u.genre', sep='|', header=None)
genres_mapping.columns = ['genre_id', 'genre_name']

# Create a genre dictionary for easy access
genre_dict = genres_mapping.set_index('genre_name')['genre_id'].to_dict()

# Create the movie dataframe with correct columns
num_genres = len(genres_mapping)
genre_column_names = [f'genre_{i + 1}' for i in range(num_genres)]
movies.columns = ['item_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL'] + genre_column_names

# Merge ratings with movie titles and genre columns
movie_data = pd.merge(ratings, movies[['item_id', 'title', 'release_date'] + genre_column_names], on='item_id')

# Debugging: Print the columns to check for 'release_date'
print("Columns in movie_data DataFrame:", movie_data.columns)

# Create a user-item matrix
user_item_matrix = movie_data.pivot_table(index='user_id', columns='item_id', values='rating').fillna(0)

# Compute cosine similarity between users
user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

def clean_title(title):
    title = re.sub(r'\s+', ' ', title).strip()
    title = re.sub(r'\s*\(\d{4}\)\s*', '', title)
    return title.lower()

def get_movie_genres(movie_row):
    """Get genres for a given movie row."""
    genres = []
    for col in genre_column_names:
        if movie_row[col] == 1:  # Check if the genre is present (1)
            genre_index = int(col.split('_')[1])  # Get genre index from column name
            genre_name = genre_dict.get(genre_index, None)  # Get genre name
            if genre_name:
                genres.append(genre_name)  # Append the genre name if found
            else:
                print(f"Warning: Genre ID {genre_index} not found in genre_dict.")  # Debugging info
    return genres

def recommend_movies(user_favorite_movie):
    recommendations_dict = {}
    cleaned_input_title = clean_title(user_favorite_movie)
    movie_data['cleaned_title'] = movie_data['title'].apply(clean_title)

    if cleaned_input_title not in movie_data['cleaned_title'].values:
        recommendations_dict["error"] = "Movie not found. Please try a different title."
        return recommendations_dict

    selected_movie_row = movie_data[movie_data['cleaned_title'] == cleaned_input_title]

    if selected_movie_row.empty:
        recommendations_dict["error"] = "Selected movie not found. Please try a different title."
        return recommendations_dict

    selected_movie_row = selected_movie_row.iloc[0]
    genres = get_movie_genres(selected_movie_row)

    # Debugging: print the genres for the selected movie
    print("Selected movie genres:", genres)

    if not genres:
        recommendations_dict["error"] = "No genres found for the selected movie."
        return recommendations_dict

    user_id = selected_movie_row['user_id']
    similar_users = user_similarity_df[user_id].nlargest(10).index
    recommendations = movie_data[movie_data['user_id'].isin(similar_users)]

    # Filter recommendations based on the genres of the selected movie
    recommendations['genre_filter'] = recommendations[genre_column_names].any(axis=1)
    recommendations = recommendations[recommendations['genre_filter']]

    recommendations['rating'] = pd.to_numeric(recommendations['rating'], errors='coerce')
    recommendations = recommendations[recommendations['rating'].notnull()]

    recommended_movies = recommendations.groupby('title')['rating'].mean().sort_values(ascending=False).head(10)

    if recommended_movies.empty:
        recommendations_dict["error"] = "No recommendations available for this movie."
        return recommendations_dict

    recommendations_dict = recommended_movies.to_dict()
    return recommendations_dict

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['movie_title']
    recommended = recommend_movies(user_input)
    return render_template('index.html', recommendations=recommended)

@app.route('/filter', methods=['GET'])
def filter_recommendations():
    genre_filter = request.args.get('genre_filter', '')
    year_filter = request.args.get('year_filter', '')

    # Get recommendations based on a default movie title
    recommended_movies = recommend_movies('Star Wars')  # Use "Star Wars" or a valid title for testing

    # Now we filter recommendations based on the selected genre
    filtered_recommendations = {}
    for movie, rating in recommended_movies.items():
        movie_row = movie_data[movie_data['title'] == movie]
        if not movie_row.empty:
            genres = get_movie_genres(movie_row.iloc[0])
            print(f"Checking movie: {movie}, Genres: {genres}, Genre Filter: {genre_filter}")  # Debug statement
            
            if (genre_filter in genres) or (genre_filter == ''):
                filtered_recommendations[movie] = rating

    # If a year filter is applied, further refine the recommendations
    if year_filter:
        filtered_recommendations = {
            k: v for k, v in filtered_recommendations.items()
            if any(movie_data.loc[movie_data['title'] == k, 'release_date'].astype(str).str.contains(year_filter))
        }

    return render_template('index.html', recommendations=filtered_recommendations)

@app.route('/rate', methods=['POST'])
def rate_movie():
    movie_title = request.form['movie_title']
    user_rating = request.form['user_rating']
    
    print(f"Rating received for '{movie_title}': {user_rating}")  # Debugging line
    
    return render_template('index.html', message=f"Thank you for rating '{movie_title}' with {user_rating}.")

if __name__ == '__main__':
    app.run(debug=True)
