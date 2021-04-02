from abc import ABC, abstractmethod
from functools import reduce


class CinemaScrapy(ABC):
    """Abstract scraper for cinema pages

    _cinema_page (string) -- link to fetch for movies
    """

    def __init__(self, _cinema_page):
        """[summary]

        Args:
            _cinema_page ([type]): [description]
        """
        self._cinema_page = _cinema_page

    @abstractmethod
    def _scrape_movie_title(self, movie_container):
        """[summary]

        Args:
            movie_container ([type]): [description]
        """
        return

    @abstractmethod
    def _scrape_movie_synopsis(self, movie_container):
        """[summary]

        Args:
            movie_container ([type]): [description]
        """
        return

    @abstractmethod
    def _separate_movie_traits(self, traits):
        """[summary]

        Args:
            traits ([type]): [description]
        """
        return

    def _split_string_trait(self, traits, trait, separator):
        """[summary]

        Args:
            traits ([type]): [description]
            trait ([type]): [description]
            separator ([type]): [description]

        Returns:
            [type]: [description]
        """
        if trait in traits.keys():
            traits[trait] = traits[trait].split(separator)
        return traits

    def _scrape_movie_traits(self, movie_container):
        """[summary]

        Args:
            movie_container ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._separate_movie_traits(
            self._collect_movie_traits(movie_container)
        )

    @abstractmethod
    def _scrape_movie_schedule(self, movie_container):
        """This method obtains a movie's schedule

        Args:
            movie_container (any): Web container of the movie
        
        Returns:
            dict: Movie with schedule data
        """
        return

    def scrape_movie(self, movie_container):
        """This method scraps a movie page

        Args:
            movie_container (any): movie information container

        Returns:
            dict: Movie data
        """
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
        """This method normalize a movie data

        Args:
            movie (dict): A movie data
        
        Returns:
            dict: Normalized movie data
        """
        return

    @abstractmethod
    def scrape(self):
        """This method starts the scrapping of a cinema's billboard page
        
        Returns:
            dict: Movies data
        """
        return
