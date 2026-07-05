# Style Fatigue

An experiment investigating how quickly and why people habituate to AI model language style updates.

## Overview

This study examines which style dimensions (formulaicness, repetition, punctuation, formality, formatting, slang, trends) influence habituation speed, which habituations are beneficial vs. harmful, and how to predict them.

**Design**: Between-subjects, longitudinal (4-6 sessions over ~2 weeks). Participants are randomized at enrollment (blocked randomization) into control, variant A, or variant B. Everyone starts on a baseline Claude style; once an adaptive trigger detects habituation (stable **and low** noticeability plus stable satisfaction across 3 sessions), variant-arm participants are shifted to their assigned style profile. Control-arm participants stay on baseline but are stamped with a pseudo-shift marker at the same trigger point, providing the false-positive detection baseline.

**Scope note (Study 1)**: the two variants each bundle several style dimensions (formality, formatting, punctuation, etc.), so Study 1 supports claims at the style-*bundle* level only. Isolating which individual dimension drives habituation requires single-dimension variants — a Study 2 design.

## Interactive demo

An [interactive study-flow demo](https://claude.ai/code/artifact/03f20a7f-83c9-4d54-b232-c947ae8c408c) walks through the participant experience (left) alongside the researcher view (right): condition assignment, the live shift-trigger metrics, the session timeline, and the event stream. It uses canned responses drawn from the three real style profiles and the actual trigger math — no live API calls.

> Note: the demo is a private claude.ai artifact; viewers may need to be granted access to open it.

## Prerequisites

- Docker & Docker Compose
- Node.js 22+
- Python 3.11+

## Quickstart

```bash
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
docker compose up
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

## Directory structure

```
backend/               FastAPI server (Python 3.11, SQLAlchemy 2.0, Alembic)
  app/
    models/            SQLAlchemy models (participant, session, conversation, survey, event_log)
    schemas/           Pydantic request/response schemas
    routers/           API routes (participants, sessions, conversations, surveys, study)
    services/          Claude integration, condition assignment, shift trigger, event logging
    middleware/        Request timing
  alembic/             Database migrations
  tests/               pytest suite (incl. end-to-end participant flow)
frontend/              React 18 + TypeScript + Vite + Tailwind/shadcn participant app
  src/                 Pages, components, hooks, API client
  tests/               vitest component tests
experiment/            Experiment config as data (not code)
  style_profiles/      baseline, variant_a, variant_b (system prompts + few-shot)
  survey_instruments/  post_conversation (masked), exit_survey (funnel debrief)
  intents.json         Intent + topic menu
  config.json          Conditions, shift criteria, session limits, model settings
analysis/
  scripts/             export_data, preview_profiles, power_analysis
  notebooks/           Data-quality and habituation-curve notebooks
  output/              Generated tables (e.g. power_analysis.md)
.github/workflows/     CI (ci.yml)
Dockerfile             Production image (builds frontend, served by backend)
railway.toml           Railway deployment config
```

## How the study works

- **Auth by unique URL token** — no login, no cookies, no PII. Participant routes are nested under `/api/participants/{token}/`.
- **Backend decides the style profile** per session and **never sends condition or style fields to the frontend** — participants can't unblind themselves from the network tab.
- **Adaptive shift trigger** ([`services/shift.py`](backend/app/services/shift.py)) monitors noticeability + satisfaction stability; assignment uses blocked randomization ([`services/experiment.py`](backend/app/services/experiment.py)).
- **Comprehensive event logging** — the `event_log` table captures client + server timestamps for page views, messages, surveys, and shift events, feeding the behavioral measures.
- **Config as data** — style profiles, intents, and survey instruments are JSON files in `experiment/`; edit them without touching code.

## Development

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install
npm run dev

# Database migrations
cd backend && alembic upgrade head
cd backend && alembic revision --autogenerate -m "description"
```

### Testing & CI

```bash
cd backend && pytest          # backend suite, incl. mocked end-to-end flow
cd backend && ruff check .     # backend lint
cd frontend && npm test        # vitest component tests
cd frontend && npm run lint    # eslint
```

CI (`.github/workflows/ci.yml`) runs all of the above on every pull request and push to `main`: the backend job also renders the migration SQL, and the frontend job also runs `npm run build`.

## API

All routes are prefixed with `/api`. Participant-facing routes are token-scoped under `/api/participants/{token}/...` and resolve ownership on every request; `GET /api/config` and `GET /api/surveys/{survey_type}` are public. The full interactive reference (FastAPI Swagger) is auto-generated at [`/docs`](http://localhost:8000/docs).

## Deployment (Railway)

Production runs as a single service: the root `Dockerfile` builds the frontend and the
FastAPI backend serves it (SPA fallback), with migrations applied on boot.

1. Create a Railway project from this repo — `railway.toml` configures the build and `/api/health` healthcheck
2. Add the PostgreSQL addon; Railway injects `DATABASE_URL`
3. Set `ANTHROPIC_API_KEY` and a real `SECRET_KEY` (it seeds condition randomization — set it once before enrolling anyone and never change it mid-study)

## Analysis & piloting

The `analysis/scripts/` tools:

- **`preview_profiles.py`** — manipulation check: generates side-by-side sample responses per style profile so you can confirm the three are perceptibly distinct (needs `ANTHROPIC_API_KEY`).
- **`power_analysis.py`** — prints two-proportion power tables for the primary detection-rate contrast and writes them to `analysis/output/power_analysis.md` (stdlib only).
- **`export_data.py`** — exports the database tables to CSV for the notebooks.

The `analysis/notebooks/` cover data-quality checks and habituation curves.

Before recruiting:

```bash
# Manipulation check: are the three style profiles perceptibly distinct?
ANTHROPIC_API_KEY=... python analysis/scripts/preview_profiles.py

# Sample size: prints power tables for the detection-rate contrast
python analysis/scripts/power_analysis.py
```

## Compensation

TBD — placeholder for participant compensation details.
