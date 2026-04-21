import os


class Settings:
    llm_qa_endpoint: str = os.getenv("LLM_QA_ENDPOINT", "https://llm-qa.acion.es/ask")
    llm_qa_secret: str = os.getenv("LLM_QA_SECRET", "")
    tester_ui_password: str = os.getenv("TESTER_UI_PASSWORD", "")
    tester_session_secret: str = os.getenv("TESTER_SESSION_SECRET", "change-me")
    tester_session_days: int = int(os.getenv("TESTER_SESSION_DAYS", "30"))
    tester_cookie_secure: bool = os.getenv("TESTER_COOKIE_SECURE", "false").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "180"))
    upstream_max_retries: int = int(os.getenv("UPSTREAM_MAX_RETRIES", "2"))
    upstream_retry_delay_seconds: float = float(
        os.getenv("UPSTREAM_RETRY_DELAY_SECONDS", "1.0")
    )


settings = Settings()
