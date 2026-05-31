import json
import os
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def obs_path(tmp_path, monkeypatch):
    path = str(tmp_path / "observation_events.jsonl")
    monkeypatch.setattr("perf.perf_app.OBS_EVENTS_PATH", path)
    return path


@pytest.fixture()
def client(obs_path):
    from perf.perf_app import app
    return TestClient(app)


def _flat_event(strategy_id="SMC_ICT_CHOCH_BOS_RETEST"):
    return {"strategy_id": strategy_id, "signal": {"direction": "LONG_WATCH", "confidence": 0.65}}


def _nested_event(strategy_id="SMC_ICT_CHOCH_BOS_RETEST"):
    return {
        "strategy": {"strategy_id": strategy_id, "strategy_version": "0.1.0"},
        "signal": {"direction": "SHORT_WATCH", "confidence": 0.70},
    }


# --- POST /perf/observation_event ---

def test_post_flat_strategy_id_returns_200(client):
    r = client.post("/perf/observation_event", json=_flat_event())
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_post_nested_strategy_id_returns_200(client):
    r = client.post("/perf/observation_event", json=_nested_event())
    assert r.status_code == 200
    assert r.json()["strategy_id"] == "SMC_ICT_CHOCH_BOS_RETEST"


def test_post_missing_strategy_id_returns_400(client):
    r = client.post("/perf/observation_event", json={"signal": {"confidence": 0.5}})
    assert r.status_code == 400


def test_post_adds_produced_at_when_absent(client, obs_path):
    r = client.post("/perf/observation_event", json=_flat_event())
    assert r.status_code == 200
    stored = json.loads(open(obs_path).read().strip())
    assert "produced_at" in stored


def test_post_preserves_produced_at_when_present(client, obs_path):
    ev = _flat_event()
    ev["produced_at"] = "2026-05-30T10:00:00+00:00"
    r = client.post("/perf/observation_event", json=ev)
    assert r.status_code == 200
    stored = json.loads(open(obs_path).read().strip())
    assert stored["produced_at"] == "2026-05-30T10:00:00+00:00"


def test_post_response_contains_event_id(client):
    r = client.post("/perf/observation_event", json=_flat_event())
    body = r.json()
    assert "event_id" in body
    assert body["event_id"].startswith("OE_")


def test_post_persists_to_jsonl(client, obs_path):
    client.post("/perf/observation_event", json=_flat_event())
    client.post("/perf/observation_event", json=_nested_event())
    lines = open(obs_path).read().strip().splitlines()
    assert len(lines) == 2


# --- GET /perf/strategy/{strategy_id}/promotion_gate ---

def test_get_promotion_gate_no_events_returns_insufficient_sample(client):
    r = client.get("/perf/strategy/SMC_ICT_CHOCH_BOS_RETEST/promotion_gate")
    assert r.status_code == 200
    body = r.json()
    assert body["promotion_gate"]["verdict"] == "INSUFFICIENT_SAMPLE"


def test_get_promotion_gate_wrong_strategy_returns_insufficient_sample(client):
    client.post("/perf/observation_event", json=_flat_event("OTHER_STRATEGY"))
    r = client.get("/perf/strategy/SMC_ICT_CHOCH_BOS_RETEST/promotion_gate")
    assert r.json()["sample_size"] == 0


def test_get_promotion_gate_returns_strategy_id(client):
    r = client.get("/perf/strategy/SMC_ICT_CHOCH_BOS_RETEST/promotion_gate")
    assert r.json()["strategy_id"] == "SMC_ICT_CHOCH_BOS_RETEST"


def test_get_promotion_gate_returns_total_events_loaded(client):
    client.post("/perf/observation_event", json=_flat_event())
    client.post("/perf/observation_event", json=_flat_event("OTHER"))
    r = client.get("/perf/strategy/SMC_ICT_CHOCH_BOS_RETEST/promotion_gate")
    assert r.json()["total_events_loaded"] == 2


def test_get_promotion_gate_counts_correct_strategy_only(client):
    for _ in range(3):
        client.post("/perf/observation_event", json=_flat_event("SMC_ICT_CHOCH_BOS_RETEST"))
    client.post("/perf/observation_event", json=_flat_event("OTHER"))
    r = client.get("/perf/strategy/SMC_ICT_CHOCH_BOS_RETEST/promotion_gate")
    assert r.json()["sample_size"] == 3
