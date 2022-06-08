# Инициализатор страниц(page объектов)
# Каждую новую страницу нужно будет обязательно тут проинициализировать

from web.driver.base import BaseWebDriver
from pages.google_home_page import GoogleHomePage
from pages.google_calculator_page import GoogleCalculatorPage


class Pages:
    browser: BaseWebDriver
    google_home_page: GoogleHomePage
    google_calculator_page: GoogleCalculatorPage

    @classmethod
    def init(cls, browser: BaseWebDriver):
        cls.browser = browser
        cls.google_home_page = GoogleHomePage(browser)
        cls.google_calculator_page = GoogleCalculatorPage(browser)


pages = Pages()
