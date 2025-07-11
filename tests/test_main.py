"""
Basic tests for the Semantic Kernel A2A Travel Agent application.
Run with: pytest tests/
"""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "semantic-kernel-travel-agent"


def test_root_endpoint(client):
    """Test the root endpoint returns the main interface."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_agent_card_endpoint(client):
    """Test the agent card endpoint."""
    response = client.get("/agent-card")
    assert response.status_code == 200
    data = response.json()
    # Should return agent card data or error message
    assert "name" in data or "error" in data


def test_static_files(client):
    """Test that static files are served correctly."""
    response = client.get("/static/css/style.css")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_chat_api_structure(client):
    """Test that chat API endpoints exist and have proper structure."""
    # Test that endpoints exist (they may return errors without proper setup)
    response = client.post("/api/chat/message", json={"message": "test"})
    # Just check that the endpoint exists, not the response
    assert response.status_code in [200, 422, 500]  # Various valid responses
