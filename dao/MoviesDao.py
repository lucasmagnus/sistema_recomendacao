from db.Connection import Connection
from datetime import datetime
from util.Util import Util


class MoviesDao:

    @staticmethod
    def get_movies(with_context):

        # COLEÇÃO DE AVALIAÇÕES
        col_ratings = Connection.db()["ratings"]

        # INICIA A BASE DE AVALIACOES
        base_ratings = {}

        for data in col_ratings.find():
            base_ratings.setdefault(data['userId'], {})

            # APLICAÇÃO DO CONTEXTO -> FILTRA AS AVALIACOES PELO CONTEXTO(SE É FIM DE SEMANA OU NÃO)
            if with_context and not Util.is_context_dayweek(datetime.fromtimestamp(float(data['timestamp'])).weekday()):
                continue

            base_ratings[data['userId']][data['movieId']] = float(data['rating'])

        return base_ratings

    @staticmethod
    def get_movie(movie_id):
        # COLEÇÃO DE FILMES
        col_movies = Connection.db()["movies"]

        return col_movies.find_one({"movieId": movie_id})

    @staticmethod
    def get_movie_api(movie_id):
        # COLEÇÃO DE FILMES
        col_movies = Connection.db()["movies"]
        data = col_movies.find_one({"movieId": movie_id})

        return {
            "movieId": data['movieId'],
            "title": data['title'],
            "genres": data['genres'],
            "year": data['year'],
        }

    @staticmethod
    def get_tags_movie(movieId):
        col_tabs = Connection.db()["tags"]
        return col_tabs.find({"movieId": movieId})

    @staticmethod
    def get_categories(movieId):
        col_tabs = Connection.db()["movies"]
        return col_tabs.find_one({"movieId": movieId})["genres"]

    @staticmethod
    def get_movie_genre(genre):
        col_movies = Connection.db()["movies"]
        return col_movies.find_one({"genres": genre})

    @staticmethod
    def get_movies_links():
        col_links = Connection.db()["links"]
        return col_links.find()

    @staticmethod
    def get_movie_link(movie_id):
        col_links = Connection.db()["links"]
        return col_links.find_one({'movieId': movie_id})

    @staticmethod
    def get_all_movies_genres():

        col_movies = Connection.db()["movies"]
        base_movies = {}

        for data in col_movies.find():
            base_movies[data['movieId']] = (data['genres'], data['year'])

        return base_movies

    @staticmethod
    def get_all_movies():

        col_movies = Connection.db()["movies"]
        return col_movies.find()

    @staticmethod
    def get_rating(movie_id):
        # COLEÇÃO DE FILMES
        col_movies = Connection.db()["ratings"]

        return col_movies.find_one({"movieId": movie_id})

    @staticmethod
    def get_all_movies_per_genre(genres):
        # COLEÇÃO DE FILMES
        col_movies = Connection.db()["movies"]

        return col_movies.find({"genres": {"$" "in": genres}})

    @staticmethod
    def get_user_ratings(user_id):
        # COLEÇÃO DE AVALIAÇÕES DO USUARIO
        col_movies = Connection.db()["ratings"]

        return col_movies.find({"userId": user_id})

    @staticmethod
    def get_tmdb_id(movieId):
        col = Connection.db()["links"]

        return col.find_one({"movieId": movieId})

    @staticmethod
    def get_tmdb_exist(tmdbId):
        col = Connection.db()["links"]

        return col.find_one({"tmdbId": tmdbId})

    @staticmethod
    def add_new_link(data):
        col = Connection.db()["links"]

        return col.insert({
                'movieId': data['movieId'],
                'tmdbId': data['tmdbId']
            })
