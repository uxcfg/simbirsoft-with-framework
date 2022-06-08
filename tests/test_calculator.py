from utils.allure import allure_step


def test_calculator(pages):
    """
    Открыть страницу http://google.com
    В поисковую строку ввести слово “Калькулятор”
    Нажать на кнопку поиска
    В открывшемся калькуляторе посчитать результат выражения: «1 * 2 - 3 + 1»

    OP:
    в строке памяти (строка над результатом) отображается ранее введенная формула «1 * 2 - 3 + 1 =»
    в строке результата отображается «0»
    """
    home = pages.google_home_page
    calc = pages.google_calculator_page

    with allure_step("Открыть страницу http://google.com"):
        home.open()

    with allure_step("В поисковую строку ввести слово “Калькулятор”"):
        home.fill_search_input("Калькулятор")

    with allure_step("Нажать на кнопку поиска"):
        home.click_on_search_btn()

    with allure_step("В открывшемся калькуляторе посчитать результат выражения: «1 * 2 - 3 + 1»"):
        calc.calculate_expression()
