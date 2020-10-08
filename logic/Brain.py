from math import sqrt
from dao.MoviesDao import MoviesDao


class Brain:

    @staticmethod
    def euclidean(database, user, target):

        # FILMES EM COMUM
        common = {}

        # PERCORRE LISTA DE FILMES AVALIADOS PELO USUÁRIO
        for movie in database[user]:

            # VERIFICA SE O ALVO TAMBÉM AVALIOU ESTE FILME
            if movie in database[target]:
                # IDENTIFICA QUE ESTE FILME É COMUM ENTRE OS DOIS
                common[movie] = 1

        # SE NÃO EXISTE AVALIAÇÕES EM COMUM RETORNA
        if len(common) == 0:
            return 0

        # SOMA AS VARIÂNCIAS ENTRE AS NOTAS DO USUARIO E DO ALVO REFERENTE AO MESMO FILME ELEVADO AO QUADRADO
        sum_distance = sum([pow(database[user][item] - database[target][item], 2)
                            for item in database[user] if item in database[target]])

        # RETORNA DISTANCIA EUCLIADIANA
        return 1 / (1 + sqrt(sum_distance))

    @staticmethod
    def jaccard(item, database, data_ratings):

        result = {}

        for movie in database:

            # IGNORA SE O FILME PERCORRIDO É IGUAL AO FILME ALVO
            if movie['movieId'] == item['movieId']:
                continue

            # IGNORA SE O FILME PERCORRIDO JÁ FOI AVALIADO PELO USUÁRIO
            if any(x['movieId'] == movie['movieId'] for x in data_ratings):
                continue

            # SOMA OS GENEROS IGUAIS ENTRE O FILME PERCORRIDO E O FILEM ALVO
            similar_genres = 0

            # SOMA O TOTAL DE GENEROS ENTRE OS 2 FILMES
            sum_genres = len(item["genres"])

            # PERCORRE OS GENEROS DO FILME PERCORRIDO
            for genre in movie["genres"]:

                # VERIFICA SE O GENERO DO FILME PERCORRIDO É IGUAL AO DO FILME ALVO
                if genre in item["genres"]:
                    similar_genres += 1
                else:
                    sum_genres += 1

            # print("SIMILARIDADE ITEM " + item['title'] + " COM " + movie['title'] + " é: + str(similar_genres / sum_genres))

            # SETA O RESULTADO DA SIMILARIDADE DO FILME
            result.setdefault(movie['movieId'], 0)
            result[movie['movieId']] += similar_genres / sum_genres

        # GERA LISTA DE RECOMENDACAO
        rankings = [(total, item) for item, total in result.items()]

        # ORDENA LISTA
        rankings.sort()
        rankings.reverse()

        # RETORNA LISTA DE RECOMENDAÇÃO
        return rankings[0:2]

    @staticmethod
    def recommender_collaborative(database, user):
        total = {}
        sum_similarity = {}

        # PERCORRE A LISTA DE AVALIACOES
        for target in database:

            # SE USUARIO FOR ELE MESMO, PULA
            if target == user:
                continue

            # CALCULA SIMILARIDADE
            similarity = Brain.euclidean(database, user, target)

            # LOG
            if similarity > 0:
                print("A SIMILARIDADE DE " + user + " COM " + target + " É: " + str(similarity))

            # SE SIMILARIDADE FOR MENOR QUE 0 PULA
            if similarity <= 0:
                continue

            # PERCORRE A LISTA DE FILMES AVALIADOS PELO ALVO
            for item in database[target]:

                # VERIFICA SE O FILME JÁ NÃO FOI VISTO PELO USUÁRIO
                if item not in database[user]:
                    # CALCULA O TOTAL
                    total.setdefault(item, 0)
                    total[item] += database[target][item] * similarity

                    # CALCULA A SOMA DA SIMILARIDADE
                    sum_similarity.setdefault(item, 0)
                    sum_similarity[item] += similarity

        # GERA LISTA DE RECOMENDACAO
        rankings = [(total / sum_similarity[item], item) for item, total in total.items()]

        # ORDENA LISTA
        rankings.sort()
        rankings.reverse()

        # RETORNA LISTA DE RECOMENDAÇÃO
        return rankings[0:10]

    @staticmethod
    def recommender_content(database):

        for movie in database:
            # CARREGA DADOS DO FILME
            data_movie = MoviesDao.get_movie(movie[1])

            # CARREGA LISTA DOS FILMES QUE CONTENHAM AO MENOS UMA CATEGORIA IGUAL AO FILME EM QUESTÃO
            data_movies = MoviesDao.get_all_movies_per_genre(data_movie['genres'])

            # CARREGA AVALIACOES JÁ REALIZADAS PELO USUÁRIO
            data_ratings = MoviesDao.get_user_ratings('600')

            # REALIZA CALCULO DA SIMILARIDADE
            data_similar = Brain.jaccard(data_movie, data_movies, data_ratings)

            print(data_movie['title'] + ": " + str(movie[0]))

            # CALCULA POSSIVEL NOTA
            for item in data_similar:
                new_rating = float(movie[0]) * float(item[0])
                result_movie = MoviesDao.get_movie(item[1])

                print("=============> " + result_movie['title'] + ": " + str(new_rating))

            print()



            '''rating_a = float(MoviesDao.get_rating(data_similar[0][1])['rating'])
            rating_b = float(MoviesDao.get_rating(data_similar[1][1])['rating'])

            pred_divider = (float(data_similar[0][0]) * rating_a) + (float(data_similar[1][0]) * rating_b)
            pred_dividend = (data_similar[0][0] + data_similar[1][0])
            print("NOTA QUE DARIA PARA " + data_movie['title'] + ": " + str(pred_divider / pred_dividend))'''

            # print(data_movie['title'] + " -> " + str(data_similar))
