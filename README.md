 **YouGile QA Automation Project**
Дипломный проект по автоматизации тестирования веб-приложения YouGile (система управления проектами).
Проект включает в себя два набора автотестов: UI-тесты (на базе Selenium) и API-тесты (на базе Requests).

###  Стек технологий

Python 3.12+
Pytest — фреймворк для запуска тестов.
Selenium — для UI-автотестов.
Requests — для API-автотестов.
Allure — для формирования отчетов.

### Установка

# Клонируйте репозиторий на свой компьютер:

bash
git clone <URL_вашего_репозитория>
cd yougile_testing_project
Создайте и активируйте виртуальное окружение:
bash
# Для Linux / macOS:
python -m venv venv
source venv/bin/activate
# Для Windows:
python -m venv venv
venv\Scripts\activate

# Установите необходимые зависимости:

bash
pip install -r requirements.txt

###  Настройка конфигурации

Перед запуском тестов вам необходимо создать файл 
config.py
 в корне проекта (рядом с папками ui_tests и api_tests), так как он содержит секретные данные и не хранится в репозитории.

# Создайте файл config.py и заполните его по образцу:

config.example.py

# Данные для авторизации в UI
EMAIL = "ваша_почта@example.com"
PASSWORD = "ваш_пароль"

# Данные для API-тестов
API_URL = "https://ru.yougile.com/api-v2"
API_TOKEN = "ВАШ_API_ТОКЕН_БЕЗ_СЛОВА_BEARER"  # Получите в настройках профиля YouGile
PROJECT_ID = "ID_вашего_тестового_проекта"
COLUMN_ID = "ID_вашей_тестовой_колонки"
USER_ID = "ID_вашего_пользователя"

### Запуск тестов

Все команды выполняются из корневой папки проекта.

## Запустить вообще все тесты (UI + API):

python -m pytest -s

## Запустить только UI-тесты (Selenium):
python -m pytest ui_tests/ -s

## Запустить только API-тесты (Requests):
python -m pytest api_tests/ -s


(Флаг -s позволяет видеть все print() в консоли, чтобы отслеживать шаги выполнения).

### Генерация отчета Allure

Проект интегрирован с Allure для наглядного отображения результатов.

# Запустите тесты с сохранением результатов:

python -m pytest --alluredir=allure-results

## Сгенерируйте и откройте отчет в браузере:
allure serve allure-results

###  Структура проекта

yougile_testing_project/
├── api_tests/               # API-тесты
│   ├── conftest.py          # Фикстуры для API (headers, base_url)
│   └── test_api.py          # Сами API-тесты (CRUD, роли, негативные)
├── ui_tests/                # UI-тесты
│   ├── pages/               # Page Object'ы (LoginPage, BoardPage, ChatPage)
│   ├── conftest.py          # Фикстуры (запуск браузера, удаление чата)
│   └── test_*.py            # Тесты (логин, задачи, чаты)
├── config.py                # (Создается локально) Настройки и токены
├── requirements.txt         # Зависимости проекта
├── pytest.ini               # Конфигурация Pytest (если есть)
└── README.md                # Описание проекта

