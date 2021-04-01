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
    def _separate_movie_traits(self, traits):
        return

    def _split_string_trait(self, traits, trait, separator):
        if trait in traits.keys():
            traits[trait] = traits[trait].split(separator)
        return traits

    def _scrape_movie_traits(self, movie_container):
        return self._separate_movie_traits(
            self._collect_movie_traits(movie_container)
        )

    @abstractmethod
    def _scrape_movie_schedule(self, movie_container):
        return

    def scrape_movie(self, movie_container):
        return {
            self._scrape_movie_title(movie_container): self._normalize_movie(
                reduce(
                    lambda a, b: {**a, **b},
                    [
                        self._scrape_movie_synopsis(movie_container),
                        self._scrape_movie_traits(movie_container),
                        self._scrape_movie_schedule(movie_container),
                    ],
                )
            )
        }

    @abstractmethod
    def _normalize_movie(self, movie):
        return

    @abstractmethod
    def scrape(self):
        """Fetch movies' info in _cinema_page, return a list """

        return
