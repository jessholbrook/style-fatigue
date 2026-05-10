# Style Fatigue — Claude Code Guide

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL
- **Frontend**: React 18, TypeScript, Vite
- **LLM**: Anthropic Claude API (via `anthropic` Python SDK)
- **Infra**: Docker Compose (local), Railway (production)

## Commands

```bash
# Run backend tests
cd backend && pytest

# Run frontend tests
cd frontend && npm test

# Lint
cd backend && ruff check .
cd frontend && npm run lint

# Database migrations
cd backend && alembic upgrade head
cd backend && alembic revision --autogenerate -m "description"
```

## Architecture

- Between-subjects design: each participant assigned one condition
- Auth by unique URL token — no login, no cookies, no PII
- Frontend never knows about conditions; backend decides style profile per session
- Survey instruments and style profiles are JSON data files in `experiment/`
- Adaptive shift trigger: backend monitors noticeability + preference stability
- Comprehensive event logging in `event_log` table (client + server timestamps)
- JSONB columns for flexible data (messages, survey responses, event payloads)

## Conventions

- Participant routes are nested under `/api/participants/{token}/`
- All API routes prefixed with `/api/`
- Pydantic schemas in `backend/app/schemas/`, DB models in `backend/app/models/`
- Experiment config is data, not code — edit JSON files in `experiment/`
