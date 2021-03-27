from functools import reduce


class Scrapper:
    """
    Frontend to different cinema scrapers

    @scrapies -- specialized scrapers (list)
    """

    def __init__(self):
        self.scrapies = []

    def add(self, scrapy):
        """Add a Scrappy to the list of scrapies"""
        self.scrapies.append(scrapy)

    def _difference(self, dictionary, intersection):
        return {
            key: dictionary[key]
            for key in set(dictionary.keys()).difference(intersection)
        }

    def _merge_movies(self, x, y):
        # TODO: mergear como la gente
        return dict(x, **y)

    def _merge(self, a, b):
        """Merge 2 dictionaries 'a' and 'b' containing movie data"""

        shared_movies = set(a.keys()).union(set(b.keys()))

        movies = dict(
            self._difference(a, shared_movies),
            **self._difference(b, shared_movies)
        )

        for movie in shared_movies:
            movies.update({ movie: self._merge_movies(a[movie], b[movie]) })

        return movies

    def scrape(self):
        if len(self.scrapies) < 2:
            return self.scrapies[0].scrape()

        return reduce(
            self._merge, [scrapy.scrape() for scrapy in self.scrapies]
        )


# from cinema import CinemaLaPlataScrappy

# x = Scrapper()
# x.add(CinemaLaPlataScrappy())
# x.add(CinemaLaPlataScrappy())
# print(x.scrape())
