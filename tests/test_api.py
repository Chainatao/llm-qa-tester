import os
import pytest

from fastapi.testclient import TestClient

os.environ.setdefault("LLM_QA_SECRET", "dummy")
os.environ.setdefault("TESTER_UI_PASSWORD", "ui-pass")
os.environ.setdefault("TESTER_SESSION_SECRET", "session-signing-secret")

from app.main import app  # noqa: E402
from app.api import routes as api_routes  # noqa: E402


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


def test_ask_requires_auth_cookie() -> None:
    response = client.post("/api/ask", json={"question": "Legal question"})
    assert response.status_code == 401


def test_login_and_ask_success(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_ask_llm_qa(question: str, options: str | None) -> dict:
        return {
            "success": True,
            "data": {
                "route": {"category": "legal", "confidence": 0.99, "rationale": "test"},
                "answer": {"response": 1, "phase_used": "fase_1_literal", "reasoning": "ok"},
            },
            "error": None,
        }

    monkeypatch.setattr(api_routes, "ask_llm_qa", fake_ask_llm_qa)

    login_response = client.post("/api/auth/login", json={"password": "ui-pass"})
    assert login_response.status_code == 200
    assert login_response.json()["success"] is True

    ask_response = client.post("/api/ask", json={"question": "Legal question"})
    assert ask_response.status_code == 200
    body = ask_response.json()
    assert body["success"] is True
    assert body["data"]["success"] is True
