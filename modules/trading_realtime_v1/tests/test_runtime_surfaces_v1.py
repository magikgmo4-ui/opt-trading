from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.trading_realtime_v1.app import event_bridge_v1, export_v1, reporting_v1, trading_realtime_v1


LIVE_RECORD_1 = {
    "record_ts": "2026-04-04T18:05:00-04:00",
    "local_date": "2026-04-04",
    "session_name": "open_1800",
    "variant_id": "xau_open_sweep_fvg",
    "direction": "bearish",
    "entry": 3187.0,
    "sl": 3208.0,
    "rr_planned": 2.0,
}

LIVE_RECORD_2 = {
    "record_ts": "2026-04-05T00:05:00-04:00",
    "local_date": "2026-04-05",
    "session_name": "midnight",
    "variant_id": "xau_open_no_sweep_fvg",
    "direction": "bullish",
    "entry": 3199.0,
    "sl": 3188.0,
    "rr_planned": 1.5,
}


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


@pytest.fixture
def isolated_runtime_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    state_dir = tmp_path / "state" / "trading_realtime_v1"
    live_source = tmp_path / "sample_live_reference_v1.jsonl"
    observations = state_dir / "runtime_observations_v1.jsonl"
    runs = state_dir / "runtime_runs_v1.jsonl"
    events = state_dir / "runtime_events_v1.jsonl"
    bridge_runs = state_dir / "runtime_bridge_runs_v1.jsonl"
    reports = state_dir / "runtime_reports_v1.jsonl"
    exports_dir = state_dir / "runtime_exports"
    event_schema = tmp_path / "trading_event_v1.schema.json"
    trade_schema = tmp_path / "trading_trade_v1.schema.json"
    profile_path = tmp_path / "xauusd_dual_stack_v1.profile.yaml"

    write_jsonl(live_source, [LIVE_RECORD_1, LIVE_RECORD_2])
    event_schema.write_text("{}\n", encoding="utf-8")
    trade_schema.write_text("{}\n", encoding="utf-8")
    profile_path.write_text("profile_id: xauusd_dual_stack_v1\n", encoding="utf-8")

    monkeypatch.setattr(trading_realtime_v1, "LIVE_SOURCE_PATH", live_source)
    monkeypatch.setattr(trading_realtime_v1, "STATE_DIR", state_dir)
    monkeypatch.setattr(trading_realtime_v1, "RUNTIME_OBSERVATIONS_JSONL", observations)
    monkeypatch.setattr(trading_realtime_v1, "RUNTIME_RUNS_JSONL", runs)
    monkeypatch.setattr(trading_realtime_v1, "PROFILE_PATH", profile_path)
    monkeypatch.setattr(trading_realtime_v1, "EVENT_SCHEMA_PATH", event_schema)
    monkeypatch.setattr(trading_realtime_v1, "TRADE_SCHEMA_PATH", trade_schema)

    monkeypatch.setattr(event_bridge_v1, "STATE_DIR", state_dir)
    monkeypatch.setattr(event_bridge_v1, "RUNTIME_OBSERVATIONS_JSONL", observations)
    monkeypatch.setattr(event_bridge_v1, "RUNTIME_EVENTS_JSONL", events)
    monkeypatch.setattr(event_bridge_v1, "RUNTIME_BRIDGE_RUNS_JSONL", bridge_runs)
    monkeypatch.setattr(event_bridge_v1, "EVENT_SCHEMA_PATH", event_schema)

    monkeypatch.setattr(reporting_v1, "STATE_DIR", state_dir)
    monkeypatch.setattr(reporting_v1, "RUNTIME_OBSERVATIONS_JSONL", observations)
    monkeypatch.setattr(reporting_v1, "RUNTIME_RUNS_JSONL", runs)
    monkeypatch.setattr(reporting_v1, "RUNTIME_EVENTS_JSONL", events)
    monkeypatch.setattr(reporting_v1, "RUNTIME_BRIDGE_RUNS_JSONL", bridge_runs)
    monkeypatch.setattr(reporting_v1, "RUNTIME_REPORTS_JSONL", reports)

    monkeypatch.setattr(export_v1, "STATE_DIR", state_dir)
    monkeypatch.setattr(export_v1, "RUNTIME_OBSERVATIONS_JSONL", observations)
    monkeypatch.setattr(export_v1, "RUNTIME_RUNS_JSONL", runs)
    monkeypatch.setattr(export_v1, "RUNTIME_EVENTS_JSONL", events)
    monkeypatch.setattr(export_v1, "RUNTIME_BRIDGE_RUNS_JSONL", bridge_runs)
    monkeypatch.setattr(export_v1, "RUNTIME_REPORTS_JSONL", reports)
    monkeypatch.setattr(export_v1, "RUNTIME_EXPORTS_DIR", exports_dir)

    return {
        "state_dir": state_dir,
        "live_source": live_source,
        "observations": observations,
        "runs": runs,
        "events": events,
        "bridge_runs": bridge_runs,
        "reports": reports,
        "exports_dir": exports_dir,
    }


