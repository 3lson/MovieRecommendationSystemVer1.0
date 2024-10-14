# Movie Recommendation System

## Project Overview
This **Movie Recommendation System** is designed to help users discover movies based on their preferences. By entering a movie title, users can receive personalized recommendations. The system also includes features like genre and year filtering, and users can rate movies to further refine the suggestions. This project showcases data analysis and web development skills using Python and Flask.

## Tools and Technologies Used
- **Flask**: A lightweight web framework in Python that made it easy to build and deploy the application.
- **HTML/CSS**: Used to create a simple, clean front-end interface.
- **Bootstrap**: Helped in making the application responsive and visually appealing with minimal effort.
- **Jinja2**: A Python templating engine that integrates with Flask for rendering dynamic HTML content.
- **Pandas**: A powerful data manipulation library in Python used to handle the movie dataset and filter user preferences.

## Dataset
The project utilizes the **MovieLens 100k dataset**, which contains 100,000 ratings from 943 users across 1,682 movies. The dataset is broken down into the following files:
- **u.data**: Contains user ratings (user ID, movie ID, rating, and timestamp).
- **u.item**: Provides movie information like title, release date, and genre.
- **u.genre**: Lists all the possible genres.
- **u.user**: Holds demographic information about the users.

### Advantages of the Dataset
- **Comprehensive Data**: It provides detailed user ratings and a wide range of movie genres, which are useful for generating nuanced recommendations.
- **User Variety**: The dataset includes ratings from a diverse group of users, making it ideal for collaborative filtering techniques.
- **Well-Supported**: The MovieLens dataset is widely used in research and projects, so there is plenty of documentation and community support available.

### Disadvantages of the Dataset
- **Sparsity**: Not every user has rated every movie, so there can be gaps in the data which can lead to less accurate recommendations.
- **Limited Audience**: The dataset only includes ratings from a specific group, which might not represent broader viewing preferences.
- **Outdated**: Since the dataset covers a specific time period, it might not reflect more recent movie trends or newer titles.

## What I Learned
Throughout the development of this project, I gained several key insights:

- **Data Handling**: I learned how critical it is to properly clean, filter, and organize data when building recommendation systems. Handling missing values, categorizing genres, and managing user ratings required careful attention to detail.
- **Building a Web Application**: This was a great opportunity to deepen my understanding of Flask and how to integrate back-end logic with front-end templates. Flask’s simplicity made it easy to focus on core features while still delivering a functional product.
- **User Experience Matters**: I learned that creating a smooth and responsive user interface can make or break the success of an application. Implementing Bootstrap helped me quickly design a clean and user-friendly interface.
- **Filtering by Genre and Year**: Adding these filtering options gave users more control over their recommendations, which greatly improved the flexibility and usefulness of the app.
- **Collaboration Challenges**: I faced challenges with designing the recommendation system, especially when dealing with collaborative filtering methods. The experience taught me the importance of balancing user input and data analysis to create a more refined system.

## Initial Challenges
At first, the recommendation system was only based on user ratings, which limited its effectiveness. When users wanted more control over recommendations—such as filtering by genre or release year—I had to extend the functionality to accommodate those preferences. The project then evolved into something more dynamic and user-focused.

### Current Features
- **User Input**: Users can type in a movie title to get recommendations.
- **Genre Filtering**: Users can select specific genres to narrow down the recommendations.
- **Year Filtering**: Users can filter movies based on their release year.
- **Movie Rating**: Users can rate the movies they have seen, which will help refine future recommendations.
- **Responsive Design**: The application is fully responsive, ensuring a seamless experience on both desktops and mobile devices.

### User Authentication Issues
There are known issues with the user authentication feature, particularly with registration and login. We are working to resolve these bugs in future updates. Stay tuned for improvements, or check the issues section for ongoing discussions.

## Future Improvements
The project is a solid start, but there’s always room for enhancement:

- **Advanced Recommendation Algorithms**: I plan to implement more sophisticated algorithms, like collaborative filtering or content-based filtering, to improve the accuracy of recommendations.
- **User Accounts**: Adding user accounts will allow users to save their ratings and preferences for more personalized suggestions.
- **Additional Movie Information**: Incorporating movie descriptions, trailers, and other details will help users make more informed decisions.
- **Search Functionality**: I want to add a full search feature so users can find specific movies instead of relying only on recommendations.

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
