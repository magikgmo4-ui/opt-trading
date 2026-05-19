import json
import time
import unittest
from unittest.mock import MagicMock, patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.proposition_engine.app.schema import (
    NormalizedSignal, PropositionRequest, Proposition,
    PropositionError, EngineError, BridgeCallError,
)
from modules.proposition_engine.app.engine import PropositionEngine, _parse_proposition
from modules.proposition_engine.app.builder_prompt import compose_prompt
from modules.proposition_engine.app.engines import query_engines


def _signal(side="BUY", ticker="BTCUSDT", price=65000.0):
    return NormalizedSignal(
        signal_id="test-sig-001",
        ticker=ticker,
        side=side,
        price=price,
        timestamp=time.time(),
        strategy_id="test_v1",
        tf="1h",
    )


class TestSchema(unittest.TestCase):
    def test_normalized_signal_from_dict(self):
        d = {"signal_id": "x", "ticker": "ETHUSDT", "side": "SELL", "price": "3000",
             "timestamp": "1700000000", "strategy_id": "s1", "tf": "4h"}
        sig = NormalizedSignal.from_dict(d)
        self.assertEqual(sig.ticker, "ETHUSDT")
        self.assertEqual(sig.price, 3000.0)
        self.assertIsNone(sig.sl)

    def test_proposition_to_dict(self):
        prop = Proposition(
            request_id="r1", signal_id="s1", action="BUY", size_pct=0.1,
            entry=65000.0, sl=64000.0, tp=67000.0, confidence=0.8, rationale="test",
        )
        d = prop.to_dict()
        self.assertEqual(d["action"], "BUY")
        self.assertEqual(d["status"], "ok")
        self.assertIsNone(d["error"])

    def test_exception_classes(self):
        self.assertTrue(issubclass(EngineError, PropositionError))
        self.assertTrue(issubclass(BridgeCallError, PropositionError))


class TestParseProposition(unittest.TestCase):
    def test_valid_json(self):
        text = '{"action": "BUY", "size_pct": 0.1, "entry": 65000, "sl": null, "tp": 67000, "confidence": 0.75, "rationale": "strong signal"}'
        r = _parse_proposition(text, 65000.0)
        self.assertEqual(r["action"], "BUY")
        self.assertAlmostEqual(r["confidence"], 0.75)
        self.assertIsNone(r["sl"])

    def test_json_embedded_in_text(self):
        text = 'Some preamble. {"action": "SELL", "size_pct": 0.05, "entry": 3000, "sl": null, "tp": null, "confidence": 0.6, "rationale": "ok"} trailing text'
        r = _parse_proposition(text, 3000.0)
        self.assertEqual(r["action"], "SELL")

    def test_unparseable_returns_hold(self):
        r = _parse_proposition("not json at all", 65000.0)
        self.assertEqual(r["action"], "HOLD")
        self.assertEqual(r["confidence"], 0.0)

    def test_empty_text_returns_hold(self):
        r = _parse_proposition("", 65000.0)
        self.assertEqual(r["action"], "HOLD")


class TestBuilderPrompt(unittest.TestCase):
    def test_prompt_contains_signal_info(self):
        sig = _signal()
        ctx = {"decision": {"decision": "GO_LONG", "confidence": 0.85, "rationale": "strong"},
               "ranker": {"opportunity_score": 0.71, "priority": "HIGH", "setup_bias": "LONG"},
               "probability": {"probability_long": 0.72, "probability_short": 0.28, "confidence": 0.45}}
        prompt = compose_prompt(sig, ctx)
        self.assertIn("BTCUSDT", prompt)
        self.assertIn("BUY", prompt)
        self.assertIn("GO_LONG", prompt)
        self.assertIn("0.71", prompt)
        self.assertIn("JSON", prompt)

    def test_prompt_includes_sl_tp_when_present(self):
        sig = _signal()
        sig.sl = 64000.0
        sig.tp = 67000.0
        ctx = {}
        prompt = compose_prompt(sig, ctx)
        self.assertIn("64000.0", prompt)
        self.assertIn("67000.0", prompt)


