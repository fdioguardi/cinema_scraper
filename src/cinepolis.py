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
        return driver.find_element_by_class_name("title-text").text.strip()

    def _scrape_movie(self, movie_driver):
        
        return {self._scrape_movie_title(movie_driver): {}}

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
            self._scrape_movie(driver)
        print(movies)

CinepolisScrappy(browser_executable=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe").scrape()
