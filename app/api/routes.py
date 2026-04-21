import httpx
from fastapi import APIRouter, HTTPException

from app.core.client import ask_llm_qa
from app.schemas.models import APIResponse, AskRequest

router = APIRouter()


@router.get("/health", response_model=APIResponse)
async def health() -> APIResponse:
    return APIResponse(success=True, data={"status": "ok"}, error=None)


@router.post("/api/ask", response_model=APIResponse)
async def api_ask(payload: AskRequest) -> APIResponse:
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
