from functools import reduce
from json import dump
from cinema import CinemaLaPlataScrappy
from cinepolis import CinepolisScrappy


class Scrapper:
    def __init__(self):
        self.scrapies = [
            CinemaLaPlataScrappy(),
            CinepolisScrappy(),
        ]

    def _difference(self, dictionary, intersection):
        return {
            key: dictionary[key]
            for key in set(dictionary.keys()).difference(intersection)
        }

    def _merge_keys(self, movie, shared_keys, a_movie, b_movie):
        for key in ["Actores", "Género"]:
            if key in shared_keys:
                movie[key] = list(set(a_movie[key] + b_movie[key]))
                shared_keys.remove(key)

        if "Horarios" in shared_keys:
            movie["Horarios"] = {**a_movie["Horarios"], **b_movie["Horarios"]}
            shared_keys.remove("Horarios")
        return movie, shared_keys

    def _merge_movies(self, a_movie, a_source, b_movie, b_source):

        shared_keys = set(a_movie.keys()).intersection(set(b_movie.keys()))

        movie, shared_keys = self._merge_keys(
            dict(
                self._difference(a_movie, shared_keys),
                **self._difference(b_movie, shared_keys)
            ),
            shared_keys,
            a_movie,
            b_movie,
        )

        a_data = {}
        b_data = {}

        for key in shared_keys:
            if a_movie[key] == b_movie[key]:
                movie[key] = a_movie[key]
            else:
                a_data[key] = a_movie[key]
                b_data[key] = b_movie[key]

        if a_data:
            movie[a_source] = a_data
            movie[b_source] = b_data

        return movie

    def _merge(self, a, b):
        """a and b are tuples. First element are movies, second is source of
        info. Merge movies from a and b"""

        a_movies, a_source = a
        b_movies, b_source = b

        shared_movies = set(a_movies.keys()).intersection(set(b_movies.keys()))

        movies = dict(
            self._difference(a_movies, shared_movies),
            **self._difference(b_movies, shared_movies)
        )

        for movie in shared_movies:
            movies.update(
                {
                    movie: self._merge_movies(
                        a_movies[movie], a_source, b_movies[movie], b_source
                    )
                }
            )

        return movies

    def scrape(self, path="../data/movies.json"):
        with open(path, "w") as file:
            dump(
                self._merge(
                    *map(lambda scrapy: scrapy.scrape(), self.scrapies)
                ),
                file,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
            )
