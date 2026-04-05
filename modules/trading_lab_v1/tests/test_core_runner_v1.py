from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.trading_lab_v1.app import trading_lab_v1


PROFILE_YAML = """version: \"1\"
profile_id: \"xauusd_dual_stack_v1\"
frame:
  timezone: \"America/Montreal\"
  symbol: \"XAUUSD\"
  sessions:
    - session_id: \"open_1800\"
      enabled: true
      start_local: \"18:00\"
      end_local: \"18:59\"
      signal_window_start: \"18:00\"
      signal_window_end: \"18:05\"
    - session_id: \"midnight\"
      enabled: false
      start_local: \"00:00\"
      end_local: \"00:59\"
      signal_window_start: \"00:00\"
      signal_window_end: \"00:05\"
strategy:
  strategy_id: \"xau_session_open_v1\"
  variants:
    - variant_id: \"xau_open_sweep_fvg\"
      enabled: true
    - variant_id: \"xau_open_no_sweep_fvg\"
      enabled: true
"""


MARKET_ROWS_COMPLETE = [
    ["2026-04-03T18:00:00-04:00", 3200.0, 3205.0, 3198.0, 3204.0, 100.0],
    ["2026-04-03T18:01:00-04:00", 3204.0, 3208.0, 3202.0, 3203.0, 90.0],
    ["2026-04-03T18:02:00-04:00", 3192.0, 3196.0, 3190.0, 3191.0, 95.0],
    ["2026-04-03T18:03:00-04:00", 3191.0, 3194.0, 3188.0, 3189.0, 80.0],
    ["2026-04-03T18:04:00-04:00", 3189.0, 3192.0, 3186.0, 3187.0, 85.0],
]

MARKET_ROWS_INCOMPLETE = MARKET_ROWS_COMPLETE[:3]


