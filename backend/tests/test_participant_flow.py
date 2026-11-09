"""End-to-end participant flow with a mocked Claude."""

SURVEY = {
    "survey_type": "post_conversation",
    "responses": {"notice_change": 2, "preference": 5, "helpful": 6},
    "free_text": None,
}


def enroll(client):
    resp = client.post("/api/participants", json={})
    assert resp.status_code == 200
    body = resp.json()
    # Participant-facing payload must not reveal the condition
    assert "condition" not in body
    token = body["token"]
    assert client.post(f"/api/participants/{token}/consent", json={"agreed": True}).status_code == 200
    return token


def run_session(client, token, turns=5):
    resp = client.post(f"/api/participants/{token}/sessions")
    assert resp.status_code == 200, resp.json()
    body = resp.json()
    session = body["session"]
    assert "style_profile" not in session
    assert "is_shift_session" not in session

    intents = client.get(f"/api/participants/{token}/intents").json()["intents"]
    assert intents
    intent, topic = intents[0]["slug"], intents[0]["topics"][0]

    conv = client.post(
        f"/api/participants/{token}/sessions/{session['id']}/conversations",
        json={"intent": intent, "topic": topic},
    ).json()

    for i in range(turns):
        resp = client.post(
            f"/api/participants/{token}/sessions/{session['id']}/conversations/{conv['id']}/messages",
            json={"content": f"message {i}"},
        )
        assert resp.status_code == 200, resp.json()

    resp = client.post(
        f"/api/participants/{token}/sessions/{session['id']}/surveys", json=SURVEY
    )
    assert resp.status_code == 200, resp.json()
    return session, resp.json()


def test_full_participant_flow(client, fast_config, mock_claude):
    token = enroll(client)

    session1, _ = run_session(client, token)
    assert session1["session_number"] == 1

    # Session completed by the survey → session 2 unlocks (cooldown patched to 0)
    session2, _ = run_session(client, token)
    assert session2["session_number"] == 2

    participant = client.get(f"/api/participants/{token}").json()
    assert participant["completed_sessions"] == 2


def test_open_session_is_resumed_not_rejected(client, fast_config, mock_claude):
    token = enroll(client)

    first = client.post(f"/api/participants/{token}/sessions").json()
    assert first["resumed"] is False

    again = client.post(f"/api/participants/{token}/sessions").json()
    assert again["resumed"] is True
    assert again["session"]["id"] == first["session"]["id"]


def test_turn_limit_enforced_server_side(client, fast_config, mock_claude):
    token = enroll(client)
    session = client.post(f"/api/participants/{token}/sessions").json()["session"]
    conv = client.post(
        f"/api/participants/{token}/sessions/{session['id']}/conversations",
        json={"intent": "explain", "topic": "quantum_computing"},
    ).json()

    url = f"/api/participants/{token}/sessions/{session['id']}/conversations/{conv['id']}/messages"
    for i in range(5):
        assert client.post(url, json={"content": f"m{i}"}).status_code == 200
    assert client.post(url, json={"content": "one too many"}).status_code == 409


def test_duplicate_survey_rejected(client, fast_config, mock_claude):
    token = enroll(client)
    session, _ = run_session(client, token)
    resp = client.post(
        f"/api/participants/{token}/sessions/{session['id']}/surveys", json=SURVEY
    )
    assert resp.status_code == 409


def test_likert_out_of_range_rejected(client, fast_config, mock_claude):
    token = enroll(client)
    session = client.post(f"/api/participants/{token}/sessions").json()["session"]
    bad = {"survey_type": "post_conversation", "responses": {"notice_change": 9}}
    resp = client.post(
        f"/api/participants/{token}/sessions/{session['id']}/surveys", json=bad
    )
    assert resp.status_code == 422


def test_topics_not_repeated_across_sessions(client, fast_config, mock_claude):
    token = enroll(client)

    before = client.get(f"/api/participants/{token}/intents").json()["intents"]
    used_topic = before[0]["topics"][0]

    run_session(client, token)  # run_session picks intents[0].topics[0]

    after = client.get(f"/api/participants/{token}/intents").json()["intents"]
    remaining_topics = [t for i in after for t in i["topics"]]
    assert used_topic not in remaining_topics


def test_events_endpoint_records(client, fast_config, mock_claude):
    token = enroll(client)
    resp = client.post(
        f"/api/participants/{token}/events",
        json={"event_type": "page_view", "payload": {"page": "landing"}},
    )
    assert resp.status_code == 204


def test_enrollment_pause_blocks_new_participants_only(client, fast_config, mock_claude, monkeypatch):
    token = enroll(client)  # enrolled while open

    closed = dict(fast_config, enrollment_open=False)
    monkeypatch.setattr("app.services.experiment.load_experiment_config", lambda: closed)

    resp = client.post("/api/participants", json={})
    assert resp.status_code == 503
    assert resp.json()["detail"]["reason"] == "enrollment_closed"

    # Already-enrolled participants can still run their sessions
    assert client.post(f"/api/participants/{token}/sessions").status_code == 200


def test_shipped_config_has_recruitment_paused(client):
    resp = client.post("/api/participants", json={})
    assert resp.status_code == 503
