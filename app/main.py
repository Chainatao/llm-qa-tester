import logging.config
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "json": {
                "format": '{"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","message":"%(message)s"}'
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
            }
        },
        "root": {"handlers": ["console"], "level": "INFO"},
    }
)

app = FastAPI(
    title="LLM QA Tester",
    description="Simple frontend and proxy API to test llm-qa endpoint.",
    version="1.0.0",
)

app.include_router(router)

static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
