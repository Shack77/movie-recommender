import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    api_key = '999f031d07c56680c961874058e8978e'  # replace with your actual API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/300x450?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), key=lambda x: x[1], reverse=True)[1:6]

    recommend_movies = []
    recommend_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Use actual TMDb movie ID here
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))

    return recommend_movies, recommend_posters


movies_list = pickle.load(open('./src/movies.plk','rb'))

similarity = pickle.load(open('./src/similarity.pkl','rb'))

movies = pd.DataFrame(movies_list)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Recommendations",
    (movies['title'].values),
)


if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(len(names))
    for i in range(len(names)):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

