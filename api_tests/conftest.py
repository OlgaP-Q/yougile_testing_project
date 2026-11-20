import pytest
from config import API_URL, API_TOKEN


@pytest.fixture(scope="session")
def base_url() -> str:
    return API_URL


@pytest.fixture(scope="session")
def headers() -> dict:
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
