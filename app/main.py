import logging.config
from pathlib import Path

from fastapi import FastAPI, Response
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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    # Avoid repeated browser 404 noise for favicon requests.
    return Response(status_code=204)


app.include_router(router)

static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
