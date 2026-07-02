from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.middleware.timing import TimingMiddleware
from app.routers import conversations, participants, sessions, study, surveys


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    print(f"Starting style-fatigue backend ({settings.ENVIRONMENT})")
    yield
    print("Shutting down style-fatigue backend")


app = FastAPI(title="Style Fatigue", lifespan=lifespan)

app.add_middleware(TimingMiddleware)
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
app.include_router(study.router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


# Production single-service mode: serve the built frontend. /api routes are
# registered above and take precedence; everything else falls back to the SPA.
_dist = Path(get_settings().FRONTEND_DIST_PATH) if get_settings().FRONTEND_DIST_PATH else None
if _dist and _dist.exists():
    app.mount("/assets", StaticFiles(directory=_dist / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def spa_fallback(path: str):
        if path.startswith("api"):
            raise HTTPException(status_code=404)
        return FileResponse(_dist / "index.html")
