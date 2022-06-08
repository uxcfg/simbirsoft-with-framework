from web.pages.base import BasePage
from web.driver.web_element import Element


class GoogleCalculatorPage(BasePage):
    class Elements:
        number1 = Element("//div[text()='1']")
        number2 = Element("//div[text()='2']")
        number3 = Element("//div[text()='3']")

        multi = Element("//div[@aria-label='умножение']")
        subtraction = Element("//div[@aria-label='вычитание']")
        addition = Element("//div[@aria-label='сложение']")
        equal = Element("//div[@aria-label='равно']")

        value_memory = Element("//span[text()='1 × 2 - 3 + 1 =']")
        calc_result = Element("//div[@role='presentation']//span[text()='0']")

    def is_loaded(self):
        Element("//body")
        return True

    def calculate_expression(self):
        self.Elements.number1.click()
        self.Elements.multi.click()
        self.Elements.number2.click()
        self.Elements.subtraction.click()
        self.Elements.number3.click()
        self.Elements.addition.click()
        self.Elements.number1.click()
        self.Elements.equal.click()

        assert self.Elements.value_memory.text == "1 × 2 - 3 + 1 ="
        assert self.Elements.calc_result.text == "0"
