import abc
import time
from dataclasses import dataclass
from typing import Union

from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    TimeoutException,
    InvalidElementStateException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement as WebDriverElement
from selenium.webdriver.support.wait import WebDriverWait
from web.driver.exceptions import (
    ElementNotFound,
    ElementNotVisible,
    ElementStillVisible,
    ElementNotClickable,
    ElementNotInteractable,
    ElementAttributeError,
    ElementStillInteractable,
)
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class BaseElement(abc.ABC):
    name: str
    xpath: Union[None, str] = None
    wait_time: int = None

    def __str__(self):
        return self.xpath

    def __getitem__(self, item):
        self.xpath = f"({self.xpath})[{item}]"
        return self

    def join(self, path):
        self.xpath = f"{self.xpath}{path}"
        return self


class WebElement(BaseElement):
    def __post_init__(self):
        self.xpath = self.xpath or f"//*[normalize-space(.)='{self.name}']"

    def _init(self):
        from register import pages

        self.browser = pages.browser
        self.wait_time = self.wait_time or self.browser.wait_time

    @property
    def web_element(self) -> WebDriverElement:
        self._init()

        for attempt in range(self.wait_time):
            try:
                return self.browser.driver.find_element(By.XPATH, self.xpath)
            except NoSuchElementException:
                if attempt + 1 == self.wait_time:
                    raise ElementNotFound(f"Элемент: {self} не найден в течение {self.wait_time} сек")
                time.sleep(1)

    @property
    def text(self):
        self._init()
        return self.web_element.text

    def attr(self, value):
        self._init()
        return self.web_element.get_attribute(value)

    def click(self):
        """
        Иногда необходим скролл, когда шапка перекрывает текущий элемент
        """
        self._init()
        self.wait_visible()
        end_time = time.time() + self.browser.wait_time
        error = None
        scroll_up = True
        scroll_size = 100
        while time.time() < end_time:
            try:
                ActionChains(self.browser.driver).move_to_element(self.web_element).perform()
                time.sleep(0.1)
                return self.web_element.click()
            except WebDriverException as e:
                error = e
                if scroll_up and not isinstance(error, TimeoutException):
                    self.browser.scroll_up(scroll_size)
                    scroll_up = False

        raise ElementNotClickable(error)

    def fill(self, value, slowly=False):
        self._init()
        self.wait_visible()
        self.wait_enabled()
        try:
            self.web_element.clear()
            if slowly:
                for v in value:
                    self.web_element.send_keys(v)
                return value
            self.web_element.send_keys(value)
        except InvalidElementStateException as e:
            raise ElementNotInteractable(f"Элемент {self} не доступен для ввода. {e}")
        return value

    def upload_file(self, path):
        self._init()
        self.web_element.send_keys(path)
        return path

    def check_value(self, value):
        self._init()
        element_value = self.web_element.get_attribute("value")
        assert element_value == value, f"Значение `{element_value}` не сопадало с ожидаемым `{value}`"

    def wait_visible(self, wait_time=None):
        self._init()
        wait_time = wait_time or self.wait_time
        try:
            WebDriverWait(self.browser.driver, wait_time, ignored_exceptions=(StaleElementReferenceException,)).until(
                lambda driver: self.visible
            )
            return self
        except TimeoutException:
            raise ElementNotVisible(f"Элемент: {self} не отображен в течение {self.wait_time} сек")

    def wait_enabled(self):
        self._init()
        try:
            WebDriverWait(
                self.browser.driver, self.wait_time, ignored_exceptions=(StaleElementReferenceException,)
            ).until(lambda driver: self.web_element.is_enabled())
            return self
        except TimeoutException:
            raise ElementNotInteractable(f"Элемент: {self} не активен в течение {self.wait_time} сек")

    @property
    def visible(self):
        return self.web_element.is_displayed()

    def is_exists(self, wait_time=5):
        self._init()
        wait_time_before = self.wait_time
        self.wait_time = wait_time
        self.browser.wait_time = wait_time
        try:
            result = self.web_element
        except ElementNotFound:
            result = False
        self.wait_time = wait_time_before
        self.browser.wait_time = wait_time_before
        return result

    def wait_not_visible(self):
        self._init()
        try:
            WebDriverWait(self.browser.driver, self.wait_time).until_not(
                lambda driver: driver.find_element(By.XPATH, self.xpath).is_displayed()
            )
            return True
        except TimeoutException:
            raise ElementStillVisible(f"Элемент: {self} отображается спустя {self.wait_time} сек")
        except NoSuchElementException:
            return True

    def clear(self):
        self.web_element.clear()

    def press_keys(self, keys):
        self._init()
        self.wait_visible()

        for key in keys:
            ActionChains(self.browser.driver).key_down(key, self.web_element).key_up(key, self.web_element).perform()
            time.sleep(0.01)

    def wait_disabled(self):
        self._init()
        try:
            WebDriverWait(self.browser.driver, self.wait_time).until(lambda driver: not self.web_element.is_enabled())
            return self
        except TimeoutException as e:
            raise ElementStillInteractable(f"Элемент: {self} активен спустя {self.wait_time} сек {e}")

    def wait_value(self, value):
        self._init()
        timeout = time.time() + self.wait_time
        while time.time() < timeout:
            current_value = self.web_element.get_attribute("value")
            if current_value == value:
                return True
            else:
                time.sleep(1)
        else:
            raise ElementAttributeError(f"Не дождались значения {value} в элементе {self.xpath}")

    def wait_text(self, text):
        self._init()
        try:
            WebDriverWait(
                self.browser.driver, self.wait_time, ignored_exceptions=(StaleElementReferenceException,)
            ).until(EC.text_to_be_present_in_element((By.XPATH, self.xpath), text))
            return self
        except TimeoutException as e:
            raise ElementAttributeError(f"Не дождались значения {text} в элементе {self.xpath}")

    def move_to(self):
        self._init()
        ActionChains(self.browser.driver).move_to_element(self.web_element).perform()

    def click_with_offset(self, x: int, y: int):
        self._init()
        ActionChains(self.browser.driver).move_to_element_with_offset(self.web_element, x, y).click().perform()


