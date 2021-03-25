from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from typing import Any

class Movie:
    """A movie..."""

    def __init__(self, properties: dict[str, Any]) -> None:

        self.title = properties[title]
        self.genre = genre
        self.language = language
        self.origin = origin
        self.web = web
        self.duration = duration
        self.director = director
        self.rating = rating
        self.cast = cast
        self.synopsis = synopsis
        self.schedule = schedule


class CinemaScrappy(ABC):
    """Abstract scrapper for cinema pages

    _cinema_page (sting) -- link to fetch for movies
    """

    def __init__(self, _cinema_page: str) -> None:
        self._cinema_page = _cinema_page

    def _make_soup(self, link: str) -> BeautifulSoup:
        """Prepare a nutritious soup to begin scrapping"""

        return BeautifulSoup(requests.get(link).text, "html.parser")

    @abstractmethod
    def scrap(self) -> list[Movie]:
        """Fetch movies' info in _cinema_page, return a list """

        return


class CinemaLaPlataScrappy(CinemaScrappy):
    """Scrapper of Cinema La Plata's billboard"""

    def __init__(self) -> None:
        super().__init__(_cinema_page="http://www.cinemalaplata.com/")

    def _scrape_movie(self, movie_link: Tag) -> BeautifulSoup:
        movie_container = self._make_soup(
            self._cinema_page + movie_link.find("a").get("href")
        ).div(class="page-container singlepost")

        movie_data = {}
        for data in movie_container:
            #llenamos movie_data
            pass

        return Movie().setup(movie_data)

        # for movie_data in movie_soup.find_all("div", attrs={"class": "dropcap6"}):
        #     print( movie_data.find("span").get_text() )

    def scrap(self) -> list[Movie]:
        movies_container = self._make_soup(
            self._cinema_page + "Cartelera.aspx"
        ).find_all("div", attrs={"class": "page-container singlepost"})

        for movie in movies_container:
            self._scrape_movie(movie)

CinemaLaPlataScrappy().scrap()
