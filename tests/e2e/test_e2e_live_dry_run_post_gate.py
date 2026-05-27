"""
E2E live/dry-run post-gate pipeline tests.

Vérifie :
- Preflight flags (ALLOW_E2E_LIVE_DRY_RUN, DRY_RUN, ALLOW_LIVE_TRADE)
- Chaîne post-gate complète en mode dry-run contrôlé
- gate papier approuvée requise avant trade_executor
- fake sheets + learning_feeder dry-run
- LocalCMS gate comportement default/require
- Aucun appel externe réel (exchange, Telegram, Google Sheets)
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = PROJECT_ROOT / "scripts" / "e2e" / "dry_run_pipeline.py"

_BASE_ENV = {
    **os.environ,
    "DRY_RUN": "1",
    "PAPER_MODE": "1",
    "ALLOW_E2E_LIVE_DRY_RUN": "1",
}
# Ensure forbidden flags are absent by default
for _k in ("ALLOW_LIVE_TRADE", "ALLOW_GOOGLE_SHEETS_API_WRITE", "ALLOW_TELEGRAM_SEND",
           "REQUIRE_LOCALCMS_E2E", "SKIP_LOCALCMS_E2E", "LOCALCMS_URL"):
    _BASE_ENV.pop(_k, None)


def _run(extra: dict | None = None, drop: list | None = None, timeout: int = 30) -> tuple[int, dict]:
    env = {**_BASE_ENV}
    if drop:
        for k in drop:
            env.pop(k, None)
    if extra:
        env.update(extra)
    r = subprocess.run(
        [sys.executable, str(_SCRIPT)],
        capture_output=True, text=True, timeout=timeout, env=env,
    )
    try:
        report = json.loads(r.stdout)
    except json.JSONDecodeError:
        report = {}
    return r.returncode, report


def _make_proposition(action: str = "BUY", confidence: float = 0.82) -> object:
    from modules.proposition_engine.app.schema import Proposition
    return Proposition(
        request_id="test_req",
        signal_id="test_sig",
        action=action,
        size_pct=0.15,
        entry=65000.0,
        sl=63000.0,
        tp=68000.0,
        confidence=confidence,
        rationale="test",
        engines_context={},
        duration_ms=5,
        dry_run=True,
        status="ok",
    )


def _make_trade_result() -> object:
    from modules.trade_executor.app.schema import TradeResult
    return TradeResult(
        request_id="test_req",
        signal_id="test_sig",
        trade_id="paper_BTCUSDT_abc123",
        action="BUY",
        ticker="BTCUSDT",
        fill_price=65000.0,
        fill_qty=0.15,
        size_pct=0.15,
        sl=63000.0,
        tp=68000.0,
        status="dry_run",
        reason="paper_filled",
        duration_ms=5,
        dry_run=True,
    )


def _make_trade_record() -> object:
    from modules.result_tracker.app.schema import CloseRequest
    from modules.result_tracker.app.tracker import ResultTracker
    return ResultTracker().track(CloseRequest(
        trade_result=_make_trade_result(),
        close_price=68000.0,
        dry_run=True,
    ))


# ── Preflight flag tests ──────────────────────────────────────────────────────

class TestPreflightFlags(unittest.TestCase):

    def test_blocked_without_allow_e2e_flag(self):
        rc, report = _run(drop=["ALLOW_E2E_LIVE_DRY_RUN"])
        self.assertEqual(rc, 1, "Should exit 1 without ALLOW_E2E_LIVE_DRY_RUN=1")
        pg = report.get("e2e_post_gate_status", {})
        self.assertEqual(pg.get("status"), "BLOCKED")
        self.assertIn("ALLOW_E2E_LIVE_DRY_RUN", pg.get("reason", ""))

    def test_blocked_when_dry_run_not_set(self):
        rc, report = _run(drop=["DRY_RUN"])
        self.assertEqual(rc, 1, "Should exit 1 when DRY_RUN is absent")
        pg = report.get("e2e_post_gate_status", {})
        self.assertEqual(pg.get("status"), "BLOCKED")
        self.assertIn("DRY_RUN", pg.get("reason", ""))

    def test_blocked_when_dry_run_false(self):
        rc, report = _run(extra={"DRY_RUN": "0"})
        self.assertEqual(rc, 1, "Should exit 1 when DRY_RUN=0")
        pg = report.get("e2e_post_gate_status", {})
        self.assertEqual(pg.get("status"), "BLOCKED")

    def test_blocked_when_allow_live_trade_set(self):
        rc, report = _run(extra={"ALLOW_LIVE_TRADE": "1"})
        self.assertEqual(rc, 1, "ALLOW_LIVE_TRADE=1 must block the run")
        pg = report.get("e2e_post_gate_status", {})
        self.assertEqual(pg.get("status"), "BLOCKED")
        self.assertIn("ALLOW_LIVE_TRADE", pg.get("reason", ""))

    def test_blocked_report_has_all_fields(self):
        rc, report = _run(drop=["ALLOW_E2E_LIVE_DRY_RUN"])
        pg = report.get("e2e_post_gate_status", {})
        for field in ("status", "reason", "dry_run", "live_trade", "gate_status",
                      "localcms_gate", "sheets_mode", "telegram_mode", "modules"):
            self.assertIn(field, pg, f"Missing field in BLOCKED report: {field}")

    def test_blocked_report_live_trade_false_without_flag(self):
        rc, report = _run(drop=["ALLOW_E2E_LIVE_DRY_RUN"])
        pg = report.get("e2e_post_gate_status", {})
        self.assertFalse(pg.get("live_trade"))

    def test_blocked_report_live_trade_true_when_set(self):
        rc, report = _run(extra={"ALLOW_LIVE_TRADE": "1"})
        pg = report.get("e2e_post_gate_status", {})
        self.assertTrue(pg.get("live_trade"))


# ── Post-gate pipeline success tests ─────────────────────────────────────────

class TestPostGatePipelineSuccess(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rc, report = _run()
        cls.rc = rc
        cls.report = report
        cls.pg = report.get("e2e_post_gate_status", {})

    def test_exits_0(self):
        self.assertEqual(self.rc, 0, f"Pipeline should exit 0\nreport: {self.report}")

    def test_e2e_post_gate_status_pass(self):
        self.assertEqual(self.pg.get("status"), "PASS")

    def test_dry_run_true_in_status(self):
        self.assertTrue(self.pg.get("dry_run"))

    def test_live_trade_false_in_status(self):
        self.assertFalse(self.pg.get("live_trade"))

    def test_gate_status_approved_paper(self):
        self.assertEqual(self.pg.get("gate_status"), "APPROVED_PAPER")

    def test_sheets_mode_fake(self):
        self.assertEqual(self.pg.get("sheets_mode"), "fake")

    def test_telegram_mode_dry_run(self):
        self.assertEqual(self.pg.get("telegram_mode"), "dry_run")

    def test_all_7_modules_pass(self):
        modules = self.pg.get("modules", {})
        for mod in ("signal_router", "proposition_engine", "validation_gate",
                    "trade_executor", "result_tracker", "datasheet_writer",
                    "learning_feeder"):
            self.assertEqual(modules.get(mod), "PASS", f"{mod} should be PASS, got {modules.get(mod)}")

    def test_pipeline_name_updated(self):
        self.assertEqual(self.report.get("pipeline"), "E2E post-gate live/dry-run")

    def test_report_dry_run_true(self):
        self.assertTrue(self.report.get("dry_run"))

    def test_all_ok_true(self):
        self.assertTrue(self.report.get("all_ok"))

    def test_e2e_status_pass(self):
        self.assertEqual(self.report.get("e2e_status"), "PASS")

    def test_7_steps_present(self):
        step_names = [s["step"] for s in self.report.get("steps", [])]
        for name in ("1_signal_router", "2_proposition_engine", "3_validation_gate",
                     "4_trade_executor", "5_result_tracker", "6_datasheet_writer",
                     "7_learning_feeder"):
            self.assertIn(name, step_names)

    def test_trade_executor_dry_run_true(self):
        for s in self.report.get("steps", []):
            if s["step"] == "4_trade_executor":
                self.assertTrue(s["result"].get("dry_run"), "trade_executor must be dry_run")

    def test_datasheet_writer_not_written(self):
        for s in self.report.get("steps", []):
            if s["step"] == "6_datasheet_writer":
                self.assertFalse(s["result"].get("written", True))
                self.assertTrue(s["result"].get("dry_run"))

    def test_learning_feeder_bridge_dry_run(self):
        for s in self.report.get("steps", []):
            if s["step"] == "7_learning_feeder":
                self.assertEqual(s["result"].get("bridge_status"), "dry_run")
                self.assertFalse(s["result"].get("brick_stored"))


# ── LocalCMS gate behavior ────────────────────────────────────────────────────

class TestLocalcmsGateBehavior(unittest.TestCase):

    def test_localcms_absent_default_warn_skipped_e2e_continues(self):
        rc, report = _run()
        self.assertEqual(rc, 0, "E2E should continue when LocalCMS absent in default mode")
        gate = report.get("localcms_gate", {})
        self.assertEqual(gate.get("status"), "WARN_SKIPPED")
        pg = report.get("e2e_post_gate_status", {})
        self.assertEqual(pg.get("status"), "PASS")
        self.assertEqual(pg.get("localcms_gate"), "WARN_SKIPPED")

    def test_require_localcms_absent_blocked(self):
        rc, report = _run(extra={"REQUIRE_LOCALCMS_E2E": "1"})
        self.assertEqual(rc, 1, "REQUIRE_LOCALCMS_E2E=1 + LocalCMS absent should exit 1")
        gate = report.get("localcms_gate", {})
        self.assertEqual(gate.get("status"), "BLOCKED")

    def test_skip_localcms_exits_0(self):
        rc, _ = _run(extra={"SKIP_LOCALCMS_E2E": "1"})
        self.assertEqual(rc, 0)


# ── Gate rejection blocks trade_executor ──────────────────────────────────────

class TestGateRejectionBlocksTradeExecutor(unittest.TestCase):
    """Unit-level: trade_executor rejects when gate verdict is not APPROVED."""

    def test_rejected_gate_blocks_trade(self):
        from modules.validation_gate.app.schema import GateDecision
        from modules.trade_executor.app.schema import TradeRequest
        from modules.trade_executor.app.executor import TradeExecutor

        prop = _make_proposition()
        rejected_decision = GateDecision(
            request_id="test_req",
            signal_id="test_sig",
            verdict="REJECTED",
            reason="risk_limit_exceeded",
            risk_status="BLOCK",
            risk_reason="risk_limit_exceeded",
            duration_ms=1,
            dry_run=True,
        )
        req = TradeRequest(
            gate_decision=rejected_decision,
            proposition=prop,
            ticker="BTCUSDT",
            dry_run=True,
        )
        result = TradeExecutor().execute(req)
        self.assertEqual(result.status, "rejected", "TradeExecutor must reject when gate is not APPROVED")
        self.assertIn("gate_not_approved", result.reason)

    def test_hold_gate_blocks_trade(self):
        from modules.validation_gate.app.schema import GateDecision
        from modules.trade_executor.app.schema import TradeRequest
        from modules.trade_executor.app.executor import TradeExecutor

        prop = _make_proposition()
        hold_decision = GateDecision(
            request_id="test_req",
            signal_id="test_sig",
            verdict="HOLD",
            reason="operator_timeout",
            risk_status="ALLOW",
            risk_reason="ok",
            duration_ms=1,
            dry_run=True,
        )
        req = TradeRequest(
            gate_decision=hold_decision,
            proposition=prop,
            ticker="BTCUSDT",
            dry_run=True,
        )
        result = TradeExecutor().execute(req)
        self.assertEqual(result.status, "rejected")

    def test_approved_gate_allows_trade_dry_run(self):
        from modules.validation_gate.app.schema import GateRequest
        from modules.validation_gate.app.gate import ValidationGate
        from modules.trade_executor.app.schema import TradeRequest
        from modules.trade_executor.app.executor import TradeExecutor

        prop = _make_proposition()
        decision = ValidationGate().gate(GateRequest(
            proposition=prop, ticker="BTCUSDT", dry_run=True, require_operator=False))
        self.assertEqual(decision.verdict, "APPROVED")

        result = TradeExecutor().execute(TradeRequest(
            gate_decision=decision, proposition=prop, ticker="BTCUSDT", dry_run=True))
        self.assertIn(result.status, ("dry_run", "filled"))
        self.assertTrue(result.dry_run)


# ── Fake sheets integration ────────────────────────────────────────────────────

class TestFakeSheetsIntegration(unittest.TestCase):

    def test_fake_sheets_receives_payload_ref(self):
        from modules.datasheet_writer.app.sheets_adapter import write_trade_to_sheets
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter, FakeSheetsClient
        record = _make_trade_record()
        writer = SheetsWriter(client=FakeSheetsClient())
        result = write_trade_to_sheets(record, writer, payload_ref="data/datasheet/test.jsonl")
        self.assertTrue(result.ok)
        self.assertEqual(result.mode, "fake")
        self.assertEqual(result.rows_written, 1)

    def test_fake_sheets_no_google_api_call(self):
        from modules.datasheet_writer.app.sheets_adapter import write_trade_to_sheets
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter, FakeSheetsClient
        record = _make_trade_record()
        google_mods_before = {k for k in sys.modules if "google" in k.lower() and "oauth" in k.lower()}
        write_trade_to_sheets(record, SheetsWriter(client=FakeSheetsClient()), payload_ref="ref.jsonl")
        google_mods_after = {k for k in sys.modules if "google" in k.lower() and "oauth" in k.lower()}
        new_mods = google_mods_after - google_mods_before
        self.assertEqual(new_mods, set(), f"Google OAuth modules loaded: {new_mods}")

    def test_datasheet_writer_dry_run_no_write(self):
        from modules.datasheet_writer.app.writer import DatasheetWriter
        record = _make_trade_record()
        result = DatasheetWriter().write(record, dry_run=True)
        self.assertTrue(result.dry_run)
        self.assertFalse(result.written)
        self.assertTrue(result.ok)


# ── Learning feeder dry-run ────────────────────────────────────────────────────

class TestLearningFeederDryRun(unittest.TestCase):

    def test_learning_feeder_dry_run_returns_dry_run_status(self):
        from modules.learning_feeder.app.feeder import LearningFeeder
        from modules.learning_feeder.app.schema import FeedRequest
        prop = _make_proposition()
        record = _make_trade_record()
        req = FeedRequest(
            signal_id=record.signal_id,
            proposition=prop,
            trade_record=record,
            dry_run=True,
            store_brick=False,
        )
        result = LearningFeeder().feed(req)
        self.assertEqual(result.bridge_status, "dry_run")
        self.assertFalse(result.brick_stored)
        self.assertTrue(result.dry_run)
        self.assertIsInstance(result.summary, str)
        self.assertGreater(len(result.summary), 0)

    def test_learning_feeder_dry_run_no_brick_stored(self):
        from modules.learning_feeder.app.feeder import LearningFeeder
        from modules.learning_feeder.app.schema import FeedRequest
        import tempfile
        prop = _make_proposition()
        record = _make_trade_record()
        tmp = Path(tempfile.mkdtemp())
        req = FeedRequest(
            signal_id=record.signal_id,
            proposition=prop,
            trade_record=record,
            dry_run=True,
            store_brick=True,  # even if store_brick=True, dry_run wins
        )
        result = LearningFeeder(bricks_dir=tmp).feed(req)
        self.assertFalse(result.brick_stored, "dry_run=True must prevent brick storage")
        bricks = list(tmp.rglob("*.json"))
        self.assertEqual(len(bricks), 0, "No brick files should be created in dry_run mode")


# ── No external calls ─────────────────────────────────────────────────────────

class TestNoExternalCalls(unittest.TestCase):

    def test_script_has_no_direct_gspread_import(self):
        text = _SCRIPT.read_text()
        self.assertNotIn("gspread", text)
        self.assertNotIn("google.oauth2", text)

    def test_script_has_no_direct_telegram_send(self):
        text = _SCRIPT.read_text()
        self.assertNotIn("send_telegram(", text)
        self.assertNotIn("send_telegram_html(", text)

    def test_script_all_dispatcher_calls_are_dry_run(self):
        lines = _SCRIPT.read_text().splitlines()
        dispatch_indices = [i for i, ln in enumerate(lines) if "dispatcher.dispatch(" in ln]
        self.assertGreater(len(dispatch_indices), 0, "No dispatcher.dispatch calls found")
        for idx in dispatch_indices:
            window = "\n".join(lines[idx:idx + 30])
            self.assertIn("dry_run=True", window,
                          f"dispatcher.dispatch at line {idx+1} not guarded by dry_run=True")

    def test_no_bitget_in_script(self):
        text = _SCRIPT.read_text()
        self.assertNotIn("bitget", text.lower())

    def test_no_exchange_order_calls(self):
        text = _SCRIPT.read_text()
        self.assertNotIn(".post(", text)
        for method in ("create_order", "place_order", "submit_order"):
            self.assertNotIn(method, text)

    def test_no_google_module_loaded_during_pipeline(self):
        rc, report = _run()
        self.assertEqual(rc, 0)
        for s in report.get("steps", []):
            res = s.get("result", {})
            if isinstance(res, dict):
                self.assertNotIn("gspread", str(res))
                self.assertNotIn("google.oauth2", str(res))


if __name__ == "__main__":
    unittest.main(verbosity=2)
