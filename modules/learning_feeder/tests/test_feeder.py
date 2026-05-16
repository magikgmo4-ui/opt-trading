"""Learning feeder tests — python3 -m unittest"""
from __future__ import annotations
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.proposition_engine.app.schema import Proposition
from modules.result_tracker.app.schema import TradeRecord
from modules.learning_feeder.app.schema import FeedRequest, FeedResult
from modules.learning_feeder.app.composer import compose_feedback
from modules.learning_feeder.app.feeder import LearningFeeder


def _prop(**kw) -> Proposition:
    defaults = dict(
        request_id="req-001", signal_id="sig-001",
        action="BUY", size_pct=0.5,
        entry=65000.0, sl=63000.0, tp=70000.0,
        confidence=0.85, rationale="strong breakout above resistance",
        engines_context={}, duration_ms=50,
        dry_run=True, status="ok", error=None,
    )
    defaults.update(kw)
    return Proposition(**defaults)


def _record(**kw) -> TradeRecord:
    defaults = dict(
        trade_id="paper_BTCUSDT_abc123", request_id="req-001", signal_id="sig-001",
        ticker="BTCUSDT", action="BUY",
        entry_price=65000.0, close_price=67000.0,
        fill_qty=0.5, size_pct=0.5,
        sl=63000.0, tp=70000.0,
        gross_pnl=1000.0, net_pnl=960.4, fees=39.6,
        duration_s=120.0, outcome="win",
        opened_at="2026-05-16T10:00:00+00:00",
        closed_at="2026-05-16T10:02:00+00:00",
        dry_run=True, meta={},
    )
    defaults.update(kw)
    return TradeRecord(**defaults)


def _req(dry_run=True, **kw) -> FeedRequest:
    defaults = dict(
        signal_id="sig-001",
        proposition=_prop(),
        trade_record=_record(),
        dry_run=dry_run,
    )
    defaults.update(kw)
    return FeedRequest(**defaults)


def _mock_bridge(status="ok"):
    bridge = MagicMock()
    resp = MagicMock()
    resp.status = status
    resp.error = None
    bridge.send.return_value = resp
    return bridge


def _feeder(bridge=None, bricks_dir=None) -> LearningFeeder:
    return LearningFeeder(bridge=bridge, bricks_dir=bricks_dir)


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------

class TestSchema(unittest.TestCase):

    def test_feed_request_defaults(self):
        req = _req()
        self.assertEqual(req.request_id, "")
        self.assertTrue(req.dry_run)
        self.assertEqual(req.bridge_timeout_s, 90)
        self.assertTrue(req.store_brick)

    def test_feed_result_defaults(self):
        r = FeedResult(
            request_id="r", signal_id="s",
            bridge_status="dry_run", brick_stored=False,
            brick_id="", summary="test",
        )
        self.assertEqual(r.duration_ms, 0)
        self.assertTrue(r.dry_run)
        self.assertEqual(r.meta, {})


# ---------------------------------------------------------------------------
# Composer tests
# ---------------------------------------------------------------------------

class TestComposer(unittest.TestCase):

    def test_contains_ticker(self):
        text = compose_feedback(_prop(), _record())
        self.assertIn("BTCUSDT", text)

    def test_contains_outcome(self):
        text = compose_feedback(_prop(), _record(outcome="win"))
        self.assertIn("WIN", text)

    def test_contains_pnl(self):
        text = compose_feedback(_prop(), _record(net_pnl=960.4))
        self.assertIn("960.4", text)

    def test_contains_rationale(self):
        text = compose_feedback(_prop(rationale="strong breakout above resistance"), _record())
        self.assertIn("strong breakout above resistance", text)

    def test_win_positive_feedback_text(self):
        text = compose_feedback(_prop(), _record(outcome="win"))
        self.assertIn("Positive reinforcement", text)

    def test_loss_negative_feedback_text(self):
        text = compose_feedback(_prop(), _record(outcome="loss"))
        self.assertIn("Negative feedback", text)

    def test_breakeven_neutral_text(self):
        text = compose_feedback(_prop(), _record(outcome="breakeven"))
        self.assertIn("Neutral", text)

    def test_contains_confidence(self):
        text = compose_feedback(_prop(confidence=0.85), _record())
        self.assertIn("0.85", text)

    def test_contains_action(self):
        text = compose_feedback(_prop(), _record(action="SELL"))
        self.assertIn("SELL", text)


# ---------------------------------------------------------------------------
# LearningFeeder dry_run tests
# ---------------------------------------------------------------------------

