# Описание фремворка
Основная идея - использование паттерна page object.
Каждый тест может иметь свой page object. Базовые классы находятся в web.pages.
Необходимые для тестов страницы создавать в папке pages
Классы страниц требуется прописать в файле register для их инициализации при запуске теста

# Настройка проекта
Установите python 3.8 и выше.

Необходимо прописать ENVIRONMENT переменные.
Шаблон переменных и их описание находится в файле `.env.template`.
Создайте файл `.env` и скопируйте туда переменные.
Также все переменные можно прописать в PATH.

## Установка/обновление chromedriver
Установите библиотеки `pip install -r requirements.txt`.
Данная команда сразу установит chromedriver. Если в будущем вы планируете обновить версию chromedriver,
то пропишите в `requirements.txt` новую версию, а затем выполните команду `pip install -r requirements.txt --upgrade`

# Запуск тестов
Через команду `pytest <путь к тесту>` или pycharm.

# Запуск тестов в Jenkins
Прописать переменную  `VENV` - путь до виртуального окруженич python.
Прописать `REPO_PATH` - путь до репозитория с тестами

# Пожеланию по развитию проекта
Не забывайте форматировать код в редакторе. Делайте это через команду `black .`
Спасибо!
