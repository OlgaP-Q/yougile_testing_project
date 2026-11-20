"""Page Object страницы Доски (Board) в YouGile."""
from __future__ import annotations
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BoardPage:
    """Методы для работы с задачами на доске."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        # Кнопка добавления задачи
        self.add_task_btn = (
            By.XPATH,
            "//span[text()='Добавить задачу']/ancestor::div[@role='button']",
        )
        # Поле ввода при создании задачи
        # (единственное поле с таким data-testid)
        self.task_input = (
            By.XPATH,
            "//textarea[@data-testid='board-task-input-name']",
        )

    def create_task(self, task_name: str) -> None:
        """Создаёт задачу на доске."""
        wait = WebDriverWait(self.driver, 10)

        print("  -> Жмем '+ Добавить задачу'...")
        wait.until(EC.element_to_be_clickable(self.add_task_btn)).click()

        print(f"  -> Вводим текст: '{task_name}'...")
        input_field = wait.until(EC.element_to_be_clickable(self.task_input))
        input_field.send_keys(task_name)
        input_field.send_keys(Keys.ENTER)

        try:
            self.driver.find_element(
                By.XPATH, "//*[contains(text(), 'Новая колонка')]"
            ).click()
        except Exception:
            pass

    def edit_task(self, old_name: str, new_name: str) -> None:
        """Открывает задачу, меняет её название и сохраняет."""
        wait = WebDriverWait(self.driver, 15)

        # 1. Открываем задачу на доске
        print(f"  -> Открываем задачу '{old_name}'...")
        task_title_locator = (
            By.XPATH,
            f"//div[@data-testid='board-task-title' "
            f"and normalize-space(.)='{old_name}']",
        )
        wait.until(EC.element_to_be_clickable(task_title_locator)).click()

        # 2. Ждем появления боковой панели и кликаем по заголовку
        print("  -> Активируем редактирование названия...")
        panel_title_locator = (
            By.XPATH,
            f"//*[normalize-space(text())='{old_name}' "
            f"and not(@data-testid='board-task-title')]"
        )
        panel_title = wait.until(
            EC.element_to_be_clickable(panel_title_locator)
        )
        panel_title.click()

        # 3. Ищем поле ввода, ИСКЛЮЧАЯ поле создания задачи на доске
        print(f"  -> Вводим новое имя: '{new_name}'...")
        edit_input_locator = (
            By.XPATH,
            "//textarea[not(@data-testid='board-task-input-name')] | "
            "//input[@type='text'"
            " and not(@data-testid='board-task-input-name')] | "
            "//*[@contenteditable='true' "
            "and not(@data-testid='board-task-input-name')]"
        )
        input_field = wait.until(
            EC.visibility_of_element_located(edit_input_locator)
        )

        # 4. Очищаем поле (надежно, через физические клавиши)
        print("  -> Очищаем поле от старого текста...")
        input_field.click()

        # Если поле не пустое,
        # зажимаем Ctrl, жмем A, отпускаем Ctrl и жмем Backspace
        val = input_field.get_attribute("value") or input_field.text
        if val:
            (
                ActionChains(self.driver)
                .key_down(Keys.CONTROL)
                .send_keys("a")
                .key_up(Keys.CONTROL)
                .send_keys(Keys.BACKSPACE)
                .perform()
            )

        # 5. Вводим новый текст и сохраняем
        input_field.send_keys(new_name)
        input_field.send_keys(Keys.ENTER)

        # 6. Ждем, пока в панели обновится заголовок
        new_panel_title_locator = (
            By.XPATH,
            f"//*[normalize-space(text())='{new_name}' "
            f"and not(@data-testid='board-task-title')]"
        )
        wait.until(EC.visibility_of_element_located(new_panel_title_locator))

        # 7. Закрываем панель
        print("  -> Закрываем боковую панель...")
        try:
            close_btn = self.driver.find_element(
                By.XPATH, "//*[@data-icon='IconClose']/parent::*"
            )
            self.driver.execute_script("arguments[0].click();", close_btn)
        except Exception:
            self.driver.find_element(By.TAG_NAME, "body").click()

        # 8. Обновляем страницу, чтобы доска гарантированно перерисовалась
        print("  -> Обновляем страницу...")
        self.driver.refresh()

        # 9. Ждем появления карточки с новым именем на доске
        new_board_title_locator = (
            By.XPATH,
            f"//div[@data-testid='board-task-title' "
            f"and normalize-space(.)='{new_name}']"
        )
        wait.until(EC.visibility_of_element_located(new_board_title_locator))
        print("  -> Карточка успешно обновлена на доске.")

    def is_task_visible(self, task_name: str) -> bool:
        """Проверяет, есть ли задача
        с таким именем на доске (точное совпадение)."""
        wait = WebDriverWait(self.driver, 5)
        task_locator = (
            By.XPATH,
            f"//div[@data-testid='board-task-title' "
            f"and normalize-space(.)='{task_name}']",
        )
        try:
            wait.until(EC.visibility_of_element_located(task_locator))
            return True
        except Exception:
            return False
