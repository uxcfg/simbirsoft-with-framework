from selenium.webdriver import Remote, DesiredCapabilities

from web.driver.base import BaseWebDriver


class RemoteWebDriver(BaseWebDriver):
    def __init__(self, browser="chrome", wait_time=2, command_executor="http://127.0.0.1/wd/hub/", **kwargs):
        browser_name = browser.upper()

        caps = getattr(DesiredCapabilities, browser_name, {})

        if kwargs.get("desired_capabilities"):
            caps.update(kwargs["desired_capabilities"])

        kwargs["desired_capabilities"] = caps

        self.driver = Remote(command_executor, **kwargs)

        super(RemoteWebDriver, self).__init__(wait_time)
