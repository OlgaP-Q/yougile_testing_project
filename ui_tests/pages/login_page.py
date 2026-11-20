from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        # 1. Локатор кнопки "Войти" на главной странице
        self.home_login_btn = (
            By.XPATH, "//a[contains(@class, 'sign-in-button')]"
        )

        # 2. Локаторы для полей, которые появятся ПОСЛЕ клика
        self.email_input = (By.XPATH, "//input[@type='email']")
        self.password_input = (By.XPATH, "//input[@type='password']")
        self.submit_btn = (
            By.XPATH, "//div[@role='button' and contains(., 'Войти')]"
        )

    def open_page(self) -> None:
        self.driver.get("https://ru.yougile.com")

    def login(self, email: str, password: str) -> None:
        wait = WebDriverWait(self.driver, 10)

        # ШАГ 1: Ждем появления кнопки "Войти" на главной и кликаем по ней
        home_btn = wait.until(
            EC.element_to_be_clickable(self.home_login_btn)
        )
        home_btn.click()

        # ШАГ 2: Ждем, пока загрузится форма логина и вводим почту
        email_field = wait.until(
            EC.visibility_of_element_located(self.email_input)
        )
        email_field.clear()
        email_field.send_keys(email)

        # ШАГ 3: Вводим пароль
        password_field = wait.until(
            EC.visibility_of_element_located(self.password_input)
        )
        password_field.send_keys(password)

        # ШАГ 4: Жмем кнопку "Войти" уже на странице логина
        wait.until(EC.element_to_be_clickable(self.submit_btn)).click()
