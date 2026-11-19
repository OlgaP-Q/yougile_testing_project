"""Тест создания задачи на доске YouGile."""
import uuid

import pytest

from pages.board_page import BoardPage


@pytest.mark.ui
def test_create_task_ui(logged_in_driver) -> None:
    """
    E2E: создание новой задачи на доске.

    Использует фикстуру logged_in_driver (уже авторизован).
    Генерирует уникальное имя задачи, чтобы избежать ложных срабатываний
    при повторных запусках.
    """
    print("\n--- ТЕСТ: Создание задачи ---")

    board_url = (
        "https://ru.yougile.com/team/00cd725db8a1/"
        "%D0%B4%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC"
    )
    task_name = f"Autotest Task {uuid.uuid4().hex[:6]}"

    print("  -> Переходим на доску...")
    logged_in_driver.get(board_url)

    board_page = BoardPage(logged_in_driver)

    print(f"  -> Создаем задачу '{task_name}'...")
    board_page.create_task(task_name)

    print("  -> ПРОВЕРКА: ищем задачу на доске...")
    assert board_page.is_task_visible(task_name), (
        f"ОШИБКА: Задача '{task_name}' не появилась на доске!"
    )

    print("  -> ТЕСТ ПРОЙДЕН. Задача создана.")