def write_market_csv(path: Path, rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


@pytest.fixture
def isolated_runner_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    docs_dir = tmp_path / "docs" / "ot" / "trading" / "schemas"
    docs_dir.mkdir(parents=True)
    profile_path = docs_dir / "xauusd_dual_stack_v1.profile.yaml"
    event_schema_path = docs_dir / "trading_event_v1.schema.json"
    trade_schema_path = docs_dir / "trading_trade_v1.schema.json"
    state_dir = tmp_path / "state" / "trading_lab_v1"
    csv_complete = tmp_path / "complete.csv"
    csv_incomplete = tmp_path / "incomplete.csv"

    profile_path.write_text(PROFILE_YAML, encoding="utf-8")
    event_schema_path.write_text("{}\n", encoding="utf-8")
    trade_schema_path.write_text("{}\n", encoding="utf-8")
    write_market_csv(csv_complete, MARKET_ROWS_COMPLETE)
    write_market_csv(csv_incomplete, MARKET_ROWS_INCOMPLETE)

    monkeypatch.setattr(trading_lab_v1, "PROFILE_PATH", profile_path)
    monkeypatch.setattr(trading_lab_v1, "EVENT_SCHEMA_PATH", event_schema_path)
    monkeypatch.setattr(trading_lab_v1, "TRADE_SCHEMA_PATH", trade_schema_path)
    monkeypatch.setattr(trading_lab_v1, "STATE_DIR", state_dir)
    monkeypatch.setattr(trading_lab_v1, "EVENTS_JSONL", state_dir / "events_v1.jsonl")
    monkeypatch.setattr(trading_lab_v1, "TRADES_JSONL", state_dir / "trades_v1.jsonl")
    monkeypatch.setattr(trading_lab_v1, "MARKET_RUNS_JSONL", state_dir / "market_runs_v1.jsonl")
    monkeypatch.setattr(trading_lab_v1, "FEATURES_JSONL", state_dir / "features_v1.jsonl")
    monkeypatch.setattr(trading_lab_v1, "BATCH_RUNS_JSONL", state_dir / "batch_runs_v1.jsonl")
    monkeypatch.setattr(trading_lab_v1, "BATCH_REPORTS_JSONL", state_dir / "batch_reports_v1.jsonl")
    monkeypatch.setattr(trading_lab_v1, "SAMPLE_MARKET_CSV", csv_complete)

    return {
        "state_dir": state_dir,
        "profile_path": profile_path,
        "csv_complete": csv_complete,
        "csv_incomplete": csv_incomplete,
    }


def test_load_profile_parses_sessions_and_variants(isolated_runner_state: dict[str, Path]) -> None:
    del isolated_runner_state
    profile = trading_lab_v1.load_profile()

    assert profile["version"] == "1"
    assert profile["profile_id"] == "xauusd_dual_stack_v1"
    assert profile["frame"]["timezone"] == "America/Montreal"
    assert profile["frame"]["symbol"] == "XAUUSD"
    assert len(profile["frame"]["sessions"]) == 2
    assert profile["frame"]["sessions"][0]["session_id"] == "open_1800"
    assert profile["frame"]["sessions"][0]["enabled"] is True
    assert profile["strategy"]["strategy_id"] == "xau_session_open_v1"
    assert profile["strategy"]["variants"][0]["variant_id"] == "xau_open_sweep_fvg"


def test_choose_session_returns_first_enabled_and_named_session(isolated_runner_state: dict[str, Path]) -> None:
    del isolated_runner_state
    profile = trading_lab_v1.load_profile()

    first_enabled = trading_lab_v1.choose_session(profile, None)
    explicit = trading_lab_v1.choose_session(profile, "open_1800")

    assert first_enabled["session_id"] == "open_1800"
    assert explicit["session_id"] == "open_1800"

    with pytest.raises(SystemExit, match="Unknown session_id: missing"):
        trading_lab_v1.choose_session(profile, "missing")


def test_load_market_csv_parses_and_sorts_rows(isolated_runner_state: dict[str, Path]) -> None:
    rows = trading_lab_v1.load_market_csv(isolated_runner_state["csv_complete"], "America/Montreal")

    assert len(rows) == 5
    assert rows[0]["ts"] == datetime(2026, 4, 3, 18, 0, tzinfo=ZoneInfo("America/Montreal"))
    assert rows[-1]["close"] == 3187.0


def test_detect_fvg_and_sweep_detect_bearish_sweep_fvg(isolated_runner_state: dict[str, Path]) -> None:
    rows = trading_lab_v1.load_market_csv(isolated_runner_state["csv_complete"], "America/Montreal")
    first_five = rows[:5]

    sweep = trading_lab_v1.detect_sweep(first_five)
    fvg = trading_lab_v1.detect_fvg(first_five)
    direction = trading_lab_v1.choose_direction(first_five, fvg["fvg_direction"])
    variant = trading_lab_v1.choose_variant_from_features(sweep["sweep_detected"], fvg["fvg_detected"])

    assert sweep == {"sweep_above": True, "sweep_below": True, "sweep_detected": True}
    assert fvg["fvg_detected"] is True
    assert fvg["fvg_direction"] == "bearish"
    assert fvg["fvg_gap_points"] == 2.0
    assert direction == "bearish"
    assert variant == "xau_open_sweep_fvg"


def test_build_feature_payload_complete_sequence_sets_market_fields(isolated_runner_state: dict[str, Path]) -> None:
    profile = trading_lab_v1.load_profile()
    session = trading_lab_v1.choose_session(profile, "open_1800")
    rows = trading_lab_v1.load_market_csv(isolated_runner_state["csv_complete"], "America/Montreal")

    payload = trading_lab_v1.build_feature_payload(profile, session, rows, "2026-04-03", isolated_runner_state["csv_complete"])

    assert payload["sequence_complete"] is True
    assert payload["session_name"] == "open_1800"
    assert payload["local_date"] == "2026-04-03"
    assert payload["first5_direction"] == "bearish"
    assert payload["variant_id"] == "xau_open_sweep_fvg"
    assert payload["entry"] == 3187.0
    assert payload["sl"] == 3208.0
    assert payload["rr_planned"] == 2.0
    assert payload["first5_range_points"] == 22.0
    assert payload["first5_body_delta"] == -13.0
    assert payload["open_candle"]["range_points"] == 7.0
    assert payload["open_candle"]["body_points"] == 4.0


def test_build_feature_payload_incomplete_sequence_blocks_variant_and_trade_fields(isolated_runner_state: dict[str, Path]) -> None:
    profile = trading_lab_v1.load_profile()
    session = trading_lab_v1.choose_session(profile, "open_1800")
    rows = trading_lab_v1.load_market_csv(isolated_runner_state["csv_incomplete"], "America/Montreal")

    payload = trading_lab_v1.build_feature_payload(profile, session, rows, "2026-04-03", isolated_runner_state["csv_incomplete"])

    assert payload["sequence_complete"] is False
    assert payload["candle_count"] == 3
    assert payload["variant_id"] is None
    assert payload["entry"] is None
    assert payload["sl"] is None
    assert payload["rr_planned"] == 2.0
    assert payload["fvg_detected"] is False
    assert payload["sweep_detected"] is False


def test_process_market_run_complete_writes_feature_event_trade_and_run(isolated_runner_state: dict[str, Path]) -> None:
    profile = trading_lab_v1.load_profile()
    session = trading_lab_v1.choose_session(profile, "open_1800")

    result = trading_lab_v1.process_market_run(profile, session, isolated_runner_state["csv_complete"], "2026-04-03")

    assert result["features"]["sequence_complete"] is True
    assert result["event"]["event_type"] == "setup_classified"
    assert result["trade"]["variant_id"] == "xau_open_sweep_fvg"
    assert result["trade"]["entry"] == 3187.0
    assert result["run_payload"]["selected_rows"] == 5
    assert result["run_payload"]["trade_written"] == str(trading_lab_v1.TRADES_JSONL)

    assert len(trading_lab_v1.load_jsonl(trading_lab_v1.FEATURES_JSONL)) == 1
    assert len(trading_lab_v1.load_jsonl(trading_lab_v1.EVENTS_JSONL)) == 1
    assert len(trading_lab_v1.load_jsonl(trading_lab_v1.TRADES_JSONL)) == 1
    assert len(trading_lab_v1.load_jsonl(trading_lab_v1.MARKET_RUNS_JSONL)) == 1


def test_process_market_run_incomplete_skips_trade_write(isolated_runner_state: dict[str, Path]) -> None:
    profile = trading_lab_v1.load_profile()
    session = trading_lab_v1.choose_session(profile, "open_1800")

    result = trading_lab_v1.process_market_run(profile, session, isolated_runner_state["csv_incomplete"], "2026-04-03")

    assert result["features"]["sequence_complete"] is False
    assert result["event"]["event_type"] == "setup_blocked"
    assert result["trade"] is None
    assert result["run_payload"]["trade_written"] is None
    assert len(trading_lab_v1.load_jsonl(trading_lab_v1.TRADES_JSONL)) == 0


def test_batch_report_appends_report_and_show_last_returns_it(isolated_runner_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    profile = trading_lab_v1.load_profile()
    session = trading_lab_v1.choose_session(profile, "open_1800")
    trading_lab_v1.process_market_run(profile, session, isolated_runner_state["csv_complete"], "2026-04-03")
    write_jsonl(trading_lab_v1.BATCH_RUNS_JSONL, [{"analysis_date": "2026-04-03", "session_id": "open_1800"}])

    rc = trading_lab_v1.batch_report(["open_1800", "2026-04-03", "2026-04-03"])
    report = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert report["features_count"] == 1
    assert report["trades_count"] == 1
    assert report["market_runs_count"] == 1
    assert report["batch_runs_count"] == 1
    assert report["sequence_complete_count"] == 1
    assert report["variants"] == {"xau_open_sweep_fvg": 1}
    assert report["directions"] == {"bearish": 1}
    assert report["trade_results"] == {"open": 1}

    assert len(trading_lab_v1.load_jsonl(trading_lab_v1.BATCH_REPORTS_JSONL)) == 1

    rc_last = trading_lab_v1.show_last_batch_report([])
    last_report = json.loads(capsys.readouterr().out)
    assert rc_last == 0
    assert last_report["features_count"] == 1


def test_show_last_batch_report_returns_message_when_no_report_exists(isolated_runner_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_runner_state
    rc = trading_lab_v1.show_last_batch_report([])
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert payload == {"message": "no batch report yet"}
