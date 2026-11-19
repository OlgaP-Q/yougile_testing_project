"""Тесты авторизации в YouGile."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import EMAIL, PASSWORD
from pages.login_page import LoginPage


@pytest.mark.ui
def test_successful_login(driver) -> None:
    """
    Успешный вход:
      - открывает страницу логина;
      - вводит валидные EMAIL/PASSWORD;
      - проверяет, что URL сменился и появился интерфейс.
    """
    print("\n--- ТЕСТ: Успешный вход ---")

    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login(EMAIL, PASSWORD)

    # Проверяем, что URL больше не содержит /login
    assert "/login" not in driver.current_url, (
        f"Не удалось войти в систему. Текущий URL: {driver.current_url}"
    )

    # Дополнительно ждём появления бокового меню —
    # это гарантирует, что интерфейс реально прогрузился
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Моя компания')]")
        )
    )

    print("  -> Вход выполнен успешно.")
