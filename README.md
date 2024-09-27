# Movie Recommendation System

## Project Overview
This project is a **Movie Recommendation System** designed to help users discover movies based on their preferences. Users can input a movie title to receive personalized recommendations, with additional features like genre filtering and user ratings. The project demonstrates the application of data analysis and web development skills using Python and Flask.

## Tools Used
- **Flask**: A micro web framework for Python that allows for easy and efficient web application development.
- **HTML/CSS**: Used for front-end development to create a responsive and user-friendly interface.
- **Bootstrap**: A popular front-end framework that facilitates responsive design and quick prototyping.
- **Jinja2**: A templating engine for Python that integrates with Flask to dynamically generate HTML content.
- **Pandas**: A data manipulation library for Python used to handle and analyze the dataset effectively.

## Dataset
The dataset used for this project is the **MovieLens 100k dataset**, which contains 100,000 ratings from 943 users on 1,682 movies. The dataset includes the following files:
- **u.data**: Contains user ratings, including user ID, movie ID, rating, and timestamp.
- **u.item**: Contains movie information, including movie ID, title, release date, and genre.
- **u.genre**: Contains a list of genres.
- **u.user**: Contains user demographic information.

### Advantages of the Dataset
- **Rich Information**: The dataset provides detailed user ratings and associated movie genres, allowing for nuanced recommendations.
- **Diversity of Data**: With ratings from various users, the dataset offers a range of opinions on each movie, making it ideal for collaborative filtering approaches.
- **Well-Documented**: The dataset is widely used in academic research and projects, making it easy to find resources and documentation for implementation.

### Disadvantages of the Dataset
- **Sparsity**: The dataset is relatively sparse, meaning that not all users have rated all movies. This can lead to challenges in generating accurate recommendations.
- **Limited Scope**: The dataset only includes ratings from a specific group of users, which may not represent broader trends or preferences in movie watching.
- **Temporal Bias**: Since the dataset covers ratings over a specific period, it may not reflect current viewing trends or the popularity of newer movies.

## Learning Objectives
Throughout the development of this project, I learned about:
- The importance of data handling and the impact of user ratings on recommendations.
- How to implement genre-based filtering to improve recommendation accuracy.
- Building a web application using Flask and integrating it with HTML/CSS for a user-friendly interface.

## Initial Challenges
Initially, the recommendation system was solely based on user ratings. However, I encountered limitations when users wanted recommendations based solely on specific genres. This led to the addition of a genre filtering feature to cater to diverse user preferences.

### Current Features
- **User Input**: Users can input a movie title to get recommendations.
- **Genre Filtering**: Users can filter recommendations by selecting specific genres.
- **Year Filtering**: Users can filter recommendations based on the release year.
- **Rating System**: Users can rate the movies they have seen, which will influence future recommendations.
- **Responsive Design**: The application features a modern and sleek interface built with Bootstrap.

## Future Improvements
- **Enhanced Recommendation Algorithms**: Implement more sophisticated recommendation algorithms (e.g., collaborative filtering) to provide better suggestions.
- **User Accounts**: Allow users to create accounts to save their ratings and preferences for a more personalized experience.
- **Movie Descriptions**: Include descriptions and trailers for each movie in the recommendations to help users make informed choices.
- **Search Functionality**: Implement a search feature to find movies directly instead of relying solely on recommendations.

## Installation
To run the application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. Create a virtual environment 
```bash
python -m venv venv
```

3. Active the virtual environment 
```bash
source venv/bin/activate
```

4.Install the required dependencies
```bash
pip install -r requirements.txt
```

5. Run the Flask application 
```bash
flask run
```

6. Access the application in your browser at `http://127.0.0.1:5000`

## Usage
Once the application is running, you can:

Enter a movie title in the search box to get recommendations.
Apply genre or year filters to refine the recommendations.
Rate movies to improve future recommendations.

## Contributing
If you would like to contribute to this project, feel free to fork the repository and submit a pull request. You can also open an issue if you encounter any problems or have suggestions for improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.