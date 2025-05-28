import pickle
import requests
import pandas as pd
import streamlit as st
import io
import gdown


try:
    movie_df = pd.read_pickle('movies.pkl')
    movie_list = movie_df['title'].values
    movie_ids = movie_df['movie_id'].values
except Exception as e:
    st.error(f"Error loading movie list: {e}")
    st.stop()

# Load movie list and similarity matrix with error handling
@st.cache_data(show_spinner="Downloading similarity matrix...")
def load_similarity():
    url = "https://drive.google.com/uc?id=1b_vub9X7pjen0iv7pYx7LNIHnpFnWJ9U"
    output = "similarity.pkl"
    gdown.download(url, output, quiet=False)
    with open(output, "rb") as f:
        similarity_matrix = pickle.load(f)
    return similarity_matrix

similarity = load_similarity()

if similarity is None:
    st.error("Failed to load similarity matrix.")
    st.stop()
# Additional Styling
st.markdown("""
    <style>
        .stApp{
            background-color: #d0dbe5;
        }
        body {
            background-color: #ffffff;
            color: #333333;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #ff7043;
            color: white;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #e64a19;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        .stSelectbox>div>div>div>input {
            background-color: #e0e0e0;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            font-size: 16px;
            padding: 8px;
        }
        .stImage {
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stColumns>div {
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    header [data-testid="stHeader"] a[href*="github.com"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Fetch poster, rating, and overview
def fetch_movie_details(movie_id):
    try:
        # API request to get movie details
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d436409403751bdc95a94ea50929d45d')
        data = response.json()

        # Extract poster URL, rating, and overview
        poster_url = 'https://image.tmdb.org/t/p/w154/' + data['poster_path']
        rating = data.get('vote_average', 'N/A')  # If rating is unavailable, show 'N/A'
        overview = data.get('overview', 'Overview not available')  # If overview is unavailable, show a default message

        return poster_url, rating, overview
    except Exception as e:
        st.error(f"Error fetching movie details: {e}")
        return None, None, None



# Movie recommendation function
def recommend(movie, num_recommendations):
    try:
        movie_index = list(movie_list).index(movie)
    except ValueError:
        return [], [], [], []  # Return empty lists if movie is not found

    distance = similarity[movie_index]
    m_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[
             1:num_recommendations + 1]  # Get top 'num_recommendations'
    recommended_movies = []
    rm_posters = []
    ratings = []
    overviews = []
    for i in m_list:
        movie_id = movie_ids[i[0]]
        poster_url, rating, overview = fetch_movie_details(movie_id)
        recommended_movies.append(movie_list[i[0]])
        rm_posters.append(poster_url)
        ratings.append(rating)
        overviews.append(overview)
    return recommended_movies, rm_posters, ratings, overviews


# Streamlit app UI
st.title('Movies Recommender System')

# User selects a movie from the dropdown
option = st.selectbox('Select a movie', movie_list)

# User selects the number of recommendations
num_recommendations = st.selectbox(
    'How many recommendations do you want?',
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Options for the number of recommendations
    index=4  # Default value (in this case, 5)
)

# Session state to hold movie details that are clicked
if 'clicked_movie' not in st.session_state:
    st.session_state.clicked_movie = None
    st.session_state.clicked_movie_details = {}

# Button to get recommendations
if st.button('Recommend'):
    with st.spinner('Fetching recommendations...'):
        recommended_movies, posters, ratings, overviews = recommend(option, num_recommendations)
        if recommended_movies and posters:
            # Display recommendations in a flexible grid (multiple rows if needed)
            items_per_row = 4
            num_rows = (num_recommendations + items_per_row - 1) // items_per_row  # Calculate number of rows

            # Loop through rows
            for row in range(num_rows):
                start = row * items_per_row
                end = min((row + 1) * items_per_row, num_recommendations)
                columns = st.columns(items_per_row)  # Create columns for this row

                # Loop through the recommendations for this row
                for i in range(start, end):
                    with columns[i - start]:
                        st.write("##### " + recommended_movies[i])
                        # Show the poster with updated `use_container_width`
                        if st.image(posters[i], width=150, use_container_width=True, caption='## ' + recommended_movies[i]):
                            # Store clicked movie in session state
                            if st.session_state.clicked_movie == recommended_movies[i]:
                                st.session_state.clicked_movie_details = {
                                    "rating": ratings[i],
                                    "overview": overviews[i]
                                }
                            else:

                                st.session_state.clicked_movie = recommended_movies[i]
                                st.session_state.clicked_movie_details = {}
st.set_page_config(
    page_title="Your App Title",  # Change to your app's title
                  
    layout="wide",                # Or "centered"
    initial_sidebar_state="collapsed",  # Optional: auto-collapse sidebar
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "Made with ❤️ using Streamlit"  # You can change this or set to None
    }
)
                        

                        # Show movie details if the movie was clicked
                        if st.session_state.clicked_movie == recommended_movies[i]:
                            st.write(f"**Rating**: {ratings[i]}")  # Display rating
                            st.write(f"**Overview**: {overviews[i]}")  # Display overview


        else:
            st.write("Movie not found. Please try again.")

