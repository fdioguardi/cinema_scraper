from abstract_cinema import CinemaScrapy
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CinepolisScrapy(CinemaScrapy):
    """Scrapper of Cinepolis's billboard

    Args:
        CinemaScrapy ([type]): [description]
    """

    def __init__(
        self,
        driver_executable="chromedriver",
        browser_executable="/usr/bin/brave",
    ):
        """[summary]

        Args:
            driver_executable (str, optional): [description]. Defaults to "chromedriver".
            browser_executable (str, optional): [description]. Defaults to "/usr/bin/brave".
        """
        super().__init__(_cinema_page="http://www.villagecines.com/")
        self.browser_executable = browser_executable
        self.driver_executable = driver_executable

    def driver(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        options = webdriver.ChromeOptions()
        options.binary_location = self.browser_executable
        return webdriver.Chrome(
            executable_path=self.driver_executable, options=options
        )

    def _scrape_movie_title(self, driver):
        """[summary]

        Args:
            driver ([type]): [description]

        Returns:
            [type]: [description]
        """
        return (
            driver.find_element_by_class_name("title-text")
            .text.strip()
            .upper()
        )

    def _scrape_cinema_name(self, cinema):
        """[summary]

        Args:
            cinema ([type]): [description]

        Returns:
            [type]: [description]
        """
        return cinema.find_element_by_class_name("btn-link").text.strip()

    def _scrape_movie_auditorium_and_schedule(self, cinema):
        """[summary]

        Args:
            cinema ([type]): [description]

        Returns:
            [type]: [description]
        """
        return {
            combination.find_element_by_class_name(
                "text-uppercase"
            ).text.strip(): [
                anchor.text for anchor in combination.find_elements_by_tag_name("a")
            ]
            for combination in cinema.find_elements_by_class_name(
                "movie-showtimes-component-combination"
            )
        }

    def _scrape_movie_schedule(self, driver):
        """[summary]

        Args:
            driver ([type]): [description]

        Returns:
            [type]: [description]
        """
        schedule_tab = driver.find_element_by_class_name(
            "movie-detail-showtimes-component"
        )

        schedule_data = {}
        for cinema in schedule_tab.find_elements_by_class_name(
            "panel-primary"
        ):
            cinema.click()
            schedule_data[
                self._scrape_cinema_name(cinema)
            ] = self._scrape_movie_auditorium_and_schedule(cinema)
        return {"Horarios": schedule_data}

    def _scrape_movie_synopsis(self, movie_driver):
        """[summary]

        Args:
            movie_driver ([type]): [description]

        Returns:
            [type]: [description]
        """
        return {
            "Sinopsis": movie_driver.find_element_by_id(
                "sinopsis"
            ).text.strip()
        }

    def _wait_for_traits(self, movie_driver, timeout=10):
        """[summary]

        Args:
            movie_driver ([type]): [description]
            timeout (int, optional): [description]. Defaults to 10.

        Returns:
            [type]: [description]
        """
        """Wait 'timeout' seconds for traits to load. Else explode"""

        return WebDriverWait(movie_driver, timeout).until(
            EC.text_to_be_present_in_element((By.ID, "tecnicos"), "Título")
        )

    def _collect_movie_traits(self, movie_driver):
        """[summary]

        Args:
            movie_driver ([type]): [description]

        Returns:
            [type]: [description]
        """
        movie_driver.find_element_by_id("tecnicos-tab").click()
        self._wait_for_traits(movie_driver)

        traits = {}
        try:
            for trait in movie_driver.find_element_by_id("tecnicos").text.split(
                "\n"
            ):
                key, value = trait.split(": ", 1)
                traits[key] = value
        except ValueError:
            pass

        return traits

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

    def _separate_movie_traits(self, traits):
        """[summary]

        Args:
            traits ([type]): [description]

        Returns:
            [type]: [description]
        """
        for trait in ["Actores", "Género"]:
            traits = self._split_string_trait(traits, trait, ", ")
        return traits

    def _normalize_movie(self, movie):
        """[summary]

        Args:
            movie ([type]): [description]

        Returns:
            [type]: [description]
        """
        if "Duración" in movie.keys():
            movie["Duración"] = movie["Duración"][:-1] + "utos"
        return movie

    def scrape(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        movies = {}
        driver = self.driver()
        driver.get(self._cinema_page)
        movie_container = driver.find_element_by_class_name("movie-grid")
        for movie in [
            anchor.get_attribute("href")
            for anchor in movie_container.find_elements_by_tag_name("a")
        ]:
            try:
                driver.get(movie)
                movies.update(self.scrape_movie(driver))
            except TimeoutException:
                pass

        return movies, "Cinepolis"