@dataclass
class Element(WebElement):
    def __init__(self, xpath, wait_time=None):
        super(Element, self).__init__("", xpath, wait_time)

    def __post_init__(self):
        self.xpath = self.xpath or f"//*[normalize-space(.)='{self.name}']"


@dataclass
class Button(WebElement):
    def __post_init__(self):
        self.xpath = self.xpath or f"//button[normalize-space(.)='{self.name}']"


@dataclass
class TextInput(WebElement):
    def __post_init__(self):
        self.xpath = (
            self.xpath or f"//input[@name='{self.name}'] | //textarea[@name='{self.name}'] | //input[@id='{self.name}']"
        )


@dataclass
class StaticText(WebElement):
    def __post_init__(self):
        self.xpath = self.xpath or f"//*[normalize-space(text())='{self.name}']"


@dataclass
class LabelFor(WebElement):
    def __post_init__(self):
        self.xpath = self.xpath or f"//label[@for='{self.name}']"


@dataclass
class Link(WebElement):
    def __post_init__(self):
        self.xpath = self.xpath or f"//a[normalize-space(.)='{self.name}']"


@dataclass
class Label(WebElement):
    def __post_init__(self):
        self.xpath = self.xpath or f"//label[contains(normalize-space(.),'{self.name}')]"


@dataclass
class ListItem(WebElement):
    def __post_init__(self):
        self.xpath = self.xpath or f"//li[normalize-space(.)='{self.name}']"


@dataclass
class Href(WebElement):
    def __post_init__(self):
        self.xpath = f"//a[@href='{self.name}']"
