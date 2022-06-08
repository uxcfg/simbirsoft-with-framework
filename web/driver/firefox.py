from selenium.webdriver import DesiredCapabilities, Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options

from web.driver.base import BaseWebDriver


class FireFoxWebDriver(BaseWebDriver):
    driver_name = "Firefox"

    def __init__(
        self,
        profile=None,
        extensions=None,
        user_agent=None,
        profile_preferences=None,
        fullscreen=False,
        wait_time=2,
        timeout=90,
        capabilities=None,
        headless=False,
        incognito=False,
        **kwargs,
    ):

        firefox_profile = FirefoxProfile(profile)
        firefox_profile.set_preference("extensions.logging.enabled", False)
        firefox_profile.set_preference("network.dns.disableIPv6", False)

        firefox_capabilities = DesiredCapabilities().FIREFOX
        firefox_capabilities["marionette"] = True

        firefox_options = Options()

        if capabilities:
            for key, value in capabilities.items():
                firefox_capabilities[key] = value

        if user_agent is not None:
            firefox_profile.set_preference("general.useragent.override", user_agent)

        if profile_preferences:
            for key, value in profile_preferences.items():
                firefox_profile.set_preference(key, value)

        if extensions:
            for extension in extensions:
                firefox_profile.add_extension(extension)

        if headless:
            firefox_options.add_argument("--headless")

        if incognito:
            firefox_options.add_argument("-private")

        self.driver = Firefox(
            firefox_profile, capabilities=firefox_capabilities, options=firefox_options, timeout=timeout, **kwargs
        )

        if fullscreen:
            self.driver.fullscreen_window()

        super(FireFoxWebDriver, self).__init__(wait_time)
