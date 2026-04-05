from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.trading_lab_v1.app import comparator_v1, live_export_v1, live_observation_v1, report_export_v1


FEATURE_1 = {
    "feature_ts": "2026-04-03T18:05:00-04:00",
    "feature_id": "feat-001",
    "local_date": "2026-04-03",
    "session_name": "open_1800",
    "variant_id": "bearish_sweep_fvg",
    "first5_direction": "bearish",
    "entry": 3150.0,
    "sl": 3160.0,
    "rr_planned": 2.0,
    "source_csv": "sample_xauusd_m1.csv",
    "sequence_complete": True,
    "open_candle": {"range_points": 20.0, "body_points": 10.0},
    "first5_range_points": 42.0,
    "first5_body_delta": -18.0,
    "fvg_gap_points": 7.5,
}

FEATURE_2 = {
    "feature_ts": "2026-04-04T00:05:00-04:00",
    "feature_id": "feat-002",
    "local_date": "2026-04-04",
    "session_name": "midnight",
    "variant_id": "bullish_no_sweep_fvg",
    "first5_direction": "bullish",
    "entry": 3180.0,
    "sl": 3170.0,
    "rr_planned": 1.5,
    "source_csv": "sample_xauusd_m1.csv",
    "sequence_complete": False,
    "open_candle": {"range_points": 16.0, "body_points": 8.0},
    "first5_range_points": 35.0,
    "first5_body_delta": 14.0,
    "fvg_gap_points": 5.0,
}

TRADE_1 = {
    "analysis_date": "2026-04-03",
    "session_id": "open_1800",
    "result": "win",
}

TRADE_2 = {
    "analysis_date": "2026-04-04",
    "session_id": "midnight",
    "result": "loss",
}

MARKET_RUN_1 = {"analysis_date": "2026-04-03", "session_id": "open_1800"}
MARKET_RUN_2 = {"analysis_date": "2026-04-04", "session_id": "midnight"}
BATCH_RUN_1 = {"analysis_date": "2026-04-03", "session_id": "open_1800"}

LIVE_RECORD_MATCH = {
    "record_ts": "2026-04-03T18:07:00-04:00",
    "local_date": "2026-04-03",
    "session_name": "open_1800",
    "variant_id": "bearish_sweep_fvg",
    "direction": "bearish",
    "entry": 3151.0,
    "sl": 3161.5,
    "rr_planned": 2.1,
    "source": "sample_live_reference_v1.jsonl",
}

LIVE_RECORD_ONLY = {
    "record_ts": "2026-04-05T18:07:00-04:00",
    "local_date": "2026-04-05",
    "session_name": "open_1800",
    "variant_id": "bearish_no_sweep_fvg",
    "direction": "bearish",
    "entry": 3200.0,
    "sl": 3210.0,
    "rr_planned": 1.8,
    "source": "sample_live_reference_v1.jsonl",
}


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


