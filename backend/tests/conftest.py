import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def fast_config(monkeypatch):
    """Experiment config without the cooldown/timing frictions, for flow tests."""
    from app.services import experiment

    real = experiment.load_experiment_config()

    def patched():
        config = dict(real)
        config["enrollment_open"] = True
        config["session_cooldown_hours"] = 0
        config["min_sessions_before_shift"] = 1
        return config

    monkeypatch.setattr("app.services.experiment.load_experiment_config", patched)
    return patched()


@pytest.fixture
def mock_claude(monkeypatch):
    def fake_response(messages, style_profile):
        return {"text": f"[{style_profile}] mock response", "stop_reason": "end_turn"}

    monkeypatch.setattr("app.services.llm.get_claude_response", fake_response)
    return fake_response
