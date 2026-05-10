from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import conversations, participants, sessions, surveys


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    print(f"Starting style-fatigue backend ({settings.ENVIRONMENT})")
    yield
    print("Shutting down style-fatigue backend")


app = FastAPI(title="Style Fatigue", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[get_settings().FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(participants.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")
app.include_router(conversations.router, prefix="/api")
app.include_router(surveys.router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
