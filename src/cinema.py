from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests

class Movie:
    """A movie..."""

    # def __init__(self, properties):
    #     self.title = properties[title]
    #     self.genre = genre
    #     self.language = language
    #     self.origin = origin
    #     self.web = web
    #     self.duration = duration
    #     self.director = director
    #     self.rating = rating
    #     self.cast = cast
    #     self.synopsis = synopsis
    #     self.schedule = schedule


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
    def scrap(self):
        """Fetch movies' info in _cinema_page, return a list """

        return


class CinemaLaPlataScrappy(CinemaScrappy):
    """Scrapper of Cinema La Plata's billboard"""

    def __init__(self):        
        super().__init__(_cinema_page="http://www.cinemalaplata.com/")

    def _scrape_movie(self, movie_link):
        # Declaracion de un diccionario vacio con los datos de una pelicula
        movie_data = {}
        
        # Tomamos los datos de la pelicula
        movie_container = self._make_soup(self._cinema_page + movie_link)
        movie_data["title"] = movie_container.find(id="ctl00_pnTitu").get_text().strip()
        for data in movie_container.find_all("div", attrs={"class":"dropcap6"}):
            movie_data[data.contents[1].get_text().strip()] = data.contents[3].get_text().strip()
        
        # Tomamos horario y cine donde esta la pelicula
        movie_schedule = movie_container.find("div", attrs={"id":"ctl00_cph_pnFunciones"})
        movie_schedule_children = movie_schedule.findChildren()
        movie_data[movie_schedule_children[0].get_text().strip()] = {}
        del movie_schedule_children[0]
        for schedule in movie_schedule_children:
            pass
        return movie_data

    def scrap(self):
        """
        Method that extracts the information of the Cinemas La Plata billboard
        """        
        movies_container = self._make_soup(
            self._cinema_page + "Cartelera.aspx"
        ).find_all("div", attrs={"class": "page-container singlepost"})
        movies_info = {}
        for movie in movies_container:
            movie_info = self._scrape_movie(movie.find("a").get("href"))
            movies_info[movie_info["title"]] = movie_info

CinemaLaPlataScrappy().scrap()
