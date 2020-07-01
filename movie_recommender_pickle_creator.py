import pandas as pd
import os
from sklearn.decomposition import NMF
import numpy as np
import pickle

def get_movie_title(movie_id):
    """
    Input: movieId (int)
    gets movieTitle from the DataFrame movies, given the movieId
    """
    movieTitle = movies[movies.movieId == movie_id]["title"].values[0]
    return movieTitle

## Read in data
print("Reading in data..")
movies = pd.read_csv("flask_app/ml-latest-small/movies.csv")
ratings = pd.read_csv("flask_app/ml-latest-small/ratings.csv")
links = pd.read_csv("flask_app/ml-latest-small/links.csv")

ratings = ratings.drop("timestamp", 1)
ratings.rating.astype('int')

### Matrix
print("Creating matrix...")
rating_matrix = pd.pivot_table(ratings, values="rating", index="userId", columns="movieId")
mean_rating = rating_matrix.mean().mean()
rating_matrix = rating_matrix.fillna(np.round(mean_rating, 1))

### Useful stuff
print("Creating lists to map movie-ids with movie titles...")
dic_id_title ={}
for i in rating_matrix:
    dic_id_title[i] = get_movie_title(i)

dic_title_id = {}
for i in range(len(movies)):
    dic_title_id[ movies[["movieId", "title"]].iloc[i].title    ] =  movies[["movieId", "title"]].iloc[i].movieId

movies_list = movies.title.sort_values()

### NMF
print("Fitting NMF model...")
nmf = NMF(n_components=30)
nmf.fit(rating_matrix)
P = nmf.transform(rating_matrix)  # user-genre matrix
Q = nmf.components_   # movie-genre matrix
Rhat = np.dot(P,Q)  # reconstructed matrix
predictions = pd.DataFrame(Rhat, columns=rating_matrix.columns, index=rating_matrix.index)
predictions_columns = predictions.columns
predictions_mean = round(predictions.mean().mean(), 2)

### Create pickle files
print("Creating pickle files...")
pickle.dump( nmf, open( "flask_app/pickle_files/nmf_100.p", "wb" ) )
pickle.dump( P, open( "flask_app/pickle_files/p.p", "wb" ) )
pickle.dump( Q, open( "flask_app/pickle_files/q.p", "wb" ) )
# pickle.dump( predictions, open("pickle_files/predictions.p", "wb"))
pickle.dump( predictions_columns, open("flask_app/pickle_files/predictions_columns.p", "wb"))
pickle.dump( predictions_mean, open("flask_app/pickle_files/predictions_mean.p", "wb"))
pickle.dump( dic_id_title, open("flask_app/pickle_files/dic_id_title.p", "wb"))
pickle.dump( dic_title_id, open("flask_app/pickle_files/dic_title_id.p", "wb"))
pickle.dump( movies_list, open( "flask_app/pickle_files/movies_list.p", "wb" ) )
pickle.dump( links, open( "flask_app/pickle_files/movies_links.p", "wb" ) )

print("reconstruction_error:", nmf.reconstruction_err_)
