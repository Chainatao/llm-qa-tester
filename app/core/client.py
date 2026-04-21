import asyncio
import httpx

from app.utils.config import settings


async def ask_llm_qa(question: str, options: str | None) -> dict:
    if not settings.llm_qa_secret:
        raise RuntimeError("LLM_QA_SECRET is not configured")

    payload = {
        "question": question,
        "secret": settings.llm_qa_secret,
    }
    if options:
        payload["options"] = options

    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        for attempt in range(settings.upstream_max_retries + 1):
            try:
                response = await client.post(settings.llm_qa_endpoint, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                body = exc.response.text or ""
                is_upstream_timeout = (
                    exc.response.status_code in {500, 502, 503, 504}
                    and "Request timed out" in body
                )
                if attempt >= settings.upstream_max_retries or not is_upstream_timeout:
                    raise
                await asyncio.sleep(settings.upstream_retry_delay_seconds * (attempt + 1))
            except httpx.RequestError:
                if attempt >= settings.upstream_max_retries:
                    raise
                await asyncio.sleep(settings.upstream_retry_delay_seconds * (attempt + 1))
