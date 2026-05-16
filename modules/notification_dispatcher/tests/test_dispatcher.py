import sys
import unittest
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))

from app.events import PipelineEvent, format_message, ALL_EVENT_TYPES
from app.dispatcher import NotificationDispatcher


class TestEvents(unittest.TestCase):
    def test_all_event_types_have_templates(self):
        from app.events import TEMPLATES
        for et in ALL_EVENT_TYPES:
            self.assertIn(et, TEMPLATES, f"missing template for {et}")

    def test_validate_known_type(self):
        for et in ALL_EVENT_TYPES:
            e = PipelineEvent(event_type=et)  # type: ignore[arg-type]
            e.validate()  # must not raise

    def test_validate_unknown_type_raises(self):
        e = PipelineEvent(event_type="unknown_event")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            e.validate()

    def test_format_signal_received(self):
        e = PipelineEvent(
            event_type="signal_received",
            payload={"ticker": "BTCUSDT", "side": "BUY", "price": 65000, "tf": "1h", "strategy_id": "v1"},
        )
        msg = format_message(e)
        self.assertIn("BTCUSDT", msg)
        self.assertIn("BUY", msg)
        self.assertIn("Signal reçu", msg)

    def test_format_pipeline_error(self):
        e = PipelineEvent(
            event_type="pipeline_error",
            payload={"step": "validation_gate", "error": "risk limit exceeded"},
        )
        msg = format_message(e)
        self.assertIn("Erreur pipeline", msg)
        self.assertIn("validation_gate", msg)

    def test_format_fallback_missing_keys(self):
        e = PipelineEvent(event_type="trade_executed", payload={"ticker": "ETH"})
        msg = format_message(e)
        self.assertIn("ETH", msg)

    def test_format_pipeline_info(self):
        e = PipelineEvent(event_type="pipeline_info", payload={"message": "system starting"})
        msg = format_message(e)
        self.assertIn("system starting", msg)


class TestDispatcherDryRun(unittest.TestCase):
    def _dispatch(self, event_type: str, payload: dict = None) -> dict:
        e = PipelineEvent(event_type=event_type, payload=payload or {})  # type: ignore[arg-type]
        return NotificationDispatcher().dispatch(e, dry_run=True)

    def test_dry_run_ok(self):
        result = self._dispatch("signal_received", {"ticker": "BTC", "side": "BUY", "price": 1, "tf": "1h", "strategy_id": "t"})
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["event_type"], "signal_received")

    def test_dry_run_contains_message(self):
        result = self._dispatch("pipeline_info", {"message": "hello"})
        self.assertIn("message", result)
        self.assertIn("hello", result["message"])

    def test_all_event_types_dispatch_dry(self):
        for et in ALL_EVENT_TYPES:
            result = self._dispatch(et)
            self.assertTrue(result["ok"], f"dry run failed for {et}")

    def test_unknown_event_type_raises_on_dispatch(self):
        e = PipelineEvent(event_type="execute_trade")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            NotificationDispatcher().dispatch(e, dry_run=True)


if __name__ == "__main__":
    unittest.main()
