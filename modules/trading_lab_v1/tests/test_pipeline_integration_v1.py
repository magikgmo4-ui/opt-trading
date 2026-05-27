"""
Integration tests for run_with_outcomes pipeline in trading_lab_v1.

Verifies that a single run_with_outcomes call on sample_xauusd_m1_real_like.csv
produces fully resolved trades (no virtual_open remaining) with correct aggregate metrics.

Run: pytest modules/trading_lab_v1/tests/test_pipeline_integration_v1.py -q
"""
from __future__ import annotations

import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.trading_lab_v1.app.trading_lab_v1 import (
    run_with_outcomes,
    batch_run,
    load_jsonl,
    TRADES_JSONL,
    FEATURES_JSONL,
    SAMPLE_MARKET_CSV,
)

import pytest


@pytest.fixture(autouse=True)
def _clean_state(tmp_path, monkeypatch):
    """Redirect state JSONL paths to tmp_path for each test."""
    import modules.trading_lab_v1.app.trading_lab_v1 as lab
    monkeypatch.setattr(lab, "TRADES_JSONL", tmp_path / "trades.jsonl")
    monkeypatch.setattr(lab, "FEATURES_JSONL", tmp_path / "features.jsonl")
    monkeypatch.setattr(lab, "EVENTS_JSONL", tmp_path / "events.jsonl")
    monkeypatch.setattr(lab, "MARKET_RUNS_JSONL", tmp_path / "market_runs.jsonl")
    monkeypatch.setattr(lab, "BATCH_REPORTS_JSONL", tmp_path / "batch_reports.jsonl")


class TestRunWithOutcomes:
    def test_runs_done_count(self, tmp_path, capsys):
        run_with_outcomes([])
        out = capsys.readouterr().out
        # First JSON block: batch_run summary
        blocks = [json.loads(b) for b in _split_json_blocks(out)]
        batch = blocks[0]
        assert batch["runs_done"] == 10

    def test_all_trades_resolved(self, tmp_path):
        run_with_outcomes([])
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        trades = load_jsonl(lab.TRADES_JSONL)
        assert len(trades) == 10
        assert all(t.get("execution_state") == "virtual_closed" for t in trades)

    def test_no_virtual_open_remaining(self, tmp_path):
        run_with_outcomes([])
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        trades = load_jsonl(lab.TRADES_JSONL)
        assert not any(t.get("execution_state") == "virtual_open" for t in trades)

    def test_win_loss_timeout_counts(self, tmp_path, capsys):
        run_with_outcomes([])
        out = capsys.readouterr().out
        blocks = [json.loads(b) for b in _split_json_blocks(out)]
        outcome_block = blocks[1]  # apply_outcomes output
        assert outcome_block["wins"] == 6
        assert outcome_block["losses"] == 4
        assert outcome_block["timeouts"] == 0

    def test_avg_r_realized(self, tmp_path, capsys):
        run_with_outcomes([])
        out = capsys.readouterr().out
        blocks = [json.loads(b) for b in _split_json_blocks(out)]
        outcome_block = blocks[1]
        assert outcome_block["avg_r_realized"] == 0.8

    def test_batch_report_outcome_metrics(self, tmp_path, capsys):
        run_with_outcomes([])
        out = capsys.readouterr().out
        blocks = [json.loads(b) for b in _split_json_blocks(out)]
        report = blocks[2]
        assert report["win_count"] == 6
        assert report["loss_count"] == 4
        assert report["timeout_count"] == 0
        assert report["avg_r_realized"] == 0.8

    def test_batch_report_variants_all_covered(self, tmp_path, capsys):
        run_with_outcomes([])
        out = capsys.readouterr().out
        blocks = [json.loads(b) for b in _split_json_blocks(out)]
        report = blocks[2]
        variants = report["variants"]
        assert len(variants) == 4

    def test_trades_have_exit_fields(self, tmp_path):
        run_with_outcomes([])
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        trades = load_jsonl(lab.TRADES_JSONL)
        for t in trades:
            assert t.get("exit_price") is not None
            assert t.get("exit_ts") is not None
            assert t.get("bars_held") is not None
            assert t.get("outcome_reason") is not None
            assert t.get("tp") is not None

    def test_idempotent_clear(self, tmp_path):
        run_with_outcomes([])
        run_with_outcomes([])
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        trades = load_jsonl(lab.TRADES_JSONL)
        assert len(trades) == 10  # second run cleared and re-ran, not doubled


class TestBatchRun:
    def test_batch_run_returns_correct_count(self, tmp_path, capsys):
        batch_run([])
        out = capsys.readouterr().out
        result = json.loads(out)
        assert result["runs_done"] == 10

    def test_batch_run_session_filter(self, tmp_path, capsys):
        batch_run([str(SAMPLE_MARKET_CSV), "gold_open_18h"])
        out = capsys.readouterr().out
        result = json.loads(out)
        assert result["runs_done"] == 5

    def test_batch_run_writes_trades(self, tmp_path):
        batch_run([])
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        trades = load_jsonl(lab.TRADES_JSONL)
        assert len(trades) == 10

    def test_batch_run_trades_are_virtual_open(self, tmp_path):
        batch_run([])
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        trades = load_jsonl(lab.TRADES_JSONL)
        assert all(t.get("execution_state") == "virtual_open" for t in trades)


def _split_json_blocks(text: str) -> list[str]:
    """Split stdout containing multiple JSON objects into individual JSON strings."""
    blocks = []
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                blocks.append(text[start:i + 1])
                start = None
    return blocks
