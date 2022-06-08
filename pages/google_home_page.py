from web.driver.web_element import Element
from web.pages.base import BasePage


class GoogleHomePage(BasePage):
    url = "https://google.com"

    class Elements:
        search_input = Element("//input[@aria-label='Найти']")
        submit_btn = Element("//div[@jsname]//input[@name='btnK']")

    def is_loaded(self):
        Element("//body")
        return True

    def fill_search_input(self, value):
        self.Elements.search_input.fill(value)

    def click_on_search_btn(self):
        self.Elements.submit_btn.click()
