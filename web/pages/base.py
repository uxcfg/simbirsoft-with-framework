import abc
from dataclasses import dataclass

from web.driver.base import BaseWebDriver


class PageLoadedError(AssertionError):
    pass


class ElementNotVisible(AssertionError):
    pass


@dataclass
class BasePage(abc.ABC):
    browser: BaseWebDriver
    url = None
    name = "Страница"

    class Elements:
        pass

    def open(self, url: str = None):
        self.browser.open(url or self.url)
        self.wait_loaded()

    @abc.abstractmethod
    def is_loaded(self):
        """Признак загрузки страницы"""
        return True

    def wait_loaded(self):
        try:
            self.is_loaded()
        except Exception as e:
            raise PageLoadedError(
                f'Страница "{self.name}" по адресу {self.url or self.browser.url} на загружена по причине: {e}'
            )
