from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from web.driver.base import BaseWebDriver


class ChromeWebDriver(BaseWebDriver):
    def __init__(
        self, options=None, user_agent=None, wait_time=2, fullscreen=False, incognito=False, headless=False, **kwargs
    ):

        options = Options() if options is None else options

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        if incognito:
            options.add_argument("--incognito")

        if fullscreen:
            options.add_argument("--kiosk")

        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        self.driver = Chrome(options=options, **kwargs)
        super(ChromeWebDriver, self).__init__(wait_time)
