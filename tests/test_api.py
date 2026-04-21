import os

from fastapi.testclient import TestClient

os.environ.setdefault("LLM_QA_SECRET", "dummy")

from app.main import app  # noqa: E402


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"


def test_ui_served() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "LLM QA Tester" in response.text
