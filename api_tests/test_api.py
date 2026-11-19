import requests
from config import TEST_COLUMN_ID, TEST_PROJECT_ID, TEST_USER_ID


def test_create_task(base_url: str, headers: dict) -> None:
    """API-01: Позитивный. Создание задачи."""
    payload = {"title": "Задача из API-автотеста", "columnId":  TEST_COLUMN_ID}
    response = requests.post(
        f"{base_url}/tasks", headers=headers, json=payload
    )

    assert response.status_code == 201
    assert "id" in response.json()


def test_update_task(base_url: str, headers: dict) -> None:
    """API-02: Позитивный. Изменение задачи."""
    # Создаем задачу для теста (обеспечиваем независимость)
    create_payload = {
        "title": "Задача для изменения", "columnId": TEST_COLUMN_ID
    }
    create_response = requests.post(
        f"{base_url}/tasks", headers=headers, json=create_payload
    )
    task_id = create_response.json()["id"]

    # Меняем её
    update_payload = {"title": "Обновленная задача"}
    update_response = requests.put(
        f"{base_url}/tasks/{task_id}", headers=headers, json=update_payload
    )

    assert update_response.status_code == 200


def test_create_chat(base_url: str, headers: dict) -> None:
    """API-03: Позитивный. Создание группового чата."""
    payload = {
        "title": "API Чат из автотеста",
        "users":    {TEST_USER_ID: {"notified": True}},
        "userRoleMap": {TEST_USER_ID: "admin"},
        "roleConfigMap": {"admin": {"notified": True}}
    }
    response = requests.post(
        f"{base_url}/group-chats", headers=headers, json=payload
    )

    assert response.status_code == 201
    assert "id" in response.json()


def test_get_project_roles(base_url: str, headers: dict) -> None:
    """API-04: Позитивный. Получение списка ролей проекта."""
    response = requests.get(
        f"{base_url}/projects/{TEST_PROJECT_ID}/roles", headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json().get("content"), list)


def test_get_tasks_list(base_url: str, headers: dict) -> None:
    """API-05: Позитивный. Получение списка задач."""
    response = requests.get(
        f"{base_url}/tasks?columnId={TEST_COLUMN_ID}", headers=headers
    )

    assert response.status_code == 200
    assert "content" in response.json()


def test_create_task_empty_title(base_url: str, headers: dict) -> None:
    """API-06: Негативный. Создание задачи с пустым названием."""
    payload = {"title": "", "columnId": TEST_COLUMN_ID}
    response = requests.post(
        f"{base_url}/tasks", headers=headers, json=payload
    )

    assert response.status_code == 400  # Ошибка валидации


def test_create_task_without_token(base_url: str) -> None:
    """API-07: Негативный. Создание задачи без токена."""
    bad_headers = {"Content-Type": "application/json"}
    payload = {"title": "Задача без токена", "columnId": TEST_COLUMN_ID}

    response = requests.post(
        f"{base_url}/tasks", headers=bad_headers, json=payload
    )

    assert response.status_code == 401  # Ошибка авторизации
