"""Тест отправки сообщения в существующий чат YouGile."""
import os

import pytest

from pages.chat_page import ChatPage


@pytest.mark.ui
def test_send_message_ui(driver, chat_env, unique_message):
    """
    E2E: отправка сообщения в чат, созданный фикстурой chat_env.

    Фикстура chat_env:
      - логинит пользователя через logged_in_driver;
      - открывает Мессенджер;
      - создаёт уникальный чат 'Autotest-XXXXXX';
      - отдаёт имя чата через yield;
      - удаляет чат после теста (teardown).

    Тест независим: не требует предварительно созданных чатов,
    убирает за собой и может запускаться параллельно с другими.
    """
    os.makedirs("screenshots", exist_ok=True)
    print("\n--- ТЕСТ: Отправка сообщения в чат ---")

    chat_page = ChatPage(driver)

    try:
        print(f"  -> Отправка в чат '{chat_env}'...")
        chat_page.send_message_to_existing_chat(chat_env, unique_message)
        print("  -> ТЕСТ ПРОЙДЕН.")
    except Exception:
        driver.save_screenshot("screenshots/error_send_message.png")
        raise
