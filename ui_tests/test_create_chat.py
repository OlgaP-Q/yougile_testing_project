import uuid
import pytest
from pages.chat_page import ChatPage


@pytest.mark.ui
def test_create_chat_ui(logged_in_driver):
    """
    E2E: создание нового чата и проверка его появления в списке.

    Использует фикстуру logged_in_driver (логин уже выполнен).
    Генерирует уникальное имя, чтобы не пересекаться с другими тестами.
    В блоке finally гарантированно удаляет созданный чат.
    """
    print("\n--- ТЕСТ: Создание нового чата ---")

    chat_page = ChatPage(logged_in_driver)
    chat_name = f"Autotest-{uuid.uuid4().hex[:6]}"

    try:
        print("  -> Переходим в Мессенджер...")
        chat_page.open_messenger()

        print(f"  -> Создаем чат '{chat_name}'...")
        chat_page.create_group_chat(chat_name)

        print("  -> ПРОВЕРКА: ищем чат в списке...")
        # Утверждение (assert), что чат реально появился в списке
        assert chat_page.is_chat_visible(chat_name), (
            f"ОШИБКА: Чат '{chat_name}' не появился в списке после создания!"
        )

        print("  -> ТЕСТ ПРОЙДЕН. Чат успешно создан.")

    finally:
        # Обязательный шаг: удаляем чат, чтобы не засорять аккаунт
        print(f"  -> [teardown] Удаляем тестовый чат '{chat_name}'...")
        try:
            chat_page.delete_chat(chat_name)
        except Exception as e:
            print(f"  -> [teardown] Не удалось удалить чат: {e}")