class TestEnginesQuery(unittest.TestCase):
    def test_query_engines_buy_returns_dict(self):
        sig = _signal("BUY")
        ctx = query_engines(sig)
        self.assertIn("probability", ctx)
        self.assertIn("ranker", ctx)
        self.assertIn("decision", ctx)

    def test_query_engines_sell_returns_dict(self):
        sig = _signal("SELL")
        ctx = query_engines(sig)
        self.assertIn("probability", ctx)


class TestPropositionEngineDryRun(unittest.TestCase):
    def test_dry_run_no_bridge(self):
        eng = PropositionEngine()
        req = PropositionRequest(signal=_signal(), dry_run=True)
        prop = eng.propose(req)
        self.assertTrue(prop.dry_run)
        self.assertEqual(prop.status, "ok")
        self.assertEqual(prop.action, "HOLD")
        self.assertIsNotNone(prop.request_id)
        self.assertEqual(prop.signal_id, "test-sig-001")

    def test_dry_run_preserves_price(self):
        sig = _signal(price=70000.0)
        req = PropositionRequest(signal=sig, dry_run=True)
        eng = PropositionEngine()
        prop = eng.propose(req)
        self.assertEqual(prop.entry, 70000.0)

    def test_request_id_auto_generated(self):
        req = PropositionRequest(signal=_signal(), dry_run=True)
        eng = PropositionEngine()
        prop = eng.propose(req)
        self.assertNotEqual(prop.request_id, "")

    def test_dry_run_includes_engines_context(self):
        req = PropositionRequest(signal=_signal(), dry_run=True)
        eng = PropositionEngine()
        prop = eng.propose(req)
        self.assertIsInstance(prop.engines_context, dict)
        self.assertIn("decision", prop.engines_context)


class TestPropositionEngineMockedBridge(unittest.TestCase):
    def _mock_bridge_resp(self, content):
        resp = MagicMock()
        resp.status = "ok"
        resp.content = content
        resp.error = None
        return resp

    @patch("modules.proposition_engine.app.engine.OperatorBridge")
    def test_live_parse_buy_response(self, MockBridge):
        instance = MockBridge.return_value
        instance.send.return_value = self._mock_bridge_resp(
            '{"action": "BUY", "size_pct": 0.1, "entry": 65000, "sl": 64000, "tp": 67000, "confidence": 0.8, "rationale": "signal fort"}'
        )
        eng = PropositionEngine()
        req = PropositionRequest(signal=_signal(), dry_run=False)
        prop = eng.propose(req)
        self.assertEqual(prop.action, "BUY")
        self.assertAlmostEqual(prop.confidence, 0.8)
        self.assertEqual(prop.status, "ok")

    @patch("modules.proposition_engine.app.engine.OperatorBridge")
    def test_live_bridge_error_returns_hold(self, MockBridge):
        resp = MagicMock()
        resp.status = "error"
        resp.error = "gateway_unreachable"
        resp.content = ""
        MockBridge.return_value.send.return_value = resp
        eng = PropositionEngine()
        req = PropositionRequest(signal=_signal(), dry_run=False)
        prop = eng.propose(req)
        self.assertEqual(prop.action, "HOLD")
        self.assertEqual(prop.status, "error")

    @patch("modules.proposition_engine.app.engine.OperatorBridge")
    def test_live_unparseable_response_graceful(self, MockBridge):
        instance = MockBridge.return_value
        instance.send.return_value = self._mock_bridge_resp("Je ne sais pas quoi répondre.")
        eng = PropositionEngine()
        req = PropositionRequest(signal=_signal(), dry_run=False)
        prop = eng.propose(req)
        self.assertEqual(prop.action, "HOLD")
        self.assertEqual(prop.status, "ok")


if __name__ == "__main__":
    unittest.main()
