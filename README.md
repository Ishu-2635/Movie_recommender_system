# 🎬 Movie_recommender_system
---

This is an interactive Movie Recommender System built with **Python**, **Streamlit**, and **The Movie Database (TMDb) API**. It recommends movies based on content similarity and displays key details like posters, ratings, and overviews.

---

## 🚀 Features

- Select a movie and get up to 10 similar recommendations.
- Uses precomputed cosine similarity matrix.
- Fetches movie posters, ratings, and overviews using TMDb API.
- Responsive grid layout with interactive UI.
- Built with Streamlit and styled with custom HTML/CSS.

---

## 🧠 How It Works

1. Movie similarity is computed offline using a content-based filtering model.
2. When a user selects a movie:
   - It finds the most similar movies using cosine similarity.
   - For each recommended movie, it fetches:
     - Poster image
     - TMDb rating
     - Movie overview

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Pickle
- Requests
- TMDb API
- HTML/CSS (for Streamlit customization)

---

## 📁 Project Structure
├── app.py # Streamlit main app
├── movies.pkl # Pickled DataFrame with movie titles and IDs
├── similarity.pkl # Pickled similarity matrix (cosine similarities)
├── README.md #Project documentation