@pytest.fixture
def isolated_trading_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    state_dir = tmp_path / "state" / "trading_lab_v1"
    exports_dir = state_dir / "exports"
    live_exports_dir = state_dir / "live_exports"
    features_jsonl = state_dir / "features_v1.jsonl"
    trades_jsonl = state_dir / "trades_v1.jsonl"
    market_runs_jsonl = state_dir / "market_runs_v1.jsonl"
    batch_runs_jsonl = state_dir / "batch_runs_v1.jsonl"
    batch_reports_jsonl = state_dir / "batch_reports_v1.jsonl"
    comparator_reports_jsonl = state_dir / "comparator_reports_v1.jsonl"
    comparator_pairs_jsonl = state_dir / "comparator_pairs_v1.jsonl"
    live_observations_jsonl = state_dir / "live_observations_v1.jsonl"
    live_observation_runs_jsonl = state_dir / "live_observation_runs_v1.jsonl"
    sample_live_jsonl = tmp_path / "sample_live_reference_v1.jsonl"

    write_jsonl(features_jsonl, [FEATURE_1, FEATURE_2])
    write_jsonl(trades_jsonl, [TRADE_1, TRADE_2])
    write_jsonl(market_runs_jsonl, [MARKET_RUN_1, MARKET_RUN_2])
    write_jsonl(batch_runs_jsonl, [BATCH_RUN_1])
    write_jsonl(sample_live_jsonl, [LIVE_RECORD_MATCH, LIVE_RECORD_ONLY])

    monkeypatch.setattr(report_export_v1, "STATE_DIR", state_dir)
    monkeypatch.setattr(report_export_v1, "FEATURES_JSONL", features_jsonl)
    monkeypatch.setattr(report_export_v1, "TRADES_JSONL", trades_jsonl)
    monkeypatch.setattr(report_export_v1, "MARKET_RUNS_JSONL", market_runs_jsonl)
    monkeypatch.setattr(report_export_v1, "BATCH_RUNS_JSONL", batch_runs_jsonl)
    monkeypatch.setattr(report_export_v1, "BATCH_REPORTS_JSONL", batch_reports_jsonl)
    monkeypatch.setattr(report_export_v1, "EXPORTS_DIR", exports_dir)

    monkeypatch.setattr(comparator_v1, "STATE_DIR", state_dir)
    monkeypatch.setattr(comparator_v1, "FEATURES_JSONL", features_jsonl)
    monkeypatch.setattr(comparator_v1, "TRADES_JSONL", trades_jsonl)
    monkeypatch.setattr(comparator_v1, "COMPARATOR_REPORTS_JSONL", comparator_reports_jsonl)
    monkeypatch.setattr(comparator_v1, "COMPARATOR_PAIRS_JSONL", comparator_pairs_jsonl)
    monkeypatch.setattr(comparator_v1, "SAMPLE_LIVE_JSONL", sample_live_jsonl)

    monkeypatch.setattr(live_observation_v1, "STATE_DIR", state_dir)
    monkeypatch.setattr(live_observation_v1, "LIVE_OBSERVATIONS_JSONL", live_observations_jsonl)
    monkeypatch.setattr(live_observation_v1, "LIVE_OBSERVATION_RUNS_JSONL", live_observation_runs_jsonl)
    monkeypatch.setattr(live_observation_v1, "SAMPLE_LIVE_JSONL", sample_live_jsonl)

    monkeypatch.setattr(live_export_v1, "STATE_DIR", state_dir)
    monkeypatch.setattr(live_export_v1, "LIVE_OBSERVATIONS_JSONL", live_observations_jsonl)
    monkeypatch.setattr(live_export_v1, "LIVE_OBSERVATION_RUNS_JSONL", live_observation_runs_jsonl)
    monkeypatch.setattr(live_export_v1, "LIVE_EXPORTS_DIR", live_exports_dir)
    monkeypatch.setattr(live_export_v1, "SAMPLE_LIVE_JSONL", sample_live_jsonl)

    return {
        "state_dir": state_dir,
        "exports_dir": exports_dir,
        "live_exports_dir": live_exports_dir,
        "features_jsonl": features_jsonl,
        "trades_jsonl": trades_jsonl,
        "market_runs_jsonl": market_runs_jsonl,
        "batch_runs_jsonl": batch_runs_jsonl,
        "batch_reports_jsonl": batch_reports_jsonl,
        "comparator_reports_jsonl": comparator_reports_jsonl,
        "comparator_pairs_jsonl": comparator_pairs_jsonl,
        "live_observations_jsonl": live_observations_jsonl,
        "live_observation_runs_jsonl": live_observation_runs_jsonl,
        "sample_live_jsonl": sample_live_jsonl,
    }


def test_build_report_aggregates_core_counts_and_averages(isolated_trading_state: dict[str, Path]) -> None:
    del isolated_trading_state
    report = report_export_v1.build_report(None, None, None)

    assert report["features_count"] == 2
    assert report["trades_count"] == 2
    assert report["market_runs_count"] == 2
    assert report["batch_runs_count"] == 1
    assert report["sequence_complete_count"] == 1
    assert report["dates"] == ["2026-04-03", "2026-04-04"]
    assert report["variants"] == {
        "bearish_sweep_fvg": 1,
        "bullish_no_sweep_fvg": 1,
    }
    assert report["directions"] == {"bearish": 1, "bullish": 1}
    assert report["avg_open_range_points"] == 18.0
    assert report["avg_open_body_points"] == 9.0
    assert report["avg_first5_range_points"] == 38.5
    assert report["avg_first5_body_delta"] == -2.0
    assert report["avg_fvg_gap_points"] == 6.25
    assert report["avg_rr_planned"] == 1.75
    assert report["trade_results"] == {"win": 1, "loss": 1}


