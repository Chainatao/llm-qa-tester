import hashlib
import hmac
import time

import httpx
from fastapi import APIRouter, HTTPException, Request, Response, status

from app.core.client import ask_llm_qa
from app.schemas.models import APIResponse, AskRequest, LoginRequest
from app.utils.config import settings

router = APIRouter()
AUTH_COOKIE_NAME = "llmqa_tester_auth"


def _build_auth_token(expires_at: int) -> str:
    payload = str(expires_at)
    signature = hmac.new(
        settings.tester_session_secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}.{signature}"


def _is_request_authenticated(request: Request) -> bool:
    token = request.cookies.get(AUTH_COOKIE_NAME, "")
    if not token or "." not in token:
        return False

    payload, provided_sig = token.rsplit(".", 1)
    expected_sig = hmac.new(
        settings.tester_session_secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(provided_sig, expected_sig):
        return False

    try:
        expires_at = int(payload)
    except ValueError:
        return False

    return time.time() < expires_at


@router.get("/health", response_model=APIResponse)
async def health() -> APIResponse:
    return APIResponse(success=True, data={"status": "ok"}, error=None)


@router.get("/api/auth/status", response_model=APIResponse)
async def auth_status(request: Request) -> APIResponse:
    authenticated = _is_request_authenticated(request)
    return APIResponse(success=True, data={"authenticated": authenticated}, error=None)


@router.post("/api/auth/login", response_model=APIResponse)
async def auth_login(payload: LoginRequest, response: Response) -> APIResponse:
    if not settings.tester_ui_password:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="TESTER_UI_PASSWORD is not configured",
        )

    if not hmac.compare_digest(payload.password, settings.tester_ui_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    expires_at = int(time.time()) + (settings.tester_session_days * 24 * 60 * 60)
    token = _build_auth_token(expires_at)
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,
        max_age=settings.tester_session_days * 24 * 60 * 60,
        httponly=True,
        samesite="lax",
        secure=settings.tester_cookie_secure,
    )

    return APIResponse(success=True, data={"authenticated": True}, error=None)


@router.post("/api/auth/logout", response_model=APIResponse)
async def auth_logout(response: Response) -> APIResponse:
    response.delete_cookie(AUTH_COOKIE_NAME)
    return APIResponse(success=True, data={"authenticated": False}, error=None)


@router.post("/api/ask", response_model=APIResponse)
async def api_ask(payload: AskRequest, request: Request) -> APIResponse:
    if not _is_request_authenticated(request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    try:
        upstream = await ask_llm_qa(payload.question, payload.options)
        return APIResponse(success=True, data=upstream, error=None)
    except httpx.HTTPStatusError as exc:
        body = exc.response.text
        detail = f"Upstream returned {exc.response.status_code}: {body}"
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream connection error: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
