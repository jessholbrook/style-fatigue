from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

# backend/app/config.py -> parents[2] is the repo root locally and / in the
# backend container, where compose mounts ./experiment at /experiment.
REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://stylefatigue:stylefatigue@localhost:5432/stylefatigue"
    ANTHROPIC_API_KEY: str = ""
    SECRET_KEY: str = "change-me-in-production"
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str = "http://localhost:5173"
    EXPERIMENT_CONFIG_PATH: str = str(REPO_ROOT / "experiment")
    # When set (production), FastAPI serves the built frontend from this dir
    FRONTEND_DIST_PATH: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
