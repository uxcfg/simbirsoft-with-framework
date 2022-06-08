class DriverException(AssertionError):
    pass


class WindowNotFound(DriverException):
    pass


class ElementNotFound(DriverException):
    pass


class ElementNotVisible(DriverException):
    pass


class ElementStillVisible(DriverException):
    pass


class ElementNotInteractable(DriverException):
    pass


class ElementNotClickable(DriverException):
    pass


class ElementAttributeError(AssertionError):
    pass


class ElementStillInteractable(AssertionError):
    pass
