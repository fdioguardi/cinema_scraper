from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests


class CinemaScrappy(ABC):
    """Abstract scrapper for cinema pages

    _cinema_page (string) -- link to fetch for movies
    """

    def __init__(self, _cinema_page):
        self._cinema_page = _cinema_page

    def _make_soup(self, link):
        """Prepare a nutritious soup to begin scrapping

        Args:
            link (string): url for the page to make the beatifulsoup object

        Returns:
            BeatifulSoup: HTML form page to scrap
        """

        return BeautifulSoup(requests.get(link).text, "html.parser")

    @abstractmethod
    def scrape(self):
        """Fetch movies' info in _cinema_page, return a list """

        return


class CinemaLaPlataScrappy(CinemaScrappy):
    """Scrapper of Cinema La Plata's billboard"""

    def __init__(self):
        super().__init__(_cinema_page="http://www.cinemalaplata.com/")

    def _scrape_movie_title(self, movie_container):
        return (
            movie_container.find("div", class_="page-title").get_text().strip()
        )

    def _scrape_movie_traits(self, movie_container):
        return {
            trait.find("h4")
            .get_text()
            .strip(): trait.find("span")
            .get_text()
            .strip()
            for trait in movie_container.find_all(
                "div", attrs={"class": "dropcap6"}
            )
        }

    def _scrape_movie_schedule(self, movie_container):
        # {
        #   movie 1 = {
        #     horarios = {
        #       cine 1 =
        #       cine 2 =
        #       cine 3 =
        #     }
        #   }
        # }

        schedule_container = movie_container.find(
            "div", attrs={"id": "ctl00_cph_pnFunciones"}
        )

        # movie_schedule_children = movie_schedule.findChildren()
        # movie_data[movie_schedule_children[0].get_text().strip()] = {}
        # del movie_schedule_children[0]
        # for schedule in movie_schedule_children:
        #     pass
        horarios = {
            cinema.find("span")
            .get_text()
            .strip(): cinema.find("p")
            .get_text()
            .strip()
            .split(r"\n")
            for cinema in movie_container.find_all(
                "div", attrs={"class": "col-2"}
            )
        }

        return {schedule_container.find("h4").get_text().strip(): horarios}

    def _scrape_movie(self, movie_link):
        # Tomamos los datos de la pelicula
        movie_container = self._make_soup(self._cinema_page + movie_link)

        movie = self._scrape_movie_traits(movie_container)

        movie["Sinopsis"] = (
            movie_container.find(id="ctl00_cph_lblSinopsis").get_text().strip()
        )

        movie.update(self._scrape_movie_schedule(movie_container))

        return {self._scrape_movie_title(movie_container): movie}

    def scrape(self):
        """
        Extract information from Cinema La Plata's billboard
        """
        movies_container = self._make_soup(
            self._cinema_page + "Cartelera.aspx"
        ).find_all("div", attrs={"class": "page-container singlepost"})

        movies = {}
        for movie in movies_container:
            movies.update(self._scrape_movie(movie.find("a").get("href")))
            print(movies)
            return 0
        return movies


CinemaLaPlataScrappy().scrape()
