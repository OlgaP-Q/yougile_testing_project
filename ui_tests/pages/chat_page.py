from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException


class ChatPage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        # Основные элементы
        self.messenger_btn = (By.XPATH, "//*[text()='Мессенджер']")
        self.search_input = (By.XPATH, "//input[@placeholder='Поиск']")
        self.chat_item = (By.CSS_SELECTOR, "div[data-chat-id]")

        # Создание чата
        self.plus_btn = (By.CSS_SELECTOR, "[data-testid='create-chat-menu-trigger']")
        self.create_group_chat_menu = (By.XPATH, "//*[contains(text(), 'Создать групповой чат')]")
        self.chat_name_input = (By.XPATH, "//input[@value='Новый групповой чат']")
        self.submit_chat_btn = (By.XPATH, "//*[text()='Создать чат']")

        # Отправка сообщения (CKEditor)
        self.message_input = (By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']")
        self.send_button = (By.XPATH, "//*[@data-icon='IconSend']/parent::div")

        # Удаление чата
        self.edit_chat_btn = (
        By.XPATH, "//*[name()='svg' and (contains(@data-icon, 'Pencil') or contains(@data-icon, 'Edit'))]/parent::*")
        self.delete_chat_menu_item = (By.XPATH, "//*[contains(text(), 'Удалить чат')]")

    def open_messenger(self) -> None:
        """Переходит в раздел 'Мессенджер' и ждет загрузки списка чатов."""
        wait = WebDriverWait(self.driver, 15)
        print("  -> Переходим в Мессенджер...")
        messenger = wait.until(EC.element_to_be_clickable(self.messenger_btn))
        self.driver.execute_script("arguments[0].click();", messenger)
        wait.until(EC.presence_of_element_located(self.search_input))

    def create_group_chat(self, chat_name: str) -> None:
        """Создает новый групповой чат."""
        wait = WebDriverWait(self.driver, 15)

        print("  -> Кликаем на плюсик...")
        plus = wait.until(EC.element_to_be_clickable(self.plus_btn))
        self.driver.execute_script("arguments[0].click();", plus)

        print("  -> Выбираем 'Создать групповой чат'...")
        menu_item = wait.until(EC.element_to_be_clickable(self.create_group_chat_menu))
        self.driver.execute_script("arguments[0].click();", menu_item)

        print("  -> Вводим название чата...")
        name_field = wait.until(EC.visibility_of_element_located(self.chat_name_input))
        name_field.click()
        name_field.clear()
        self.driver.execute_script("arguments[0].value = '';", name_field)
        name_field.send_keys(chat_name)

        print("  -> Нажимаем кнопку 'Создать чат'...")
        submit_btn = wait.until(EC.presence_of_element_located(self.submit_chat_btn))
        self.driver.execute_script("arguments[0].click();", submit_btn)

        # Ждем, пока модальное окно закроется
        wait.until(EC.invisibility_of_element_located(self.submit_chat_btn))

        # Ждем появления чата в списке
        print(f"  -> Ждем появления чата '{chat_name}' в списке...")
        chat_locator = (By.XPATH, f"//*[contains(text(), '{chat_name}')]")
        wait.until(EC.visibility_of_element_located(chat_locator))
        print("  -> Чат успешно создан!")

    def _find_and_open_chat(self, chat_name: str) -> None:
        """Вводит имя чата в поиск и открывает первый результат."""
        wait = WebDriverWait(self.driver, 20)

        search_field = wait.until(EC.element_to_be_clickable(self.search_input))
        search_field.click()
        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.BACKSPACE)
        search_field.send_keys(chat_name)

        chat_element = wait.until(EC.presence_of_element_located(self.chat_item))
        self.driver.execute_script("arguments[0].click();", chat_element)

        # Ждем, пока поле ввода сообщения станет видимым (чат загрузился)
        wait.until(EC.visibility_of_element_located(self.message_input))

    def send_message_to_existing_chat(self, chat_name: str, message: str) -> None:
        """Находит чат по имени, вводит сообщение и отправляет его."""
        wait = WebDriverWait(self.driver, 20)

        print(f"  -> Открываем чат '{chat_name}'...")
        self._find_and_open_chat(chat_name)

        print("  -> Вводим сообщение...")
        msg_field = wait.until(EC.element_to_be_clickable(self.message_input))
        msg_field.click()

        # Ждем, пока редактор получит фокус
        wait.until(lambda d: 'ck-focused' in d.find_element(*self.message_input).get_attribute('class'))

        ActionChains(self.driver).send_keys(message).perform()

        # Триггерим события для React
        self.driver.execute_script("""
              var el = arguments[0];
              el.dispatchEvent(new Event('input', { bubbles: true }));
              el.dispatchEvent(new Event('change', { bubbles: true }));
              el.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true, key: 'a' }));
          """, msg_field)

        print("  -> Ждем активации кнопки отправки...")
        send_btns = wait.until(EC.presence_of_all_elements_located(self.send_button))
        visible_btn = next((btn for btn in send_btns if btn.is_displayed()), None)

        if not visible_btn:
            raise AssertionError("Кнопка отправки не найдена на экране!")

        print("  -> Кликаем кнопку отправки (через JS-события)...")
        self.driver.execute_script("""
              var elem = arguments[0];
              var rect = elem.getBoundingClientRect();
              var x = rect.left + rect.width / 2;
              var y = rect.top + rect.height / 2;

              ['pointerover','pointerenter','mouseover','mouseenter',
               'pointerdown','mousedown','pointerup','mouseup','click'].forEach(function(type) {
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
          """, visible_btn)

        print("  -> ПРОВЕРКА: Ждем появления текста в истории чата...")
        message_locator = (
            By.XPATH,
            f"//div[contains(@class, 'chat-item-messages')]//*[normalize-space(text())='{message}']"
        )

        try:
            wait.until(EC.visibility_of_element_located(message_locator))
            print("  -> Сообщение успешно отправлено!")
        except TimeoutException:
            self._debug_chat_state()
            print("  -> Fallback: пробуем нативный .click()...")
            visible_btn.click()
            wait.until(EC.visibility_of_element_located(message_locator))
            print("  -> Fallback сработал!")

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
        confirm_btn_locator = (By.XPATH, "//*[normalize-space(.)='Удалить']")

        try:
            confirm_btn = wait.until(
                EC.element_to_be_clickable(confirm_btn_locator)
            )
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

    def _debug_chat_state(self) -> None:
        """Печатает содержимое чата при неудачной отправке."""
        print("  -> ОШИБКА: сообщение не появилось. Отладка:")
        try:
            chat_text = self.driver.execute_script("""
                var el = document.querySelector('.chat-item-messages');
                return el ? el.innerText.substring(0, 500) : 'chat-item-messages not found';
            """)
            print(f"  -> Последние сообщения в чате:\n{chat_text}")
        except Exception as dbg_err:
            print(f"  -> Не удалось получить отладку: {dbg_err}")

