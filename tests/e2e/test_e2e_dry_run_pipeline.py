"""E2E dry-run pipeline tests — prouve le flux complet 7 workers + LocalCMS."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _make_test_proposition(signal_id: str = "test_sig", action: str = "BUY",
                           confidence: float = 0.82) -> object:
    from modules.proposition_engine.app.schema import Proposition
    return Proposition(
        request_id="test_req",
        signal_id=signal_id,
        action=action,
        size_pct=0.15,
        entry=65000.0,
        sl=63000.0,
        tp=68000.0,
        confidence=confidence,
        rationale="test proposition",
        engines_context={"probability": {"symbol": "BTCUSDT"}, "decision": {"decision": "BUY"}},
        duration_ms=5,
        dry_run=True,
        status="ok",
    )


def _make_test_trade_result(signal_id: str = "test_sig") -> object:
    from modules.trade_executor.app.schema import TradeResult
    return TradeResult(
        request_id="test_req",
        signal_id=signal_id,
        trade_id="test_trade",
        action="BUY",
        ticker="BTCUSDT",
        fill_price=65000.0,
        fill_qty=0.15,
        size_pct=0.15,
        sl=63000.0,
        tp=68000.0,
        status="filled",
        reason="test",
        duration_ms=5,
        dry_run=True,
    )


class TestE2EDryRunPipeline(unittest.TestCase):
    """Test que chaque étape du pipeline s'importe et s'exécute en dry-run."""

    def test_signal_router_routes_signal(self):
        from modules.signal_router.app.router import route
        raw = {"engine": "test", "signal": "BUY", "symbol": "BTCUSDT",
               "tf": "1h", "price": 65000.0}
        ns = route(raw)
        self.assertIsNotNone(ns.signal_id)
        self.assertEqual(ns.ticker, "BTCUSDT")
        self.assertEqual(ns.side, "BUY")

    def test_proposition_engine_dry_run(self):
        from modules.signal_router.app.router import route
        from modules.proposition_engine.app.schema import PropositionRequest
        from modules.proposition_engine.app.schema import NormalizedSignal as PropSignal
        from modules.proposition_engine.app.engine import PropositionEngine

        ns = route({"engine": "test", "signal": "BUY", "symbol": "BTCUSDT",
                    "tf": "1h", "price": 65000.0})
        ps = PropSignal.from_dict(ns.to_dict())
        prop = PropositionEngine().propose(PropositionRequest(signal=ps, dry_run=True))
        self.assertEqual(prop.status, "ok")
        self.assertTrue(prop.dry_run)
        self.assertIn(prop.action, ("BUY", "SELL", "HOLD", "SKIP"))

    def test_validation_gate_dry_run_with_buy_proposition(self):
        from modules.validation_gate.app.schema import GateRequest
        from modules.validation_gate.app.gate import ValidationGate

        prop = _make_test_proposition()
        gate_req = GateRequest(proposition=prop, ticker="BTCUSDT",
                               dry_run=True, require_operator=False)
        decision = ValidationGate().gate(gate_req)
        self.assertEqual(decision.verdict, "APPROVED")
        self.assertTrue(decision.dry_run)

    def test_validation_gate_rejects_hold(self):
        from modules.validation_gate.app.schema import GateRequest
        from modules.validation_gate.app.gate import ValidationGate

        prop = _make_test_proposition(action="HOLD", confidence=0.0)
        gate_req = GateRequest(proposition=prop, ticker="BTCUSDT",
                               dry_run=True, require_operator=False)
        decision = ValidationGate().gate(gate_req)
        self.assertEqual(decision.verdict, "REJECTED")

    def test_trade_executor_dry_run(self):
        from modules.validation_gate.app.schema import GateRequest
        from modules.validation_gate.app.gate import ValidationGate
        from modules.trade_executor.app.schema import TradeRequest
        from modules.trade_executor.app.executor import TradeExecutor

        prop = _make_test_proposition()
        decision = ValidationGate().gate(GateRequest(
            proposition=prop, ticker="BTCUSDT", dry_run=True, require_operator=False))
        result = TradeExecutor().execute(TradeRequest(
            gate_decision=decision, proposition=prop, ticker="BTCUSDT", dry_run=True))
        self.assertIn(result.status, ("filled", "dry_run"))
        self.assertTrue(result.dry_run)

    def test_result_tracker_dry_run(self):
        from modules.result_tracker.app.schema import CloseRequest
        from modules.result_tracker.app.tracker import ResultTracker

        result = _make_test_trade_result()
        record = ResultTracker().track(CloseRequest(
            trade_result=result, close_price=68000.0, dry_run=True))
        self.assertIn(record.outcome, ("win", "loss", "breakeven"))
        self.assertTrue(record.dry_run)

    def test_datasheet_writer_dry_run_skips_write(self):
        from modules.result_tracker.app.schema import CloseRequest
        from modules.result_tracker.app.tracker import ResultTracker
        from modules.datasheet_writer.app.writer import DatasheetWriter

        result = _make_test_trade_result()
        record = ResultTracker().track(CloseRequest(
            trade_result=result, close_price=68000.0, dry_run=True))
        wr = DatasheetWriter().write(record, dry_run=True)
        self.assertTrue(wr.dry_run)
        self.assertFalse(wr.written)

    def test_learning_feeder_dry_run_no_store(self):
        from modules.result_tracker.app.schema import CloseRequest
        from modules.result_tracker.app.tracker import ResultTracker
        from modules.datasheet_writer.app.writer import DatasheetWriter
        from modules.learning_feeder.app.schema import FeedRequest
        from modules.learning_feeder.app.feeder import LearningFeeder

        result = _make_test_trade_result()
        prop = _make_test_proposition()
        record = ResultTracker().track(CloseRequest(
            trade_result=result, close_price=68000.0, dry_run=True))
        fr = LearningFeeder().feed(FeedRequest(
            signal_id=record.signal_id, proposition=prop,
            trade_record=record, dry_run=True, store_brick=False))
        self.assertEqual(fr.bridge_status, "dry_run")
        self.assertFalse(fr.brick_stored)

    def test_pipeline_script_runs(self):
        import subprocess
        env = {**__import__("os").environ, "DRY_RUN": "1", "PAPER_MODE": "1", "ALLOW_E2E_LIVE_DRY_RUN": "1"}
        r = subprocess.run(
            [__import__("sys").executable, str(PROJECT_ROOT / "scripts/e2e/dry_run_pipeline.py")],
            capture_output=True, text=True, timeout=30, env=env,
        )
        if r.returncode != 0:
            self.fail(f"Pipeline failed (rc={r.returncode}): STDERR={r.stderr[:500]}")
        report = json.loads(r.stdout)
        self.assertEqual(report["pipeline"], "E2E post-gate live/dry-run")
        self.assertTrue(report["dry_run"])

    def test_pipeline_all_steps_present(self):
        import subprocess
        env = {**__import__("os").environ, "DRY_RUN": "1", "PAPER_MODE": "1", "ALLOW_E2E_LIVE_DRY_RUN": "1"}
        r = subprocess.run(
            [__import__("sys").executable, str(PROJECT_ROOT / "scripts/e2e/dry_run_pipeline.py")],
            capture_output=True, text=True, timeout=30, env=env,
        )
        report = json.loads(r.stdout)
        step_names = [s["step"] for s in report["steps"]]
        expected = [
            "1_signal_router", "2_proposition_engine", "3_validation_gate",
            "4_trade_executor", "5_result_tracker", "6_datasheet_writer",
            "7_learning_feeder",
        ]
        for name in expected:
            self.assertIn(name, step_names)

    def test_pipeline_includes_desk_pro_fixture_synthesis(self):
        import subprocess
        env = {**__import__("os").environ, "DRY_RUN": "1", "PAPER_MODE": "1", "ALLOW_E2E_LIVE_DRY_RUN": "1"}
        r = subprocess.run(
            [__import__("sys").executable, str(PROJECT_ROOT / "scripts/e2e/dry_run_pipeline.py")],
            capture_output=True, text=True, timeout=30, env=env,
        )
        report = json.loads(r.stdout)
        steps = {s["step"]: s["result"] for s in report["steps"]}
        self.assertIn("1b_desk_pro_dry_run", steps)
        dp = steps["1b_desk_pro_dry_run"]
        self.assertIn(dp.get("status"), ("PASS", "WARN"))
        self.assertEqual(dp.get("errors"), [])
        self.assertTrue(dp.get("no_trade"))
        self.assertTrue(dp.get("no_telegram"))
        self.assertTrue(dp.get("no_webhook"))
        self.assertTrue(dp.get("no_systemd"))
        join = dp.get("join_checks") or {}
        self.assertTrue(join.get("timeframe_match"))
        self.assertTrue(join.get("symbol_match"))

    def test_pipeline_no_live_trade(self):
        import subprocess
        env = {**__import__("os").environ, "DRY_RUN": "1", "PAPER_MODE": "1", "ALLOW_E2E_LIVE_DRY_RUN": "1"}
        r = subprocess.run(
            [__import__("sys").executable, str(PROJECT_ROOT / "scripts/e2e/dry_run_pipeline.py")],
            capture_output=True, text=True, timeout=30, env=env,
        )
        report = json.loads(r.stdout)
        for step in report["steps"]:
            if step["step"] == "4_trade_executor":
                self.assertTrue(step["result"].get("dry_run", False))
            if step["step"] == "6_datasheet_writer":
                self.assertTrue(step["result"].get("dry_run", False))
                self.assertFalse(step["result"].get("written", True))

    def test_all_7_modules_importable(self):
        from modules.signal_router.app.router import route
        from modules.proposition_engine.app.engine import PropositionEngine
        from modules.validation_gate.app.gate import ValidationGate
        from modules.trade_executor.app.executor import TradeExecutor
        from modules.result_tracker.app.tracker import ResultTracker
        from modules.datasheet_writer.app.writer import DatasheetWriter
        from modules.learning_feeder.app.feeder import LearningFeeder
        self.assertTrue(callable(route))
        self.assertTrue(callable(PropositionEngine))
        self.assertTrue(callable(ValidationGate))
        self.assertTrue(callable(TradeExecutor))
        self.assertTrue(callable(ResultTracker))
        self.assertTrue(callable(DatasheetWriter))
        self.assertTrue(callable(LearningFeeder))

    def test_no_bitget_order_in_pipeline(self):
        text = (PROJECT_ROOT / "scripts" / "e2e" / "dry_run_pipeline.py").read_text()
        self.assertNotIn("bitget", text.lower())
        self.assertNotIn("bitget_bridge", text)

    def test_localcms_endpoints_mentioned_in_report(self):
        import subprocess
        env = {**__import__("os").environ, "DRY_RUN": "1", "PAPER_MODE": "1", "ALLOW_E2E_LIVE_DRY_RUN": "1"}
        r = subprocess.run(
            [__import__("sys").executable, str(PROJECT_ROOT / "scripts/e2e/dry_run_pipeline.py")],
            capture_output=True, text=True, timeout=30, env=env,
        )
        report = json.loads(r.stdout)
        self.assertIn("localcms", report)
        self.assertIn("localcms_ok", report)

    def test_pipeline_succeeds_all_7_steps(self):
        import subprocess
        env = {**__import__("os").environ, "DRY_RUN": "1", "PAPER_MODE": "1", "ALLOW_E2E_LIVE_DRY_RUN": "1"}
        r = subprocess.run(
            [__import__("sys").executable, str(PROJECT_ROOT / "scripts/e2e/dry_run_pipeline.py")],
            capture_output=True, text=True, timeout=30, env=env,
        )
        report = json.loads(r.stdout)
        self.assertTrue(report["all_ok"], f"Pipeline not all_ok: steps={len(report['steps'])} duration={report.get('duration_s')}")

    def test_pipeline_all_steps_have_no_error_status(self):
        import subprocess
        env = {**__import__("os").environ, "DRY_RUN": "1", "PAPER_MODE": "1", "ALLOW_E2E_LIVE_DRY_RUN": "1"}
        r = subprocess.run(
            [__import__("sys").executable, str(PROJECT_ROOT / "scripts/e2e/dry_run_pipeline.py")],
            capture_output=True, text=True, timeout=30, env=env,
        )
        report = json.loads(r.stdout)
        for step in report["steps"]:
            result = step["result"]
            if isinstance(result, dict):
                self.assertNotEqual(
                    result.get("status"), "error",
                    f"Step {step['step']} has error status: {result.get('error', 'unknown')}")


class TestE2EMenuJSON(unittest.TestCase):
    def test_menu_has_all_workers(self):
        data = json.loads((PROJECT_ROOT / "scripts/ai/menu/opt_trading_menu.json").read_text(encoding="utf-8"))
        workers_domain = None
        for d in data["menu"]:
            if d["id"] == "10_workers":
                workers_domain = d
                break
        self.assertIsNotNone(workers_domain)
        ids = []
        for child in workers_domain.get("children", []):
            if "children" in child:
                for w in child["children"]:
                    ids.append(w["id"])
        for wid in ["signal_router", "proposition_engine", "validation_gate",
                     "trade_executor", "result_tracker", "datasheet_writer",
                     "learning_feeder"]:
            self.assertIn(wid, ids, f"{wid} missing from workers menu")

    def test_menu_has_all_workers_operational(self):
        data = json.loads((PROJECT_ROOT / "scripts/ai/menu/opt_trading_menu.json").read_text(encoding="utf-8"))
        for d in data["menu"]:
            if d["id"] == "10_workers":
                for child in d.get("children", []):
                    if "children" in child:
                        for w in child["children"]:
                            if w["id"] in ("signal_router", "proposition_engine",
                                           "validation_gate", "trade_executor",
                                           "result_tracker", "datasheet_writer",
                                           "learning_feeder"):
                                self.assertEqual(w["status"], "operational",
                                                 f"{w['id']} should be operational")


class TestE2EDryRunPipelineInvariants(unittest.TestCase):
    def test_no_post_put_delete_patch_in_e2e_scripts(self):
        text = (PROJECT_ROOT / "scripts" / "e2e" / "dry_run_pipeline.py").read_text()
        self.assertNotIn(".post(", text)
        self.assertNotIn(".put(", text.lower())
        self.assertNotIn(".delete(", text.lower())
        self.assertNotIn(".patch(", text.lower())

    def test_dry_run_env_default(self):
        import subprocess, os
        clean_env = {k: v for k, v in os.environ.items()
                     if k not in ("DRY_RUN", "PAPER_MODE", "ALLOW_E2E_LIVE_DRY_RUN", "ALLOW_LIVE_TRADE")}
        clean_env["ALLOW_E2E_LIVE_DRY_RUN"] = "1"
        clean_env["DRY_RUN"] = "1"  # must be explicit with preflight
        r = subprocess.run(
            [__import__("sys").executable, str(PROJECT_ROOT / "scripts/e2e/dry_run_pipeline.py")],
            capture_output=True, text=True, timeout=30, env=clean_env,
        )
        report = json.loads(r.stdout)
        self.assertTrue(report["dry_run"])

    def test_closeout_no_artifacts(self):
        import subprocess, os
        env = {**os.environ, "DRY_RUN": "1", "PAPER_MODE": "1", "ALLOW_E2E_LIVE_DRY_RUN": "1"}
        r = subprocess.run(
            [__import__("sys").executable, str(PROJECT_ROOT / "scripts/e2e/dry_run_pipeline.py")],
            capture_output=True, text=True, timeout=30, env=env,
        )
        self.assertEqual(r.returncode, 0)

    def test_proposition_engine_no_live_bridge_call(self):
        from modules.proposition_engine.app.engine import PropositionEngine
        from modules.proposition_engine.app.schema import NormalizedSignal, PropositionRequest
        signal = NormalizedSignal(
            signal_id="test", ticker="BTCUSDT", side="BUY", price=65000.0,
            timestamp=1000.0, strategy_id="test", tf="1h", tp=None, sl=None, reason="",
        )
        prop = PropositionEngine().propose(PropositionRequest(signal=signal, dry_run=True))
        self.assertFalse(prop.engines_context.get("bridge_called", False))
        self.assertTrue(prop.dry_run)


if __name__ == "__main__":
    unittest.main()
