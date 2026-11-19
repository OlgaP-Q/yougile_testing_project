"""Page Object страницы Мессенджера в YouGile."""
from __future__ import annotations
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ChatPage:
    """Методы для работы с Мессенджером:
     создание, поиск, отправка, удаление."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

        # Навигация
        self.messenger_btn = (
            By.XPATH,
            "//*[contains(normalize-space(text()), 'Мессенджер')]",
        )

        # Список и поиск чатов
        self.search_input = (By.XPATH, "//input[@placeholder='Поиск']")
        self.chat_item = (By.XPATH, "//div[@data-chat-id]")

        # Поле ввода и кнопка отправки
        self.message_input = (
            By.CSS_SELECTOR,
            "div[role='textbox'][contenteditable='true']",
        )
        self.send_button = (
            By.XPATH,
            "//*[@data-icon='IconSend']/parent::div",
        )

        # Создание чата
        self.plus_btn = (
            By.CSS_SELECTOR,
            "[data-testid='create-chat-menu-trigger']",
        )
        self.create_group_chat_menu = (
            By.XPATH,
            "//*[contains(text(), 'Создать групповой чат')]",
        )
        self.chat_name_input = (
            By.XPATH,
            "//input[@value='Новый групповой чат']",
        )
        self.submit_chat_btn = (By.XPATH, "//*[text()='Создать чат']")

        # Удаление чата
        self.edit_chat_btn = (
            By.CSS_SELECTOR,
            "[data-testid='edit-group-chat']",
        )
        self.delete_chat_menu_item = (
            By.XPATH,
            "//button[contains(text(), 'Удалить чат')] | "
            "//div[contains(text(), 'Удалить чат')]",
        )
        # Улучшенный локатор для красной кнопки "Удалить" в окне подтверждения
        self.confirm_delete_btn = (
            By.XPATH,
            "//button[normalize-space(.)='Удалить'] | "
            "//div[normalize-space(.)='Удалить']",
        )

    # ------------------------------------------------------------------
    # Ожидания
    # ------------------------------------------------------------------

    def _wait_seconds(self, seconds: float, poll: float = 0.1) -> None:
        """Fixed wait через WebDriverWait (замена time.sleep)."""
        try:
            WebDriverWait(
                self.driver, seconds, poll_frequency=poll
            ).until(lambda d: False)
        except TimeoutException:
            pass

    # ------------------------------------------------------------------
    # Навигация
    # ------------------------------------------------------------------

    def open_messenger(self) -> None:
        """Открывает раздел Мессенджер."""
        wait = WebDriverWait(self.driver, 20)
        print("  -> Переходим в Мессенджер...")

        messenger = wait.until(
            EC.presence_of_element_located(self.messenger_btn)
        )
        self.driver.execute_script("arguments[0].click();", messenger)
        self._wait_seconds(2)

    # ------------------------------------------------------------------
    # Создание и удаление чата
    # ------------------------------------------------------------------

    def create_group_chat(self, chat_name: str) -> None:
        """Создаёт групповой чат с указанным именем."""
        wait = WebDriverWait(self.driver, 20)

        print("  -> Кликаем на плюсик...")
        plus = wait.until(EC.element_to_be_clickable(self.plus_btn))
        self.driver.execute_script("arguments[0].click();", plus)

        print("  -> Выбираем 'Создать групповой чат'...")
        menu_item = wait.until(
            EC.element_to_be_clickable(self.create_group_chat_menu)
        )
        self.driver.execute_script("arguments[0].click();", menu_item)

        print("  -> Вводим название чата...")
        name_field = wait.until(
            EC.visibility_of_element_located(self.chat_name_input)
        )
        name_field.click()
        self.driver.execute_script("arguments[0].value = '';", name_field)
        name_field.send_keys(chat_name)

        print("  -> Нажимаем 'Создать чат'...")
        submit_btn = wait.until(
            EC.presence_of_element_located(self.submit_chat_btn)
        )
        self.driver.execute_script("arguments[0].click();", submit_btn)

        wait.until(EC.invisibility_of_element_located(self.submit_chat_btn))
        print(f"  -> Чат '{chat_name}' создан.")

        # ВОТ ЗДЕСЬ ОТСТУП ДОЛЖЕН БЫТЬ 4 ПРОБЕЛА (как у create_group_chat)

    def is_chat_visible(self, chat_name: str) -> bool:
        """Проверяет, появился ли чат в левом списке."""
        wait = WebDriverWait(self.driver, 10)
        # Ищем чат внутри списка чатов (по data-chat-id)
        locator = (
            By.XPATH,
            f"//div[@data-chat-id]//*[contains(text(), '{chat_name}')]"
        )
        try:
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def delete_chat(self, chat_name: str) -> None:
        """Находит чат, открывает его и удаляет через два модальных окна."""
        wait = WebDriverWait(self.driver, 15)
        print(f"  -> [teardown] Удаляем чат '{chat_name}'...")

        # 1. Открываем чат
        self._find_and_open_chat(chat_name)

        # 2. Жмем на кнопку редактирования (карандаш) в шапке
        print("     -> Жмем на кнопку редактирования (карандаш)...")
        edit_btn = wait.until(
            EC.presence_of_element_located(self.edit_chat_btn)
        )
        self.driver.execute_script("arguments[0].click();", edit_btn)

        # 3. Ждем, пока модальное окно редактирования откроется
        print("     -> Ждем открытия окна 'Редактирование'...")
        edit_modal_locator = (
            By.XPATH,
            "//*[contains(text(), 'Редактирование группового чата')]"
        )
        wait.until(EC.visibility_of_element_located(edit_modal_locator))

        # 4. Жмем "Удалить чат" в окне редактирования
        print("     -> Жмем 'Удалить чат' в окне редактирования...")
        delete_btn_text = wait.until(
            EC.element_to_be_clickable(self.delete_chat_menu_item)
        )
        self.driver.execute_script("arguments[0].click();", delete_btn_text)

        # 5. Ждем появления ОКНА ПОДТВЕРЖДЕНИЯ
        print("     -> Ждем окна подтверждения удаления...")
        confirm_modal_locator = (
            By.XPATH,
            "//*[contains(text(), 'Удаление группового чата')]"
        )
        wait.until(EC.visibility_of_element_located(confirm_modal_locator))

        # 6. Жмем красную кнопку "Удалить"
        print("     -> Подтверждаем удаление (красная кнопка)...")

        # Ищем ЛЮБОЙ элемент (div, span, button) с точным текстом 'Удалить'
        confirm_btn_locator = (By.XPATH, "//*[normalize-space(.)='Удалить']")

        try:
            confirm_btn = wait.until(
                EC.element_to_be_clickable(confirm_btn_locator)
            )

            # Выводим HTML для отладки
            print(f"     -> HTML кнопки:"
                  f" {confirm_btn.get_attribute('outerHTML')[:200]}")
            # Кликаем физически мышью (React требует доверенных событий)
            (
                ActionChains(self.driver)
                .move_to_element(confirm_btn)
                .click()
                .perform()
            )
        except TimeoutException:
            self.driver.save_screenshot("screenshots/error_confirm_delete.png")
            raise AssertionError(
                "Не найдена кнопка 'Удалить'. Скриншот сохранен."
            )

        # 7. Ждем, пока окно подтверждения исчезнет
        print("     -> Ждем закрытия окна подтверждения...")
        wait.until(EC.invisibility_of_element_located(confirm_modal_locator))

        # 8. ПРОВЕРКА: Ждем, пока чат исчезнет из списка
        print("     -> Проверяем, что чат исчез из списка...")
        chat_in_list_locator = (
            By.XPATH,
            f"//div[@data-chat-id]//*[contains(text(), '{chat_name}')]"
        )

        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(chat_in_list_locator)
            )
            print(f"  -> Чат '{chat_name}' успешно удалён.")
        except TimeoutException:
            self.driver.save_screenshot(
                "screenshots/error_chat_not_deleted.png"
            )
            raise AssertionError(
                f"Чат '{chat_name}' не исчез из списка после удаления. "
                "Скриншот сохранен в screenshots/error_chat_not_deleted.png"
            )

    # ------------------------------------------------------------------
    # Поиск и открытие чата
    # ------------------------------------------------------------------

    def _find_and_open_chat(self, chat_name: str) -> None:
        """Вводит имя чата в поиск и открывает первый результат."""
        wait = WebDriverWait(self.driver, 20)

        search_field = wait.until(
            EC.element_to_be_clickable(self.search_input)
        )
        search_field.click()
        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.BACKSPACE)
        search_field.send_keys(chat_name)

        chat_element = wait.until(
            EC.presence_of_element_located(self.chat_item)
        )
        self.driver.execute_script("arguments[0].click();", chat_element)
        self._wait_seconds(2)

    # ------------------------------------------------------------------
    # Отправка сообщения
    # ------------------------------------------------------------------

    def send_message_to_existing_chat(
        self, chat_name: str, message: str
    ) -> None:
        """Находит чат по имени, вводит сообщение и отправляет его."""
        wait = WebDriverWait(self.driver, 20)

        print(f"  -> Ищем чат '{chat_name}' через поиск...")
        self._find_and_open_chat(chat_name)

        print("  -> Вводим сообщение...")
        msg_field = wait.until(
            EC.visibility_of_element_located(self.message_input)
        )
        msg_field.click()
        self._wait_seconds(0.5)

        ActionChains(self.driver).send_keys(message).perform()
        self._wait_seconds(1)

        self.driver.execute_script(
            """
            var el = arguments[0];
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new KeyboardEvent('keyup',
                { bubbles: true, key: 'a' }));
            """,
            msg_field,
        )

        print("  -> Ждем активации кнопки отправки...")
        self._wait_seconds(2)

        send_btns = self.driver.find_elements(*self.send_button)
        visible_btn = next(
            (btn for btn in send_btns if btn.is_displayed()), None
        )
        if visible_btn is None:
            raise AssertionError("Кнопка отправки не найдена на экране!")

        print(
            f"  -> Класс кнопки до клика: "
            f"{visible_btn.get_attribute('class')}"
        )

        print("  -> Кликаем кнопку отправки...")
        self.driver.execute_script(
            """
            var elem = arguments[0];
            var rect = elem.getBoundingClientRect();
            var x = rect.left + rect.width / 2;
            var y = rect.top + rect.height / 2;

            ['pointerover','pointerenter','mouseover','mouseenter',
             'pointerdown','mousedown','pointerup','mouseup','click']
            .forEach(function(type) {
                var evt;
                if (type.indexOf('pointer') === 0) {
                    evt = new PointerEvent(type, {
                        view: window, bubbles: true, cancelable: true,
                        clientX: x, clientY: y, button: 0, pointerId: 1
                    });
                } else {
                    evt = new MouseEvent(type, {
                        view: window, bubbles: true, cancelable: true,
                        clientX: x, clientY: y, button: 0
                    });
                }
                elem.dispatchEvent(evt);
            });
            """,
            visible_btn,
        )

        print("  -> Ждем, пока запрос уйдет на сервер...")
        self._wait_seconds(2)

        print("  -> ПРОВЕРКА: ждем сообщение в истории чата...")
        message_locator = (
            By.XPATH,
            "//div[contains(@class, 'chat-item-messages')]"
            f"//*[normalize-space(text())='{message}']",
        )

        try:
            wait.until(EC.visibility_of_element_located(message_locator))
            print("  -> Сообщение отправлено и видно в чате!")
        except TimeoutException:
            self._debug_chat_state()
            print("  -> Fallback: native .click()...")
            visible_btn.click()
            self._wait_seconds(2)
            wait.until(EC.visibility_of_element_located(message_locator))
            print("  -> Fallback сработал! Сообщение отправлено.")

    # ------------------------------------------------------------------
    # Отладка
    # ------------------------------------------------------------------

    def _debug_chat_state(self) -> None:
        """Печатает содержимое чата при неудачной отправке."""
        print("  -> ОШИБКА: сообщение не появилось. Отладка:")
        try:
            chat_text = self.driver.execute_script(
                """
                var el = document.querySelector('.chat-item-messages');
                return el ? el.innerText.substring(0, 500)
                          : 'chat-item-messages not found';
                """
            )
            print(f"  -> Последние сообщения в чате:\n{chat_text}")
        except Exception as dbg_err:  # noqa: BLE001
            print(f"  -> Не удалось получить отладку: {dbg_err}")
