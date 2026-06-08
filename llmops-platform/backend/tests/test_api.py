"""
Basic API tests
Run with: pytest tests/test_api.py
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_docs():
    """Test API documentation"""
    response = client.get("/docs")
    assert response.status_code == 200
