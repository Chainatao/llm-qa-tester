import os


class Settings:
    llm_qa_endpoint: str = os.getenv("LLM_QA_ENDPOINT", "https://llm-qa.acion.es/ask")
    llm_qa_secret: str = os.getenv("LLM_QA_SECRET", "")
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "180"))
    upstream_max_retries: int = int(os.getenv("UPSTREAM_MAX_RETRIES", "2"))
    upstream_retry_delay_seconds: float = float(
        os.getenv("UPSTREAM_RETRY_DELAY_SECONDS", "1.0")
    )


settings = Settings()
