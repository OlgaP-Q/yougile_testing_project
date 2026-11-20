"""Тест редактирования задачи на доске YouGile."""
import uuid

import pytest

from pages.board_page import BoardPage


@pytest.mark.ui
def test_edit_task_ui(logged_in_driver) -> None:
    print("\n--- ТЕСТ: Редактирование задачи ---")
    board_url = ("https://ru.yougile.com/"
                 "team/00cd725db8a1/%D0%B4%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC")
    old_name = f"Old Task {uuid.uuid4().hex[:6]}"
    new_name = f"New Task {uuid.uuid4().hex[:6]}"

    logged_in_driver.get(board_url)
    board_page = BoardPage(logged_in_driver)

    print(f"  -> Подготовка: создаем задачу '{old_name}'...")
    board_page.create_task(old_name)

    print(f"  -> Редактируем: '{old_name}' -> '{new_name}'...")
    board_page.edit_task(old_name, new_name)

    assert not board_page.is_task_visible(old_name), (
        "ОШИБКА: Задача со старым именем всё ещё видна!"
    )
    assert board_page.is_task_visible(new_name), (
        "ОШИБКА: Задача с новым именем не появилась!"
    )
    print("  -> ТЕСТ ПРОЙДЕН. Задача успешно переименована.")
