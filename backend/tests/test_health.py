def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_public_config_excludes_shift_criteria(client):
    response = client.get("/api/config")
    assert response.status_code == 200
    body = response.json()
    assert "max_sessions" in body
    assert "shift_criteria" not in body


def test_survey_instrument_path_traversal_rejected(client):
    response = client.get("/api/surveys/..%2F..%2Fconfig")
    assert response.status_code == 404
