from abstract_cinema import CinemaScrapy
from bs4 import BeautifulSoup
import requests


class CinemaLaPlataScrapy(CinemaScrapy):
    """Scraper of Cinema La Plata's billboard

    Args:
        CinemaScrapy ([type]): [description]
    """

    def __init__(self):
        """[summary]
        """
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
        """[summary]

        Args:
            movie_container ([type]): [description]

        Returns:
            [type]: [description]
        """
        return (
            movie_container.find("div", class_="page-title")
            .get_text()
            .strip()
            .upper()
        )

    def _collect_movie_traits(self, movie_container):
        """[summary]

        Args:
            movie_container ([type]): [description]

        Returns:
            [type]: [description]
        """
        return {
            trait.h4.get_text().strip(): trait.span.get_text().strip()
            for trait in movie_container.find_all(
                "div", attrs={"class": "dropcap6"}
            )
        }

    def _separate_movie_traits(self, traits):
        """[summary]

        Args:
            traits ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._split_string_trait(
            self._split_string_trait(traits, "Género", "/"), "Actores", ", "
        )

    def _scrape_movie_synopsis(self, movie_container):
        """[summary]

        Args:
            movie_container ([type]): [description]

        Returns:
            [type]: [description]
        """
        return {
            "Sinopsis": movie_container.find(id="ctl00_cph_lblSinopsis")
            .get_text()
            .strip()
        }

    def _scrape_movie_schedule(self, movie_container):
        """[summary]

        Args:
            movie_container ([type]): [description]

        Returns:
            [type]: [description]
        """
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
        """[summary]

        Args:
            movie_link ([type]): [description]

        Returns:
            [type]: [description]
        """
        return super().scrape_movie(
            self._make_soup(self._cinema_page + movie_link)
        )

    def _trim_trailing_points(self, movie):
        """[summary]

        Args:
            movie ([type]): [description]

        Returns:
            [type]: [description]
        """

        if movie["Actores"][-1][-1] == ".":
            movie["Actores"][-1] = movie["Actores"][-1][:-1]

        for trait in ["Director", "Duración"]:
            if movie[trait][-1] == ".":
                movie[trait] = movie[trait][:-1]

        return movie

    def _normalize_movie(self, movie):
        """[summary]

        Args:
            movie ([type]): [description]

        Returns:
            [type]: [description]
        """
        normalized_keys = {
            "Calificacion": "Calificación",
            "Duracion": "Duración",
        }

        for key, normalized_key in normalized_keys.items():
            movie[normalized_key] = movie.pop(key)

        return self._trim_trailing_points(movie)

    def scrape(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        movies_container = self._make_soup(
            self._cinema_page + "Cartelera.aspx"
        ).find_all("div", attrs={"class": "page-container singlepost"})

        movies = {}
        for movie in movies_container:
            movies.update(self.scrape_movie(movie.a.get("href")))

        return movies, "Cinema La Plata"
