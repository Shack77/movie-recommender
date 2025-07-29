import numpy as np 
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

#extracting features
movies = pd.read_csv('../data/tmdb_5000_movies.csv')
credits = pd.read_csv('../data/tmdb_5000_credits.csv')

movies.head()
credits.head()
#print(movies.columns)
#print(credits.columns)
movies = pd.merge(movies,credits, on= 'title', how='inner')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'release_date', 'cast', 'crew']]
movies.dropna(inplace=True)#eliminating duplicates
#print(movies.isnull().sum())
#print(movies.duplicated().sum())


def convert(obj):
    l = []
    for i in ast.literal_eval(obj):
        l.append(i['name'])

    return l

def convert7(obj):
    l = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 7:
            l.append(i['name'])
            counter +=1
        else:
            break

    return l

def director_fetch(obj):
    l = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
            break

    return l

movies['genres'] = movies['genres'].apply(convert)
movies['keywords']= movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert7)
movies['crew'] = movies['crew'].apply(director_fetch)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']= movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies['tags'] = movies['cast'] + movies['crew'] + movies['genres'] + movies['keywords'] + movies['overview']

new_df = movies[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x:' '.join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
       y.append(ps.stem(i))

    return ' '.join(y)

new_df['tags'] = new_df['tags'].apply(stem)

#vectorising
cv = CountVectorizer(max_features = 5000, stop_words = 'english')
vectors = cv.fit_transform(new_df['tags']).toarray()

similarity = cosine_similarity(vectors)


def recomend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)),reverse = True,key = lambda x:x[1])[1:10]
    for i in movies_list:
        print(new_df.iloc[i[0]].title)

pickle.dump(new_df.to_dict(), open('movies.plk','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))
