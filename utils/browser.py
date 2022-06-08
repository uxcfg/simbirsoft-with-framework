from chromedriver_binary import add_chromedriver_to_path
from selenium.webdriver.chrome.options import Options

from settings import settings
from web.driver.chrome import ChromeWebDriver
from web.driver.firefox import FireFoxWebDriver
from web.driver.remote import RemoteWebDriver


def setup_browser():
    if settings.is_remote:
        browser = remote_browser()
    else:
        browser_name = settings.browser.lower()
        if browser_name == "chrome":
            browser = chrome_browser()
        elif browser_name == "firefox":
            browser = firefox_browser()
        else:
            raise Exception(f"Browser {browser_name} not found!")
    browser.driver.set_page_load_timeout(settings.wait_time)
    browser.driver.set_script_timeout(settings.wait_time)
    return browser


def firefox_browser():
    browser = FireFoxWebDriver()
    browser.driver.set_window_size(settings.browser_width, settings.browser_height)
    return browser


def chrome_browser():
    add_chromedriver_to_path()
    options = Options()
    if settings.in_container:
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--headless")
    options.add_argument("--disable-infobars")

    browser = ChromeWebDriver(options, wait_time=settings.wait_time)
    browser.driver.set_window_size(settings.browser_width, settings.browser_height)
    return browser


def remote_browser():
    desired_capabilities = {}

    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    if settings.browser_blocked_urls:
        chrome_options.add_argument(setup_blocked_urls())
    desired_capabilities.update(chrome_options.to_capabilities())

    selenoid_options = {
        "version": settings.browser_version,
        "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru:en", "LC_ALL=ru_RU.UTF-8"],
        "timezone": "Europe/Moscow",
        "name": settings.selenoid_session_name,
        "enableVNC": settings.selenoid_enable_vnc,
    }
    if settings.selenoid_hosts_entries:
        selenoid_options["hostsEntries"] = settings.selenoid_hosts_entries
    desired_capabilities.update(selenoid_options)

    browser = RemoteWebDriver(
        browser=settings.browser,
        command_executor=settings.selenoid_url,
        wait_time=settings.wait_time,
        desired_capabilities=desired_capabilities,
    )
    browser.driver.set_window_size(settings.browser_width, settings.browser_height)
    return browser


def setup_blocked_urls():
    urls = settings.browser_blocked_urls
    rule_template = ",".join(["MAP {} 127.0.0.1".format(url) for url in urls])
    return f"--host-resolver-rules={rule_template}"
