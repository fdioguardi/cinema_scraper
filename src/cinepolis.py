from selenium import webdriver
from cinema import CinemaScrappy


class CinepolisScrappy(CinemaScrappy):
    """Scrapper of Cinepolis's billboard"""

    def __init__(
        self,
        driver_executable="chromedriver",
        browser_executable="/usr/bin/brave",
    ):
        super().__init__(_cinema_page="http://www.villagecines.com/")
        self.browser_executable = browser_executable
        self.driver_executable = driver_executable

    def chromium_driver(self):
        options = webdriver.ChromeOptions()
        options.binary_location = self.browser_executable
        return webdriver.Chrome(
            executable_path=self.driver_executable, options=options
        )

    def _scrape_movie_title(self, driver):
        return driver.find_element_by_class_name("title-text").text.strip().upper()

    def _scrape_cinema_name(self, cinema):
        return cinema.find_element_by_class_name("btn-link").text.strip()

    def _scrape_movie_auditorium_and_schedule(self, cinema):
        data = {}
        for combination in cinema.find_elements_by_class_name("movie-showtimes-component-combination"):
            data[combination.find_element_by_class_name("text-uppercase").text.strip()] = [
                a.text for a in combination.find_elements_by_tag_name("a")]
        return data

    def _scrape_movie_schedule(self, driver):
        schedule_data = {}
        schedule_tab = driver.find_element_by_class_name(
            "movie-detail-showtimes-component")
        for cinema in schedule_tab.find_elements_by_class_name("panel-primary"):
            cinema.click()
            schedule_data[self._scrape_cinema_name(
                cinema)] = self._scrape_movie_auditorium_and_schedule(cinema)
        return { "Horarios": schedule_data}

    def _scrape_movie(self, movie_driver):
        movie_data = {}

        movie_data["Sinopsis"] = movie_driver.find_element_by_id(
            "sinopsis").text.strip()

        movie_driver.find_element_by_id("tecnicos-tab").click()

        for data in movie_driver.find_element_by_id("tecnicos").text.split("\n"):
            aux = data.split(": ")
            if aux[0] == "Actores" or aux[0] == "Género":
                movie_data[aux[0]] = aux[1].split(", ")
            else:
                movie_data[aux[0]] = aux[1]

        movie_data.update(self._scrape_movie_schedule(movie_driver))

        return {self._scrape_movie_title(movie_driver): movie_data}

    def scrape(self):
        """
        Extract information from Cinepolis' billboard
        """
        movies = {}
        driver = self.chromium_driver()
        driver.get(self._cinema_page)
        movie_container = driver.find_element_by_class_name("movie-grid")
        for movie in [m.get_attribute("href") for m in movie_container.find_elements_by_tag_name("a")]:
            driver.get(movie)
            movies.update(self._scrape_movie(driver))
        print(movies)


CinepolisScrappy(
    browser_executable=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe").scrape()
