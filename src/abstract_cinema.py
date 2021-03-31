from abc import ABC, abstractmethod
from functools import reduce


class CinemaScrappy(ABC):
    """Abstract scrapper for cinema pages

    _cinema_page (string) -- link to fetch for movies
    """

    def __init__(self, _cinema_page):
        self._cinema_page = _cinema_page

    @abstractmethod
    def _scrape_movie_title(self, movie_container):
        return

    @abstractmethod
    def _scrape_movie_synopsis(self, movie_container):
        return

    @abstractmethod
    def _scrape_movie_traits(self, movie_container):
        return

    @abstractmethod
    def _scrape_movie_schedule(self, movie_container):
        return

    def scrape_movie(self, movie_container):
        return {
            self._scrape_movie_title(movie_container): reduce(
                lambda a, b: {**a, **b},
                [
                    self._scrape_movie_synopsis(movie_container),
                    self._scrape_movie_traits(movie_container),
                    self._scrape_movie_schedule(movie_container),
                ],
            )
        }

    @abstractmethod
    def scrape(self):
        """Fetch movies' info in _cinema_page, return a list """

        return
