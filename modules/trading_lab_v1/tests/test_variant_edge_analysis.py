"""
Tests for variant-report command and variant filter in run_with_outcomes.

Run: pytest modules/trading_lab_v1/tests/test_variant_edge_analysis.py -q
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.trading_lab_v1.app.trading_lab_v1 import (
    run_with_outcomes,
    variant_report,
    load_jsonl,
    SAMPLE_MARKET_CSV,
)


@pytest.fixture(autouse=True)
def _clean_state(tmp_path, monkeypatch):
    import modules.trading_lab_v1.app.trading_lab_v1 as lab
    monkeypatch.setattr(lab, "TRADES_JSONL", tmp_path / "trades.jsonl")
    monkeypatch.setattr(lab, "FEATURES_JSONL", tmp_path / "features.jsonl")
    monkeypatch.setattr(lab, "EVENTS_JSONL", tmp_path / "events.jsonl")
    monkeypatch.setattr(lab, "MARKET_RUNS_JSONL", tmp_path / "market_runs.jsonl")
    monkeypatch.setattr(lab, "BATCH_REPORTS_JSONL", tmp_path / "batch_reports.jsonl")


# ── variant_report ────────────────────────────────────────────────────────────

class TestVariantReport:
    def test_empty_trades_returns_empty_dict(self, capsys):
        variant_report([])
        out = capsys.readouterr().out
        assert json.loads(out) == {}

    def test_report_has_expected_keys(self, capsys):
        run_with_outcomes([])
        capsys.readouterr()
        variant_report([])
        out = capsys.readouterr().out
        report = json.loads(out)
        assert len(report) > 0
        for metrics in report.values():
            for key in ("n", "win", "loss", "timeout", "win_rate", "avg_r"):
                assert key in metrics

    def test_counts_are_consistent(self, capsys):
        run_with_outcomes([])
        capsys.readouterr()
        variant_report([])
        report = json.loads(capsys.readouterr().out)
        for m in report.values():
            assert m["win"] + m["loss"] + m["timeout"] == m["n"]

    def test_win_rate_matches_win_over_n(self, capsys):
        run_with_outcomes([])
        capsys.readouterr()
        variant_report([])
        report = json.loads(capsys.readouterr().out)
        for m in report.values():
            if m["n"] > 0:
                assert m["win_rate"] == round(m["win"] / m["n"], 4)

    def test_all_variants_present(self, capsys):
        run_with_outcomes([])
        capsys.readouterr()
        variant_report([])
        report = json.loads(capsys.readouterr().out)
        # sample CSV produces 4 variants across 10 sessions (all non-neutral)
        assert len(report) == 4

    def test_total_n_matches_trade_count(self, capsys):
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        run_with_outcomes([])
        capsys.readouterr()
        trade_count = len(load_jsonl(lab.TRADES_JSONL))
        variant_report([])
        report = json.loads(capsys.readouterr().out)
        assert sum(m["n"] for m in report.values()) == trade_count


# ── variant filter in run_with_outcomes ──────────────────────────────────────

class TestVariantFilter:
    def _variants_from_run(self, lab) -> list[str]:
        return sorted({t["variant_id"] for t in load_jsonl(lab.TRADES_JSONL) if t.get("variant_id")})

    def test_filter_produces_only_matching_variant(self, capsys):
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        run_with_outcomes([])
        capsys.readouterr()
        all_variants = self._variants_from_run(lab)
        assert all_variants, "sample CSV must produce at least one variant"

        target = all_variants[0]
        run_with_outcomes([str(SAMPLE_MARKET_CSV), "", "", "", target])
        capsys.readouterr()
        filtered = load_jsonl(lab.TRADES_JSONL)
        assert all(t.get("variant_id") == target for t in filtered)

    def test_filter_reduces_trade_count(self, capsys):
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        run_with_outcomes([])
        capsys.readouterr()
        all_variants = self._variants_from_run(lab)
        if len(all_variants) < 2:
            pytest.skip("need at least 2 variants to test reduction")
        all_count = len(load_jsonl(lab.TRADES_JSONL))

        target = all_variants[0]
        run_with_outcomes([str(SAMPLE_MARKET_CSV), "", "", "", target])
        capsys.readouterr()
        assert len(load_jsonl(lab.TRADES_JSONL)) < all_count

    def test_empty_filter_allows_all(self, capsys):
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        run_with_outcomes([])
        capsys.readouterr()
        all_count = len(load_jsonl(lab.TRADES_JSONL))

        run_with_outcomes([str(SAMPLE_MARKET_CSV), "", "", "", ""])
        capsys.readouterr()
        assert len(load_jsonl(lab.TRADES_JSONL)) == all_count

    def test_unknown_variant_produces_zero_trades(self, capsys):
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        run_with_outcomes([str(SAMPLE_MARKET_CSV), "", "", "", "variant_does_not_exist"])
        capsys.readouterr()
        assert len(load_jsonl(lab.TRADES_JSONL)) == 0

    def test_multi_variant_filter_comma_separated(self, capsys):
        import modules.trading_lab_v1.app.trading_lab_v1 as lab
        run_with_outcomes([])
        capsys.readouterr()
        all_variants = self._variants_from_run(lab)
        if len(all_variants) < 2:
            pytest.skip("need at least 2 variants")

        v1, v2 = all_variants[0], all_variants[1]
        run_with_outcomes([str(SAMPLE_MARKET_CSV), "", "", "", f"{v1},{v2}"])
        capsys.readouterr()
        filtered = load_jsonl(lab.TRADES_JSONL)
        allowed = {v1, v2}
        assert all(t.get("variant_id") in allowed for t in filtered)
