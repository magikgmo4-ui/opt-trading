from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.trading_realtime_v1.app import runtime_loop_v1


LIVE_RECORD = {
    "record_ts": "2026-04-05T18:05:00-04:00",
    "local_date": "2026-04-05",
    "session_name": "open_1800",
    "variant_id": "xau_open_sweep_fvg",
    "direction": "bearish",
    "entry": 3187.0,
    "sl": 3208.0,
    "rr_planned": 2.0,
    "source": "sample_live_reference_v1.jsonl",
}


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


@pytest.fixture
def isolated_runtime_loop_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    state_dir = tmp_path / "state" / "trading_realtime_v1"
    live_source = tmp_path / "sample_live_reference_v1.jsonl"
    observations = state_dir / "runtime_observations_v1.jsonl"
    runs = state_dir / "runtime_runs_v1.jsonl"
    events = state_dir / "runtime_events_v1.jsonl"
    bridge_runs = state_dir / "runtime_bridge_runs_v1.jsonl"
    reports = state_dir / "runtime_reports_v1.jsonl"
    loop_runs = state_dir / "runtime_loop_runs_v1.jsonl"

    write_jsonl(live_source, [LIVE_RECORD])

    monkeypatch.setattr(runtime_loop_v1, "LIVE_SOURCE_PATH", live_source)
    monkeypatch.setattr(runtime_loop_v1, "STATE_DIR", state_dir)
    monkeypatch.setattr(runtime_loop_v1, "RUNTIME_OBSERVATIONS_JSONL", observations)
    monkeypatch.setattr(runtime_loop_v1, "RUNTIME_RUNS_JSONL", runs)
    monkeypatch.setattr(runtime_loop_v1, "RUNTIME_EVENTS_JSONL", events)
    monkeypatch.setattr(runtime_loop_v1, "RUNTIME_BRIDGE_RUNS_JSONL", bridge_runs)
    monkeypatch.setattr(runtime_loop_v1, "RUNTIME_REPORTS_JSONL", reports)
    monkeypatch.setattr(runtime_loop_v1, "RUNTIME_LOOP_RUNS_JSONL", loop_runs)

    return {
        "state_dir": state_dir,
        "live_source": live_source,
        "observations": observations,
        "runs": runs,
        "events": events,
        "bridge_runs": bridge_runs,
        "reports": reports,
        "loop_runs": loop_runs,
    }


def test_status_reports_empty_isolated_loop_state(isolated_runtime_loop_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_runtime_loop_state
    rc = runtime_loop_v1.status([])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload["runtime_loop_runs_count"] == 0
    assert payload["runtime_observations_count"] == 0
    assert payload["runtime_events_count"] == 0
    assert payload["runtime_reports_count"] == 0


def test_run_once_returns_message_when_no_live_record_exists(isolated_runtime_loop_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    write_jsonl(isolated_runtime_loop_state["live_source"], [])
    rc = runtime_loop_v1.run_once([str(isolated_runtime_loop_state["live_source"])])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload == {"message": "no live record found", "source": str(isolated_runtime_loop_state["live_source"])}


def test_run_once_writes_observation_run_event_report_and_loop_payload(isolated_runtime_loop_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    rc = runtime_loop_v1.run_once([str(isolated_runtime_loop_state["live_source"])])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload["session_name"] == "open_1800"
    assert payload["variant_id"] == "xau_open_sweep_fvg"
    assert payload["direction"] == "bearish"
    assert payload["observation_written"] == str(isolated_runtime_loop_state["observations"])
    assert payload["event_written"] == str(isolated_runtime_loop_state["events"])
    assert payload["report_written"] == str(isolated_runtime_loop_state["reports"])

    observations = runtime_loop_v1.load_jsonl(isolated_runtime_loop_state["observations"])
    runs = runtime_loop_v1.load_jsonl(isolated_runtime_loop_state["runs"])
    events = runtime_loop_v1.load_jsonl(isolated_runtime_loop_state["events"])
    bridge_runs = runtime_loop_v1.load_jsonl(isolated_runtime_loop_state["bridge_runs"])
    reports = runtime_loop_v1.load_jsonl(isolated_runtime_loop_state["reports"])
    loop_runs = runtime_loop_v1.load_jsonl(isolated_runtime_loop_state["loop_runs"])

    assert len(observations) == 1
    assert len(runs) == 1
    assert len(events) == 1
    assert len(bridge_runs) == 1
    assert len(reports) == 1
    assert len(loop_runs) == 1

    assert observations[0]["runtime_mode"] == "observation_only"
    assert observations[0]["runtime_status"] == "observed"
    assert runs[0]["observation_written"] == str(isolated_runtime_loop_state["observations"])
    assert events[0]["event_type"] == "runtime_observed"
    assert events[0]["variant_id"] == "xau_open_sweep_fvg"
    assert bridge_runs[0]["runtime_event_written"] == str(isolated_runtime_loop_state["events"])

    report = reports[0]
    assert report["session_id"] == "open_1800"
    assert report["start_date"] == "2026-04-05"
    assert report["end_date"] == "2026-04-05"
    assert report["runtime_observations_count"] == 1
    assert report["runtime_runs_count"] == 1
    assert report["runtime_events_count"] == 1
    assert report["runtime_bridge_runs_count"] == 1
    assert report["dates"] == ["2026-04-05"]
    assert report["sessions"] == {"open_1800": 1}
    assert report["variants"] == {"xau_open_sweep_fvg": 1}
    assert report["directions"] == {"bearish": 1}
    assert report["event_types"] == {"runtime_observed": 1}
    assert report["avg_entry"] == 3187.0
    assert report["avg_sl"] == 3208.0
    assert report["avg_rr_planned"] == 2.0


def test_show_last_run_returns_message_when_no_loop_run_exists(isolated_runtime_loop_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_runtime_loop_state
    rc = runtime_loop_v1.show_last_run([])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload == {"message": "no runtime loop run yet"}


def test_show_last_run_returns_latest_loop_payload(isolated_runtime_loop_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    runtime_loop_v1.run_once([str(isolated_runtime_loop_state["live_source"])])
    capsys.readouterr()

    rc = runtime_loop_v1.show_last_run([])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload["session_name"] == "open_1800"
    assert payload["variant_id"] == "xau_open_sweep_fvg"
    assert payload["direction"] == "bearish"