def test_status_and_runtime_status_report_empty_isolated_state(isolated_runtime_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_runtime_state
    rc = trading_realtime_v1.status([])
    status_payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert status_payload["module"] == "trading_realtime_v1"
    assert status_payload["live_source_exists"] is True
    assert status_payload["event_schema_exists"] is True
    assert status_payload["trade_schema_exists"] is True

    rc_runtime = trading_realtime_v1.runtime_status([])
    runtime_payload = json.loads(capsys.readouterr().out)
    assert rc_runtime == 0
    assert runtime_payload["runtime_observations_count"] == 0
    assert runtime_payload["runtime_runs_count"] == 0


def test_observe_once_returns_message_when_live_source_is_empty(isolated_runtime_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    write_jsonl(isolated_runtime_state["live_source"], [])
    rc = trading_realtime_v1.observe_once([str(isolated_runtime_state["live_source"])])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload == {"message": "no live record found", "source": str(isolated_runtime_state["live_source"])}


def test_observe_once_writes_latest_observation_and_run(isolated_runtime_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    rc = trading_realtime_v1.observe_once([str(isolated_runtime_state["live_source"])])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload["session_name"] == "midnight"
    assert payload["variant_id"] == "xau_open_no_sweep_fvg"
    assert payload["direction"] == "bullish"

    observations = trading_realtime_v1.load_jsonl(isolated_runtime_state["observations"])
    runs = trading_realtime_v1.load_jsonl(isolated_runtime_state["runs"])
    assert len(observations) == 1
    assert len(runs) == 1
    assert observations[0]["runtime_mode"] == "observation_only"
    assert observations[0]["runtime_status"] == "observed"
    assert runs[0]["observation_written"] == str(isolated_runtime_state["observations"])


def test_bridge_latest_returns_message_when_no_observation_exists(isolated_runtime_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_runtime_state
    rc = event_bridge_v1.bridge_latest([])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload == {"message": "no runtime observation found"}


def test_bridge_latest_writes_runtime_event_and_run(isolated_runtime_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    trading_realtime_v1.observe_once([str(isolated_runtime_state["live_source"])])
    capsys.readouterr()

    rc = event_bridge_v1.bridge_latest([])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload["session_name"] == "midnight"
    assert payload["runtime_event_written"] == str(isolated_runtime_state["events"])

    events = event_bridge_v1.load_jsonl(isolated_runtime_state["events"])
    bridge_runs = event_bridge_v1.load_jsonl(isolated_runtime_state["bridge_runs"])
    assert len(events) == 1
    assert len(bridge_runs) == 1
    assert events[0]["event_type"] == "runtime_observed"
    assert events[0]["variant_id"] == "xau_open_no_sweep_fvg"
    assert events[0]["direction"] == "bullish"

    rc_last = event_bridge_v1.show_last_event([])
    last_event = json.loads(capsys.readouterr().out)
    assert rc_last == 0
    assert last_event["event_id"] == events[0]["event_id"]


def test_show_last_report_returns_message_when_no_runtime_report_exists(isolated_runtime_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_runtime_state
    rc = reporting_v1.show_last_report([])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload == {"message": "no runtime report yet"}


def test_report_runtime_aggregates_observations_events_and_bridge_runs(isolated_runtime_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    write_jsonl(isolated_runtime_state["observations"], [
        {
            "local_date": "2026-04-04",
            "session_name": "open_1800",
            "variant_id": "xau_open_sweep_fvg",
            "direction": "bearish",
            "entry": 3187.0,
            "sl": 3208.0,
            "rr_planned": 2.0,
        },
        {
            "local_date": "2026-04-05",
            "session_name": "midnight",
            "variant_id": "xau_open_no_sweep_fvg",
            "direction": "bullish",
            "entry": 3199.0,
            "sl": 3188.0,
            "rr_planned": 1.5,
        },
    ])
    write_jsonl(isolated_runtime_state["runs"], [
        {"local_date": "2026-04-04", "session_name": "open_1800"},
        {"local_date": "2026-04-05", "session_name": "midnight"},
    ])
    write_jsonl(isolated_runtime_state["events"], [
        {"local_date": "2026-04-04", "session_name": "open_1800", "variant_id": "xau_open_sweep_fvg", "direction": "bearish", "event_type": "runtime_observed"},
        {"local_date": "2026-04-05", "session_name": "midnight", "variant_id": "xau_open_no_sweep_fvg", "direction": "bullish", "event_type": "runtime_observed"},
    ])
    write_jsonl(isolated_runtime_state["bridge_runs"], [
        {"local_date": "2026-04-04", "session_name": "open_1800"},
        {"local_date": "2026-04-05", "session_name": "midnight"},
    ])

    rc = reporting_v1.report_runtime([])
    report = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert report["runtime_observations_count"] == 2
    assert report["runtime_runs_count"] == 2
    assert report["runtime_events_count"] == 2
    assert report["runtime_bridge_runs_count"] == 2
    assert report["dates"] == ["2026-04-04", "2026-04-05"]
    assert report["sessions"] == {"open_1800": 1, "midnight": 1}
    assert report["variants"] == {"xau_open_sweep_fvg": 1, "xau_open_no_sweep_fvg": 1}
    assert report["directions"] == {"bearish": 1, "bullish": 1}
    assert report["event_types"] == {"runtime_observed": 2}
    assert report["avg_entry"] == 3193.0
    assert report["avg_sl"] == 3198.0
    assert report["avg_rr_planned"] == 1.75

    stored_reports = reporting_v1.load_jsonl(isolated_runtime_state["reports"])
    assert len(stored_reports) == 1


def test_export_last_returns_message_when_no_runtime_report_exists(isolated_runtime_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_runtime_state
    rc = export_v1.export_last([])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload == {"message": "no runtime report to export"}


def test_export_new_writes_json_and_markdown_exports(isolated_runtime_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    write_jsonl(isolated_runtime_state["observations"], [
        {
            "local_date": "2026-04-04",
            "session_name": "open_1800",
            "entry": 3187.0,
            "sl": 3208.0,
            "rr_planned": 2.0,
        }
    ])
    write_jsonl(isolated_runtime_state["runs"], [{"local_date": "2026-04-04", "session_name": "open_1800"}])
    write_jsonl(isolated_runtime_state["events"], [{"local_date": "2026-04-04", "session_name": "open_1800", "variant_id": "xau_open_sweep_fvg", "direction": "bearish", "event_type": "runtime_observed"}])
    write_jsonl(isolated_runtime_state["bridge_runs"], [{"local_date": "2026-04-04", "session_name": "open_1800"}])

    rc = export_v1.export_new(["open_1800", "2026-04-04", "2026-04-04"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0

    json_export = Path(payload["json_export"])
    md_export = Path(payload["markdown_export"])
    assert json_export.exists()
    assert md_export.exists()

    exported_report = json.loads(json_export.read_text(encoding="utf-8"))
    assert exported_report["runtime_observations_count"] == 1
    assert exported_report["sessions"] == {"open_1800": 1}

    markdown_text = md_export.read_text(encoding="utf-8")
    assert "# Trading REALTIME V1 — Runtime Report Export" in markdown_text
    assert "- Session: open_1800" in markdown_text


def test_export_last_uses_latest_runtime_report(isolated_runtime_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    write_jsonl(isolated_runtime_state["reports"], [
        {
            "report_ts": "2026-04-05T01:00:00-04:00",
            "session_id": "midnight",
            "start_date": "2026-04-05",
            "end_date": "2026-04-05",
            "runtime_observations_count": 1,
            "runtime_runs_count": 1,
            "runtime_events_count": 1,
            "runtime_bridge_runs_count": 1,
            "dates": ["2026-04-05"],
            "sessions": {"midnight": 1},
            "variants": {"xau_open_no_sweep_fvg": 1},
            "directions": {"bullish": 1},
            "event_types": {"runtime_observed": 1},
            "avg_entry": 3199.0,
            "avg_sl": 3188.0,
            "avg_rr_planned": 1.5,
        }
    ])

    rc = export_v1.export_last([])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0

    json_export = Path(payload["json_export"])
    exported_report = json.loads(json_export.read_text(encoding="utf-8"))
    assert exported_report["session_id"] == "midnight"
    assert exported_report["runtime_observations_count"] == 1
