from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests


class CinemaScrappy(ABC):
    """Abstract scrapper for cinema pages

    _cinema_page (sting) -- link to fetch for movies
    """

    def __init__(self, _cinema_page: str = None) -> None:
        self._cinema_page = _cinema_page

    def _make_soup(self, link: str) -> BeautifulSoup:
        """Prepare a nutritious soup to begin scrapping"""

        return BeautifulSoup(requests.get(link).text, "html.parser")

    @abstractmethod
    def scrap(self) -> dict:
        return

class CinemaLaPlataScrappy(CinemaScrappy):
    """Scrapper of Cinema La Plata's billboard"""

    def __init__(self):
        super().__init__(_cinema_page="http://www.cinemalaplata.com/")


    def _scrape_movie(self, movie: Tag) -> BeautifulSoup:
        movie_data = self._make_soup(
            self._cinema_page + movie.find("a").get("href")
        ).find_all("div", attrs={"class": "page-container singlepost"})


    def scrap(self):
        movies = self._make_soup(
            self._cinema_page + "Cartelera.aspx"
        ).find_all("div", attrs={"class": "page-container singlepost"})

        for movie in movies:
            # self._scrape_movie(movie)
            pass

class Movie():
    """A movie..."""
    pass
# x = CinemaLaPlataScrappy().scrap()
