"""Tests for LocalCMS daily session journal HTML views."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestLocalCMSJournalHTML(unittest.TestCase):
    """Test les vues HTML du journal quotidien dans LocalCMS."""

    def setUp(self):
        self.journal_dir = PROJECT_ROOT / "data" / "journal" / "daily"
        self.journal_dir.mkdir(parents=True, exist_ok=True)

    def _write_test_entry(self, run_id: str, data: dict | None = None) -> Path:
        if data is None:
            data = {
                "run_id": run_id,
                "session_id": "test-session",
                "journal_type": "daily_session",
                "pipeline": "E2E dry-run pipeline daily session journal",
                "dry_run": True,
                "paper_mode": True,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "duration_s": 0.5,
                "pipeline_duration_s": 0.3,
                "all_ok": True,
                "steps": [
                    {"step": "1_signal_router", "timestamp": datetime.now(timezone.utc).isoformat(), "result": {"side": "BUY", "ticker": "BTCUSDT"}},
                    {"step": "2_proposition_engine", "timestamp": datetime.now(timezone.utc).isoformat(), "result": {"action": "BUY", "confidence": 0.82}},
                    {"step": "3_validation_gate", "timestamp": datetime.now(timezone.utc).isoformat(), "result": {"verdict": "APPROVED"}},
                    {"step": "4_trade_executor", "timestamp": datetime.now(timezone.utc).isoformat(), "result": {"status": "filled", "fill_price": 65000.0}},
                    {"step": "5_result_tracker", "timestamp": datetime.now(timezone.utc).isoformat(), "result": {"outcome": "win", "net_pnl": 438.03}},
                    {"step": "6_datasheet_writer", "timestamp": datetime.now(timezone.utc).isoformat(), "result": {"dry_run": True, "written": False}},
                    {"step": "7_learning_feeder", "timestamp": datetime.now(timezone.utc).isoformat(), "result": {"bridge_status": "dry_run", "brick_stored": False}},
                ],
                "signal_source": {"engine": "e2e_dry_run", "signal": "BUY", "symbol": "BTCUSDT"},
                "proposition_summary": {"action": "BUY", "confidence": 0.82},
                "validation_verdict": "APPROVED",
                "trade_executor_status": "filled",
                "result_tracker_outcome": "win",
                "pnl_paper": {"outcome": "win", "net_pnl": "438.03"},
                "datasheet_writer": {"dry_run": True, "written": False},
                "learning_feeder": {"bridge_status": "dry_run", "brick_stored": False},
                "tmux_before": {"timestamp": datetime.now(timezone.utc).isoformat(), "active": ["openclaw-core", "screeners"], "count": 2},
                "tmux_after": {"timestamp": datetime.now(timezone.utc).isoformat(), "active": ["openclaw-core", "screeners", "strict-workers"], "count": 3},
                "localcms_before": {"/health": {"ok": True}, "/menu": {"ok": True}},
                "localcms_after": {"/health": {"ok": True}, "/menu": {"ok": True}, "/runtime/tmux": {"ok": True}},
                "localcms_ok": True,
                "closeout_required": False,
                "closeout_acknowledged": True,
            }
        path = self.journal_dir / f"{run_id}.json"
        path.write_text(json.dumps(data, default=str))
        return path

    def test_journal_entry_present(self):
        from modules.localcms.app.main import _list_journal_entries
        entries = _list_journal_entries()
        self.assertIsInstance(entries, list)

    def test_journal_entry_fields(self):
        from modules.localcms.app.main import _list_journal_entries
        p = self._write_test_entry("journal_html_test_001")
        entries = _list_journal_entries()
        run_ids = [e["run_id"] for e in entries]
        self.assertIn("journal_html_test_001", run_ids)
        entry = next(e for e in entries if e["run_id"] == "journal_html_test_001")
        self.assertIn("run_id", entry)
        self.assertIn("started_at", entry)
        self.assertIn("duration_s", entry)
        self.assertIn("all_ok", entry)
        self.assertIn("closeout_acknowledged", entry)
        self.assertIn("validation_verdict", entry)
        self.assertIn("pnl_outcome", entry)
        self.assertIn("signal", entry)
        self.assertIn("symbol", entry)
        p.unlink(missing_ok=True)

    def test_journal_html_route_registered(self):
        from modules.localcms.app.main import app
        routes = [r.path for r in app.routes]
        self.assertIn("/journal", routes)
        self.assertIn("/journal/{run_id}", routes)

    def test_journal_html_renders(self):
        from modules.localcms.app.main import _journal_html
        entries = [
            {
                "run_id": "20260516_001",
                "started_at": "2026-05-16T10:00:00+00:00",
                "duration_s": 0.5,
                "all_ok": True,
                "closeout_acknowledged": True,
                "tmux_count": 3,
                "localcms_ok": True,
                "validation_verdict": "APPROVED",
                "pnl_outcome": "win",
                "signal": "BUY",
                "symbol": "BTCUSDT",
            }
        ]
        html = _journal_html(entries)
        self.assertIn("Daily Session Journal", html)
        self.assertIn("20260516_001", html)
        self.assertIn("WIN", html)
        self.assertIn("APPROVED", html)
        self.assertIn("BTCUSDT", html)
        self.assertIn("Total Sessions", html)
        self.assertIn("Wins", html)

    def test_journal_html_multiple_entries(self):
        from modules.localcms.app.main import _journal_html
        entries = [
            {"run_id": "a", "started_at": "", "duration_s": 1, "all_ok": True,
             "closeout_acknowledged": True, "tmux_count": 3, "localcms_ok": True,
             "validation_verdict": "APPROVED", "pnl_outcome": "win", "signal": "BUY", "symbol": "BTC"},
            {"run_id": "b", "started_at": "", "duration_s": 2, "all_ok": False,
             "closeout_acknowledged": False, "tmux_count": 3, "localcms_ok": False,
             "validation_verdict": "REJECTED", "pnl_outcome": "loss", "signal": "SELL", "symbol": "ETH"},
        ]
        html = _journal_html(entries)
        self.assertIn("a", html)
        self.assertIn("b", html)
        self.assertIn("REJECTED", html)
        self.assertIn("LOSS", html)
        self.assertIn("PENDING", html)

    def test_journal_html_empty(self):
        from modules.localcms.app.main import _journal_html
        html = _journal_html([])
        self.assertIn("Daily Session Journal", html)
        self.assertIn("0", html)

    def test_journal_detail_html_renders(self):
        from modules.localcms.app.main import _journal_detail_html
        entry = {
            "run_id": "20260516_001",
            "session_id": "abc-123",
            "journal_type": "daily_session",
            "started_at": "2026-05-16T10:00:00+00:00",
            "completed_at": "2026-05-16T10:00:01+00:00",
            "duration_s": 0.5,
            "pipeline_duration_s": 0.3,
            "all_ok": True,
            "dry_run": True,
            "steps": [
                {"step": "1_signal_router", "timestamp": "2026-05-16T10:00:00", "result": {"side": "BUY"}},
                {"step": "7_learning_feeder", "timestamp": "2026-05-16T10:00:01", "result": {"bridge_status": "dry_run"}},
            ],
            "signal_source": {"signal": "BUY", "symbol": "BTCUSDT"},
            "proposition_summary": {"action": "BUY", "confidence": 0.82},
            "validation_verdict": "APPROVED",
            "trade_executor_status": "filled",
            "result_tracker_outcome": "win",
            "pnl_paper": {"outcome": "win", "net_pnl": "438.03"},
            "datasheet_writer": {"dry_run": True, "written": False},
            "learning_feeder": {"bridge_status": "dry_run", "brick_stored": False},
            "tmux_before": {"count": 2, "active": ["a", "b"]},
            "tmux_after": {"count": 3, "active": ["a", "b", "c"]},
            "localcms_before": {"/health": {"ok": True}},
            "localcms_after": {"/health": {"ok": True}, "/menu": {"ok": True}},
            "localcms_ok": True,
            "closeout_required": False,
            "closeout_acknowledged": True,
        }
        html = _journal_detail_html(entry)
        self.assertIn("20260516_001", html)
        self.assertIn("WIN", html)
        self.assertIn("APPROVED", html)
        self.assertIn("BTCUSDT", html)
        self.assertIn("Pipeline Steps", html)
        self.assertIn("TMUX Snapshots", html)
        self.assertIn("LocalCMS Snapshots", html)
        self.assertIn("CLOSED", html)

    def test_journal_detail_shows_loss(self):
        from modules.localcms.app.main import _journal_detail_html
        entry = {
            "run_id": "loss_test",
            "session_id": "",
            "journal_type": "daily_session",
            "started_at": "",
            "duration_s": 0,
            "all_ok": False,
            "dry_run": True,
            "steps": [],
            "signal_source": {"signal": "SELL", "symbol": "ETHUSDT"},
            "proposition_summary": {"action": "SELL", "confidence": 0.3},
            "validation_verdict": "REJECTED",
            "trade_executor_status": "skipped",
            "result_tracker_outcome": "loss",
            "pnl_paper": {"outcome": "loss", "net_pnl": "-100.00"},
            "datasheet_writer": {"dry_run": True, "written": False},
            "learning_feeder": {"bridge_status": "dry_run", "brick_stored": False},
            "tmux_before": {"count": 0, "active": []},
            "tmux_after": {"count": 0, "active": []},
            "localcms_before": {},
            "localcms_after": {},
            "localcms_ok": False,
            "closeout_required": False,
            "closeout_acknowledged": False,
        }
        html = _journal_detail_html(entry)
        self.assertIn("loss_test", html)
        self.assertIn("LOSS", html)
        self.assertIn("REJECTED", html)
        self.assertIn("PENDING", html)
        self.assertIn("ETHUSDT", html)

    def test_journal_detail_api_link(self):
        from modules.localcms.app.main import _journal_detail_html
        entry = {
            "run_id": "detail_api_test",
            "session_id": "",
            "journal_type": "daily_session",
            "started_at": "",
            "duration_s": 0,
            "all_ok": True,
            "dry_run": True,
            "steps": [],
            "signal_source": {},
            "proposition_summary": {},
            "validation_verdict": "",
            "trade_executor_status": "",
            "result_tracker_outcome": "",
            "pnl_paper": {},
            "datasheet_writer": {},
            "learning_feeder": {},
            "tmux_before": {},
            "tmux_after": {},
            "localcms_before": {},
            "localcms_after": {},
            "localcms_ok": False,
            "closeout_required": False,
            "closeout_acknowledged": False,
        }
        html = _journal_detail_html(entry)
        self.assertIn("/journal/daily/detail_api_test", html)

    def test_pnl_badge_win(self):
        from modules.localcms.app.main import _pnl_badge
        self.assertIn("WIN", _pnl_badge("win"))

    def test_pnl_badge_loss(self):
        from modules.localcms.app.main import _pnl_badge
        self.assertIn("LOSS", _pnl_badge("loss"))

    def test_pnl_badge_breakeven(self):
        from modules.localcms.app.main import _pnl_badge
        self.assertIn("BREAKEVEN", _pnl_badge("breakeven"))

    def test_pnl_badge_unknown(self):
        from modules.localcms.app.main import _pnl_badge
        self.assertIn("unknown", _pnl_badge("foobar").lower())

    def test_verdict_badge_approved(self):
        from modules.localcms.app.main import _verdict_badge
        self.assertIn("APPROVED", _verdict_badge("APPROVED"))

    def test_verdict_badge_rejected(self):
        from modules.localcms.app.main import _verdict_badge
        self.assertIn("REJECTED", _verdict_badge("REJECTED"))

    def test_closeout_badge_acknowledged(self):
        from modules.localcms.app.main import _closeout_badge
        self.assertIn("CLOSED", _closeout_badge(True))

    def test_closeout_badge_pending(self):
        from modules.localcms.app.main import _closeout_badge
        self.assertIn("PENDING", _closeout_badge(False))


if __name__ == "__main__":
    unittest.main()
