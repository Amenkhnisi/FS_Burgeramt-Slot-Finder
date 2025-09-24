# tests/conftest.py
import pytest
from app.main import app
from app.utils.auth_utils import get_current_user  # adjust path if needed


@pytest.fixture(scope="session", autouse=True)
def override_auth():
    class MockUser:
        id = 1
        username = "amen"
        email = "amen@example.com"

    app.dependency_overrides[get_current_user] = lambda: MockUser()
