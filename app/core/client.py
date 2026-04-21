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
        response = await client.post(settings.llm_qa_endpoint, json=payload)
        response.raise_for_status()
        return response.json()
