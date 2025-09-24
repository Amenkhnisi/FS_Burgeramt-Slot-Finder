from fastapi.testclient import TestClient
from app.main import app as real_app
from app.utils.auth_utils import get_current_user


def get_test_client(with_auth=True):
    app = real_app
    if with_auth:
        class MockUser:
            id = 1
            username = "amen"
            email = "amen@example.com"
        app.dependency_overrides[get_current_user] = lambda: MockUser()
    else:
        app.dependency_overrides.pop(get_current_user, None)
    return TestClient(app)
