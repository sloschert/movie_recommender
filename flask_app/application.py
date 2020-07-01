import pandas as pd
import pickle
from flask import Flask, render_template, request
from flask_app import recommender
from flask_app import get_movie_pics

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/movies')
def movies():
    num = 3
    movies_list = list(pickle.load(open("flask_app/pickle_files/movies_list.p", "rb" ) ))
    return render_template('movies.html', num_html=num, movies_list=movies_list)

@app.route('/results')
def results():
    dic_title_id = pickle.load( open("flask_app/pickle_files/dic_title_id.p", "rb"))
    user_input = dict(request.args)
    user_movies = list(user_input.values())[::2]
    user_ratings = list(user_input.values())[1::2]
    movies_list = recommender.nmf(user_movies, user_ratings)
    recommended_pics = get_movie_pics.get_pic_link(movies_list)

    return render_template('results.html', movies_html = movies_list, user_movies=user_movies, user_ratings=user_ratings, \
    recommended_pics=recommended_pics)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__== '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