class TestFeederDryRun(unittest.TestCase):

    def test_dry_run_bridge_status(self):
        result = _feeder().feed(_req(dry_run=True))
        self.assertEqual(result.bridge_status, "dry_run")

    def test_dry_run_no_bridge_called(self):
        bridge = _mock_bridge()
        _feeder(bridge=bridge).feed(_req(dry_run=True))
        bridge.send.assert_not_called()

    def test_dry_run_brick_not_stored(self):
        result = _feeder().feed(_req(dry_run=True))
        self.assertFalse(result.brick_stored)
        self.assertEqual(result.brick_id, "")

    def test_dry_run_summary_populated(self):
        result = _feeder().feed(_req(dry_run=True))
        self.assertIn("BTCUSDT", result.summary)
        self.assertIn("WIN", result.summary)

    def test_dry_run_is_flagged(self):
        result = _feeder().feed(_req(dry_run=True))
        self.assertTrue(result.dry_run)

    def test_dry_run_duration_set(self):
        result = _feeder().feed(_req(dry_run=True))
        self.assertGreaterEqual(result.duration_ms, 0)

    def test_dry_run_auto_request_id(self):
        req = _req(dry_run=True)
        self.assertEqual(req.request_id, "")
        result = _feeder().feed(req)
        self.assertNotEqual(result.request_id, "")

    def test_dry_run_signal_id_passthrough(self):
        result = _feeder().feed(_req(dry_run=True, signal_id="sig-xyz"))
        self.assertEqual(result.signal_id, "sig-xyz")


# ---------------------------------------------------------------------------
# LearningFeeder live tests
# ---------------------------------------------------------------------------

class TestFeederLive(unittest.TestCase):

    def test_live_bridge_called(self):
        bridge = _mock_bridge("ok")
        with tempfile.TemporaryDirectory() as d:
            _feeder(bridge=bridge, bricks_dir=Path(d)).feed(_req(dry_run=False))
        bridge.send.assert_called_once()

    def test_live_bridge_status_ok(self):
        with tempfile.TemporaryDirectory() as d:
            result = _feeder(bridge=_mock_bridge("ok"), bricks_dir=Path(d)).feed(_req(dry_run=False))
        self.assertEqual(result.bridge_status, "ok")

    def test_live_brick_stored(self):
        with tempfile.TemporaryDirectory() as d:
            result = _feeder(bridge=_mock_bridge("ok"), bricks_dir=Path(d)).feed(_req(dry_run=False))
        self.assertTrue(result.brick_stored)

    def test_live_brick_id_non_empty(self):
        with tempfile.TemporaryDirectory() as d:
            result = _feeder(bridge=_mock_bridge("ok"), bricks_dir=Path(d)).feed(_req(dry_run=False))
        self.assertNotEqual(result.brick_id, "")

    def test_live_brick_file_exists(self):
        with tempfile.TemporaryDirectory() as d:
            result = _feeder(bridge=_mock_bridge("ok"), bricks_dir=Path(d)).feed(_req(dry_run=False))
            brick_files = list(Path(d).rglob("*.json"))
        self.assertEqual(len(brick_files), 1)

    def test_live_brick_json_parseable(self):
        with tempfile.TemporaryDirectory() as d:
            result = _feeder(bridge=_mock_bridge("ok"), bricks_dir=Path(d)).feed(_req(dry_run=False))
            brick_files = list(Path(d).rglob("*.json"))
            data = json.loads(brick_files[0].read_text())
        self.assertEqual(data["outcome"], "win")
        self.assertEqual(data["brick_id"], result.brick_id)

    def test_live_store_brick_false_skips_storage(self):
        with tempfile.TemporaryDirectory() as d:
            req = _req(dry_run=False, store_brick=False)
            result = _feeder(bridge=_mock_bridge("ok"), bricks_dir=Path(d)).feed(req)
            brick_files = list(Path(d).rglob("*.json"))
        self.assertFalse(result.brick_stored)
        self.assertEqual(len(brick_files), 0)

    def test_live_bridge_error_still_stores_brick(self):
        with tempfile.TemporaryDirectory() as d:
            result = _feeder(bridge=_mock_bridge("error"), bricks_dir=Path(d)).feed(_req(dry_run=False))
        self.assertEqual(result.bridge_status, "error")
        self.assertTrue(result.brick_stored)

    def test_live_not_flagged_dry_run(self):
        with tempfile.TemporaryDirectory() as d:
            result = _feeder(bridge=_mock_bridge("ok"), bricks_dir=Path(d)).feed(_req(dry_run=False))
        self.assertFalse(result.dry_run)

    def test_live_meta_has_bridge_response(self):
        with tempfile.TemporaryDirectory() as d:
            result = _feeder(bridge=_mock_bridge("ok"), bricks_dir=Path(d)).feed(_req(dry_run=False))
        self.assertIn("bridge_response", result.meta)


if __name__ == "__main__":
    unittest.main(verbosity=2)
