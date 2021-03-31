from abstract_cinema import CinemaScrappy
from bs4 import BeautifulSoup
import requests


class CinemaLaPlataScrappy(CinemaScrappy):
    """Scrapper of Cinema La Plata's billboard"""

    def __init__(self):
        super().__init__(_cinema_page="http://www.cinemalaplata.com/")

    def _make_soup(self, link):
        """Prepare a nutritious soup to begin scrapping

        Args:
            link (string): url for the page to make the beatifulsoup object

        Returns:
            BeatifulSoup: HTML form page to scrap
        """

        return BeautifulSoup(requests.get(link).text, "html.parser")

    def _scrape_movie_title(self, movie_container):
        return (
            movie_container.find("div", class_="page-title")
            .get_text()
            .strip()
            .upper()
        )

    def _scrape_movie_traits(self, movie_container):
        return {
            trait.h4.get_text().strip(): trait.span.get_text().strip()
            for trait in movie_container.find_all(
                "div", attrs={"class": "dropcap6"}
            )
        }

    def _scrape_movie_synopsis(self, movie_container):
        return {
            "Sinopsis": movie_container.find(id="ctl00_cph_lblSinopsis")
            .get_text()
            .strip()
        }

    def _scrape_movie_schedule(self, movie_container):
        schedule_container = movie_container.find(
            "div", attrs={"id": "ctl00_cph_pnFunciones"}
        )

        return {
            schedule_container.h4.get_text().strip(): {
                cinema.span.get_text()
                .strip(): cinema.p.get_text()
                .strip()
                .split("\n")
                for cinema in schedule_container.find_all(
                    "div", attrs={"class": "col-2"}
                )
            }
        }

    def scrape_movie(self, movie_link):
        movie_container = self._make_soup(self._cinema_page + movie_link)
        super.scrape_movie(movie_container)

    def scrape(self):
        """
        Extract information from Cinema La Plata's billboard
        """
        movies_container = self._make_soup(
            self._cinema_page + "Cartelera.aspx"
        ).find_all("div", attrs={"class": "page-container singlepost"})

        movies = {}
        for movie in movies_container:
            movies.update(self.scrape_movie(movie.a.get("href")))
        return movies
