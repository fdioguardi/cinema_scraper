from functools import reduce
from cinema import CinemaLaPlataScrappy
from cinepolis import CinepolisScrappy


class Scrapper:
    """
    Frontend to different cinema scrapers

    @scrapies -- specialized scrapers (list)
    """

    def __init__(self):
        self.scrapies = []

    def add(self, *args):
        """Add a Scrappy to the list of scrapies"""
        for scrapy in args:
            self.scrapies.append(scrapy)

        return self

    @classmethod
    def setup(cls):
        return cls().add(CinemaLaPlataScrappy(), CinepolisScrappy())

    def _difference(self, dictionary, intersection):
        return {
            key: dictionary[key]
            for key in set(dictionary.keys()).difference(intersection)
        }

    def _merge_movies(self, a_movie, a_source, b_movie, b_source):

        shared_keys = set(a_movie.keys()).intersection(set(b_movie.keys()))

        movie = dict(
            self._difference(a_movie, shared_keys),
            **self._difference(b_movie, shared_keys)
        )

        a_data = {}
        b_data = {}

        for key in shared_keys:
            if a_movie[key] == b_movie[key]:
                movie[key] = a_movie[key]
            else:
                a_data[key] = a_movie[key]
                b_data[key] = b_movie[key]

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

    def scrape(self):
        if len(self.scrapies) < 2:
            return self.scrapies[0].scrape()

        return reduce(
            self._merge, [scrapy.scrape() for scrapy in self.scrapies]
        )


print(Scrapper.setup().scrape())
