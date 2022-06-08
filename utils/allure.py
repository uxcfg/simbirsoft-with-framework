from contextlib import contextmanager

import allure
from allure_commons.types import AttachmentType

from settings import settings


def make_screen(name):
    from register import pages

    allure.attach(
        pages.browser.driver.get_screenshot_as_png(),
        name=name,
        attachment_type=AttachmentType.PNG,
    )


@contextmanager
def allure_step(name, wait_time: int = None):
    from register import pages

    with allure.step(name):
        try:
            if wait_time:
                pages.browser.wait_time = wait_time
            yield
            pages.browser.wait_time = settings.wait_time
            make_screen("screen")
        except Exception:
            make_screen("error")
            raise
