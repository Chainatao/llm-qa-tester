from typing import Any, Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=5, description="Question text to test against llm-qa")
    options: Optional[str] = Field(None, description="Optional A/B/C/D options block")


class LoginRequest(BaseModel):
    password: str = Field(..., min_length=1, description="Password to access tester UI")


class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
