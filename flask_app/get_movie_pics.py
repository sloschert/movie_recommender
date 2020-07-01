import pickle
import requests

def get_pic_link(movie_titles):
    """
    Input:
    List of movie titles (list)
    Output:
    List with Url-links to picture, using https://www.omdbapi.com/ API
    """

    # turn movie titles into movie Ids:
    dic_title_id = pickle.load(open("flask_app/pickle_files/dic_title_id.p", "rb"))
    movie_Ids = []
    for i in movie_titles:
        movie_Ids.append(dic_title_id[i])

    links = pickle.load(open("flask_app/pickle_files/movies_links.p", "rb"))
    links = links[["movieId", "imdbId"]]

    poster_list = []
    for i in movie_Ids:
        imdbid = links[links["movieId"]==i]["imdbId"].values[0]
        imdbid = str(imdbid).zfill(7)
        pic_link = f"http://www.omdbapi.com/?i=tt{imdbid}&apikey=aa89b36d"
        r = requests.get(pic_link)
        poster = r.json()["Poster"]
        poster_list.append(poster)

    return poster_list
