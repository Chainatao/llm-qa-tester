# llm-qa-tester

Deployable FastAPI microservice with a simple frontend to test the llm-qa question endpoint.

This service provides:
- A browser UI to paste a question and optional options block.
- A backend proxy endpoint that calls `llm-qa /ask` server-side.
- Secret handling on the server side (no secret exposed in browser JS).

## DSRS Compliance Notes

- Independent repository structure.
- FastAPI entrypoint at `app/main.py`.
- ASGI runtime via `gunicorn + uvicorn worker`.
- Dockerized service exposing port `8000`.
- GitHub Actions workflow for GHCR image publish.
- Traefik-compatible labels in `docker-compose.yml`.
- `docker-compose.yml` uses modern Compose format with no `version` field.

## Project Structure

```
llm-qa-tester/
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── schemas/
│   ├── utils/
│   └── static/
├── tests/
├── Dockerfile
├── requirements.txt
├── .env.example
├── docker-compose.yml
└── .github/workflows/deploy.yml
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```dotenv
LLM_QA_ENDPOINT=https://llm-qa.acion.es/ask
LLM_QA_SECRET=your_llm_qa_api_secret
REQUEST_TIMEOUT_SECONDS=60
```

## Local Run

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:
- `http://localhost:8000/`

API endpoints:
- `GET /health`
- `POST /api/ask`

## First-Time Server Setup (Minimal)

1. Copy only `docker-compose.yml` to `/opt/services/llm-qa-tester`
2. Ensure runtime env vars exist on server (`LLM_QA_ENDPOINT`, `LLM_QA_SECRET`)
3. Start:

```bash
cd /opt/services/llm-qa-tester
docker compose up -d
```

## Deploy With GHCR + Traefik

- Push to `main` to trigger `.github/workflows/deploy.yml`.
- Image will be published to `ghcr.io/<org-or-user>/llm-qa-tester:latest`.
- Configure host rule in compose labels, e.g. `llm-qa-tester.acion.es`.

## Example API Call

```bash
curl -X POST "https://llm-qa-tester.acion.es/api/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Según el artículo 70 de la LPAC...",
    "options": "A. ...\nB. ...\nC. ...\nD. ..."
  }'
```
