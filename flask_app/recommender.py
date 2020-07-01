import numpy as np
import pickle
import pandas as pd

def nmf(films, ratings):
    """
    takes 2 arguments, films and ratings (both lists)
    returns a list with the best recommendations
    """

    def top_films(new_prediction, k):
        """
        calculates a list of the k highest rated films in the predicted array.
        returns a list with movieIds of these k highest rated movies, minus the ones rated by the user.
        """

        top_films = list(new_prediction.iloc[0].nlargest(k).index)
        #  get rid of already watched movies
        for i in films:
            if dic_title_id[i] in top_films:
                top_films.remove(dic_title_id[i])
        return top_films

    def get_movie_title2(movieId):
        """
        returns movie title from movieId
        """
        movieTitle = dic_id_title[movieId]
        return movieTitle

    nmf = pickle.load( open( "flask_app/pickle_files/nmf_100.p", "rb" ) )
    P = pickle.load( open( "flask_app/pickle_files/p.p", "rb" ) )
    Q = pickle.load( open( "flask_app/pickle_files/q.p", "rb" ) )
    dic_id_title = pickle.load( open("flask_app/pickle_files/dic_id_title.p", "rb"))
    dic_title_id = pickle.load( open("flask_app/pickle_files/dic_title_id.p", "rb"))
    predictions_mean = pickle.load( open("flask_app/pickle_files/predictions_mean.p", "rb"))
    predictions_columns = pickle.load( open("flask_app/pickle_files/predictions_columns.p", "rb"))

    ratings = np.array(ratings)
    ratings = ratings.astype('float')
    query = np.zeros(len(predictions_columns))

    count = 0
    for i in films:
        query[list(predictions_columns).index(dic_title_id[i])] = ratings[count]
        count += 1
    query = query.reshape(-1,1).T

    new_p = nmf.transform(query)
    new_prediction = np.dot(new_p,Q)
    new_prediction = pd.DataFrame(new_prediction, columns=predictions_columns)

    top_films_list = top_films(new_prediction, 10)
    top_films_list_names = []
    for i in top_films_list:
        top_films_list_names.append(get_movie_title2(i))

    return top_films_list_names
