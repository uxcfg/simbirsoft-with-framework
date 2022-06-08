import time
import re
import requests
from selenium.common.exceptions import (
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver

from settings import settings
from urllib.parse import urlparse
from funcy import retry

from web.driver.exceptions import (
    WindowNotFound,
)


class BaseWebDriver:
    driver: WebDriver = None
    current_page = None

    def __init__(self, wait_time=2):
        self.wait_time = wait_time

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.quit()

    @property
    def title(self):
        return self.driver.title

    @property
    def html(self):
        return self.driver.page_source

    @property
    def url(self):
        return self.driver.current_url

    def switch_to_last_window(self):
        if len(self.driver.window_handles) > 1:
            tab = self.driver.window_handles[1]
            self.driver.switch_to.window(tab)

    def switch_to_first_window(self):
        tab = self.driver.window_handles[0]
        self.driver.switch_to.window(tab)

    def switch_to_window(self, index):
        total_windows = len(self.driver.window_handles)
        if total_windows > 1 and total_windows >= index:
            tab = self.driver.window_handles[-index]
            self.driver.switch_to.window(tab)

    def close_other_windows(self):
        if len(self.driver.window_handles) > 1:
            current_window = self.driver.current_window_handle
            for handle in self.driver.window_handles:
                if handle != current_window:
                    self.driver.switch_to.window(handle)
                    self.driver.close()

    def switch_to_next_window(self):
        if len(self.driver.window_handles) > 1:
            current_window = self.driver.current_window_handle
            next_window_index = self.driver.window_handles.index(current_window) - 1
            self.driver.switch_to.window(self.driver.window_handles[next_window_index])

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def reload(self):
        self.driver.refresh()

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def evaluate_script(self, script, *args):
        return self.driver.execute_script("return %s" % script, *args)

    def open(self, url):
        self.driver.get(url)

    def quit(self):
        try:
            self.driver.quit()
        except WebDriverException:
            pass

    def wait_window(self, title_part):
        timeout = self.wait_time + time.time()
        while time.time() < timeout:
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                if title_part in self.driver.title:
                    return True
            time.sleep(1)
        else:
            raise WindowNotFound(f"Не найдено окно содержащее в заголовке `{title_part}`")

    def accept_alert(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    def scroll_by(self, x: int, y: int):
        self.execute_script(f"window.scrollBy({x}, {y})")

    def scroll_down(self, pixel=1500):
        self.scroll_by(0, pixel)

    def scroll_up(self, pixel=1500):
        self.scroll_by(0, -pixel)

    @property
    def download_url(self):
        up = urlparse(settings.selenoid_url)
        session_id = self.driver.session_id
        url = f"{up.scheme}://{up.netloc}/download/{session_id}"
        return url

    def get_downloaded_file_names(self):
        if not settings.is_remote:
            return []
        response = requests.get(self.download_url)
        result = re.findall(r">(.*?)</a>", response.text)
        print(f"Downloaded response: {response.text}")
        print(f"Downloaded result: {result}")
        return result

    def get_downloaded_file(self, file_name):
        """Возвращает байтовое представление файла"""
        response = requests.get(f"{self.download_url}/{file_name}", stream=True)
        return response.content

    def download_file_to_folder(self, file_index=0):
        """Отдает байтовое представление файла"""
        file_names = self.get_downloaded_file_names()
        assert file_names, "Could not download file"

        file_name = file_names[file_index]
        raw_file = self.get_downloaded_file(file_name)
        return raw_file

    @retry(settings.wait_time, timeout=1)
    def wait_for_downloaded_file(self, filename):
        assert settings.is_remote is True, "Can not check downloaded file on local running"
        assert filename in self.get_downloaded_file_names(), f"Файл {filename} не скачан"
        return True

    def get_local_storage_item(self, key):
        return self.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set_local_storage_item(self, key: str, value: str):
        self.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def switch_to_frame(self, element):
        self.driver.switch_to.frame(element.web_element)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
