import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app  # adjust if your FastAPI app is elsewhere

client = TestClient(app)

# Set a test API key
os.environ["API_KEY"] = "test-key"
API_VERSION = os.environ.get('API_VERSION')


@pytest.fixture
def valid_headers():
    return {"x-api-key": "test-key"}


@pytest.fixture
def invalid_headers():
    return {"x-api-key": "wrong-key"}

# Test valid request


@patch("app.routes.appointments.API_KEY", "test-key")
@patch("app.routes.appointments.scrape_appointments_playwright_sync")
def test_fetch_appointments_success(mock_scrape, valid_headers):
    mock_scrape.return_value = [{"date": "2025-09-25", "location": "Berlin"}]

    response = client.get(f"{API_VERSION}/appointments", headers=valid_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Berlin"
    assert data["service"] == "Anmeldung"
    assert isinstance(data["slots"], list)
