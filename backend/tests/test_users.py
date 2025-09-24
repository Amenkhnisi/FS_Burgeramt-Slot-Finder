from fastapi.testclient import TestClient
from app.main import app
import os
from app.utils.auth_utils import get_current_user
import pytest

client = TestClient(app)

API_VERSION = os.environ.get('API_VERSION')

# Mock user


@pytest.fixture
def override_auth():
    class MockUser:
        id = 1
        username = "amen"
        email = "amen@example.com"
    app.dependency_overrides[get_current_user] = lambda: MockUser()
    yield
    app.dependency_overrides.pop(get_current_user, None)


def test_get_me():
    response = client.get(f"{API_VERSION}/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "amen"
    assert data["email"] == "amen@example.com"
