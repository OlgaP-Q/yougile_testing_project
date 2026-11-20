import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from config import EMAIL, PASSWORD
from pages.chat_page import ChatPage
from pages.login_page import LoginPage


@pytest.fixture()
def driver() -> webdriver.Chrome:
    """Запускает и закрывает браузер."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Драйвер с уже выполненным входом и дождавшийся загрузки интерфейса."""
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login(EMAIL, PASSWORD)

    # Ждём, пока прогрузится главная страница (появится боковое меню)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Моя компания')]")
        )
    )
    return driver


@pytest.fixture
def chat_env(logged_in_driver):
    """Готовит независимое окружение:
     создает уникальный чат и удаляет его после теста."""
    chat_page = ChatPage(logged_in_driver)
    chat_name = f"Autotest-{uuid.uuid4().hex[:6]}"

    chat_page.open_messenger()
    chat_page.create_group_chat(chat_name)

    yield chat_name

    try:
        chat_page.delete_chat(chat_name)
    except Exception as e:
        print(f"  [teardown] Не удалось удалить '{chat_name}': {e}")


@pytest.fixture
def unique_message() -> str:
    """Уникальный текст сообщения."""
    return f"Autotest {uuid.uuid4().hex[:8]}"