def test_export_new_writes_batch_report_and_exports(isolated_trading_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    rc = report_export_v1.export_new(["open_1800", "2026-04-03", "2026-04-03"])
    out = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert Path(out["json_export"]).exists()
    assert Path(out["markdown_export"]).exists()

    stored_reports = report_export_v1.load_jsonl(isolated_trading_state["batch_reports_jsonl"])
    assert len(stored_reports) == 1
    assert stored_reports[0]["session_id"] == "open_1800"
    assert stored_reports[0]["features_count"] == 1

    markdown_text = Path(out["markdown_export"]).read_text(encoding="utf-8")
    assert "# Trading LAB V1 — Batch Report Export" in markdown_text
    assert "Session: open_1800" in markdown_text


def test_export_last_returns_message_when_no_batch_report_exists(isolated_trading_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_trading_state
    rc = report_export_v1.export_last([])
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert payload == {"message": "no batch report to export"}


def test_compare_builds_matched_lab_only_and_live_only_records(isolated_trading_state: dict[str, Path]) -> None:
    report = comparator_v1.compare(None, None, None, isolated_trading_state["sample_live_jsonl"])

    assert report["lab_feature_count"] == 2
    assert report["live_record_count"] == 2
    assert report["matched_count"] == 1
    assert report["lab_only_count"] == 1
    assert report["live_only_count"] == 1
    assert report["variant_match_count"] == 1
    assert report["direction_match_count"] == 1
    assert report["avg_entry_delta_points"] == 1.0
    assert report["avg_sl_delta_points"] == 1.5
    assert report["avg_rr_delta"] == 0.1
    assert report["matched_dates"] == ["2026-04-03"]

    pair_rows = comparator_v1.load_jsonl(isolated_trading_state["comparator_pairs_jsonl"])
    assert len(pair_rows) == 3
    assert {row["pair_status"] for row in pair_rows} == {"matched", "lab_only", "live_only"}

    report_rows = comparator_v1.load_jsonl(isolated_trading_state["comparator_reports_jsonl"])
    assert len(report_rows) == 1


def test_show_last_report_returns_message_when_no_comparator_report_exists(isolated_trading_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_trading_state
    rc = comparator_v1.show_last_report([])
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert payload == {"message": "no comparator report yet"}


def test_observe_live_writes_observations_and_summary(isolated_trading_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    rc = live_observation_v1.observe_live([str(isolated_trading_state["sample_live_jsonl"]), "open_1800", "2026-04-03", "2026-04-03"])
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert payload["input_count"] == 2
    assert payload["observed_count"] == 1
    assert payload["dates"] == ["2026-04-03"]
    assert payload["sessions"] == ["open_1800"]

    observed_rows = live_observation_v1.load_jsonl(isolated_trading_state["live_observations_jsonl"])
    assert len(observed_rows) == 1
    assert observed_rows[0]["observation_mode"] == "live_observation"
    assert observed_rows[0]["observation_status"] == "observed"

    run_rows = live_observation_v1.load_jsonl(isolated_trading_state["live_observation_runs_jsonl"])
    assert len(run_rows) == 1


def test_show_last_run_returns_message_when_no_live_observation_run_exists(isolated_trading_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_trading_state
    rc = live_observation_v1.show_last_run([])
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert payload == {"message": "no live observation run yet"}


def test_live_export_new_writes_json_and_markdown_exports(isolated_trading_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    rc = live_export_v1.export_new([str(isolated_trading_state["sample_live_jsonl"]), "open_1800", "2026-04-03", "2026-04-03"])
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    json_export = Path(payload["json_export"])
    md_export = Path(payload["markdown_export"])
    assert json_export.exists()
    assert md_export.exists()

    exported_payload = json.loads(json_export.read_text(encoding="utf-8"))
    assert exported_payload["observation_count"] == 1
    assert exported_payload["observations"][0]["session_name"] == "open_1800"

    markdown_text = md_export.read_text(encoding="utf-8")
    assert "# Trading LIVE Observation Export" in markdown_text
    assert "Observation count: 1" in markdown_text


def test_live_export_last_uses_last_run_scope(isolated_trading_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    live_observation_v1.observe_live([str(isolated_trading_state["sample_live_jsonl"]), "open_1800", "2026-04-03", "2026-04-03"])
    capsys.readouterr()

    rc = live_export_v1.export_last([])
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    json_export = Path(payload["json_export"])
    exported_payload = json.loads(json_export.read_text(encoding="utf-8"))
    assert exported_payload["session_id"] == "open_1800"
    assert exported_payload["observation_count"] == 1


def test_live_export_last_returns_message_when_no_run_exists(isolated_trading_state: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    del isolated_trading_state
    rc = live_export_v1.export_last([])
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert payload == {"message": "no live observation run to export"}
