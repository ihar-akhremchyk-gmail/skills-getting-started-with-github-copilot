import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a test client with a fresh app instance for each test"""
    return TestClient(app)
