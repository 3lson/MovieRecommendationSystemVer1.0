from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import re
from models import db  # Import the db from models
# Other necessary imports
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Use your actual DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db instance with the app
db.init_app(app)

# Set up Flask-Migrate if you're using it
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
app.secret_key = '5728424' 
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page if not logged in

# User model

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Explicitly set the table name if necessary
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    # Assuming a Rating model exists that has a foreign key to User
    ratings = db.relationship('Rating', backref='user', lazy=True)
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

class Rating(db.Model):
    __tablename__ = 'ratings'  # Explicitly set the table name if necessary
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)  # Adjust based on your movie model
    user_rating = db.Column(db.Float, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)  # This is fine if user_id is already an integer

# Routes
@app.route('/')
def home():
    return render_template('index.html')  # Main landing page


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f"Querying for user with email: {email}")
        user = User.query.filter_by(email=email).first()
        print(f"User found: {user}")


        if user is None:
            flash('User does not exist.', 'danger')
            return redirect(url_for('login'))

        if check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required  # Ensure the user is logged in
def dashboard():
    # Assuming you have a function to get recommended movies
    recommended_movies = get_recommendations(current_user)  # Change this as needed
    
    return render_template('dashboard.html', current_user=current_user, recommendations=recommend_movies)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    
    # Query movies rated or liked by the user
    rated_movies = current_user.rated_movies
    return render_template('profile.html', user=current_user, rated_movies=rated_movies)

def get_recommendations(user):
    # Fetch user ratings, and use them to generate personalized recommendations
    user_ratings = Rating.query.filter_by(user_id=user.id).all()
    # Apply your recommendation logic here
    return recommend_movies  # Return recommended movies for the user


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
    genre_filter = request.args.get('genre_filter', '').strip()
    year_filter = request.args.get('year_filter', '').strip()

    # Debugging: print received filters
    print(f"Received genre filter: '{genre_filter}', year filter: '{year_filter}'")

    # Get recommendations based on a default movie title
    recommended_movies = recommend_movies('Star Wars')  # Change this if needed for testing

    # Now we filter recommendations based on the selected genre
    filtered_recommendations = {}
    for movie, rating in recommended_movies.items():
        movie_row = movie_data[movie_data['title'] == movie]
        if not movie_row.empty:
            genres = get_movie_genres(movie_row.iloc[0])
            print(f"Checking movie: '{movie}', Genres: {genres}, Genre Filter: '{genre_filter}'")  # Debugging
            
            if (genre_filter in genres or genre_filter == ''):
                # Check for year filter
                release_year = movie_row.iloc[0]['release_date'][:4]  # Get year from release_date
                print(f"Release year for '{movie}': {release_year}")  # Debugging

                if (year_filter == '' or year_filter == release_year):
                    filtered_recommendations[movie] = rating

    # Debugging: print filtered recommendations
    print(f"Filtered recommendations: {filtered_recommendations}")

    return render_template('index.html', recommendations=filtered_recommendations)

@app.route('/rate', methods=['POST'])
def rate_movie():
    movie_title = request.form['movie_title']
    user_rating = request.form['user_rating']
    
    print(f"Rating received for '{movie_title}': {user_rating}")  # Debugging line
    
    return render_template('index.html', message=f"Thank you for rating '{movie_title}' with {user_rating}.")

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)

