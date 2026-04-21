import os


class Settings:
    llm_qa_endpoint: str = os.getenv("LLM_QA_ENDPOINT", "https://llm-qa.acion.es/ask")
    llm_qa_secret: str = os.getenv("LLM_QA_SECRET", "")
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "60"))


settings = Settings()
