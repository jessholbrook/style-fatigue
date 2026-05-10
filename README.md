# Style Fatigue

An experiment investigating how quickly and why people habituate to AI model language style updates.

## Overview

This study examines which style dimensions (formulaicness, repetition, punctuation, formality, formatting, slang, trends) influence habituation speed, which habituations are beneficial vs. harmful, and how to predict them.

**Design**: Between-subjects, longitudinal (4-6 sessions over ~2 weeks). Participants start with a baseline Claude style and are shifted to a variant profile once habituation is detected via an adaptive trigger.

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

## Directory Structure

```
backend/       FastAPI server, database models, Claude API integration
frontend/      React + TypeScript participant-facing web app
experiment/    Style profiles, intent menus, survey instruments, config
analysis/      Jupyter notebooks and data export scripts
```

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
```

## Compensation

TBD — placeholder for participant compensation details.
