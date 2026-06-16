"""
Tests for executive_intelligence models + JSON schemas — PR1.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import jsonschema

from modules.executive_intelligence.models import (
    CANONICAL_BRIEFING,
    CANONICAL_EXECUTIVE_STATE,
    CANONICAL_REGIME,
    AssetInfluence,
    DetectedChange,
    ExecutiveBriefing,
    ExecutiveState,
    LeaderBoardEntry,
    MarketRegime,
    RegimeEvidence,
    TopOpportunity,
    TopRisk,
)

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"


# ── Market Regime ──────────────────────────────────────────────────────────

class TestMarketRegime(unittest.TestCase):
    def test_default_values(self):
        m = MarketRegime(regime="risk_on", confidence=80)
        self.assertEqual(m.regime, "risk_on")
        self.assertEqual(m.confidence, 80)
        self.assertEqual(m.contract, "market_regime.v1")
        self.assertIsInstance(m.evidence, RegimeEvidence)

    def test_confidence_bounds(self):
        m = MarketRegime(regime="risk_on", confidence=0)
        self.assertEqual(m.confidence, 0)
        m2 = MarketRegime(regime="risk_on", confidence=100)
        self.assertEqual(m2.confidence, 100)

    def test_risk_score_bounds(self):
        m = MarketRegime(regime="risk_on", confidence=50, risk_score=100)
        self.assertEqual(m.risk_score, 100)

    def test_all_regimes_valid(self):
        regimes = ["risk_on", "risk_off", "expansion", "compression",
                   "distribution", "accumulation", "panic", "recovery", "unknown"]
        for r in regimes:
            m = MarketRegime(regime=r, confidence=50)
            self.assertEqual(m.regime, r)

    def test_canonical_valid(self):
        m = CANONICAL_REGIME
        self.assertEqual(m.regime, "risk_on")
        self.assertEqual(m.confidence, 75)
        self.assertGreater(len(m.narrative), 0)

    def test_serialization_alias(self):
        m = CANONICAL_REGIME
        d = m.model_dump(by_alias=True)
        self.assertIn("schema", d)
        self.assertEqual(d["schema"], "market_regime.v1")

    def test_schema_validation(self):
        schema = json.loads((SCHEMA_DIR / "market_regime_v1.json").read_text())
        payload = CANONICAL_REGIME.model_dump(by_alias=True, mode="json")
        jsonschema.validate(payload, schema, cls=jsonschema.Draft202012Validator)

    def test_rejects_invalid_regime(self):
        with self.assertRaises(Exception):
            MarketRegime(regime="invalid", confidence=50)  # type: ignore


# ── Cross-Asset Models ─────────────────────────────────────────────────────

class TestAssetInfluence(unittest.TestCase):
    def test_valid(self):
        a = AssetInfluence(source="BTC", target="ETH", correlation=0.85, influence_score=80)
        self.assertEqual(a.source, "BTC")
        self.assertEqual(a.target, "ETH")

    def test_correlation_bounds(self):
        AssetInfluence(source="A", target="B", correlation=1.0)
        AssetInfluence(source="A", target="B", correlation=-1.0)
        with self.assertRaises(Exception):
            AssetInfluence(source="A", target="B", correlation=1.5)


class TestLeaderBoardEntry(unittest.TestCase):
    def test_valid(self):
        lb = LeaderBoardEntry(symbol="BTC", rank=1, direction="bullish", confidence=75, reliability=82, momentum_score=70, is_leader=True)
        self.assertTrue(lb.is_leader)
        self.assertEqual(lb.rank, 1)
        lb2 = LeaderBoardEntry(symbol="XRP", rank=9, direction="bearish", confidence=30, reliability=20, momentum_score=10, is_laggard=True)
        self.assertTrue(lb2.is_laggard)


class TestDetectedChange(unittest.TestCase):
    def test_valid(self):
        c = DetectedChange(
            field="direction",
            previous="neutral",
            current="bullish",
            magnitude="major",
            description="Le biais BTC est passé de neutre à haussier.",
        )
        self.assertEqual(c.field, "direction")
        self.assertEqual(c.magnitude, "major")


class TestTopOpportunity(unittest.TestCase):
    def test_valid(self):
        t = TopOpportunity(symbol="BTC", direction="bullish", confidence=75, reliability=82, score=78, reason="Contexte favorable")
        self.assertEqual(t.symbol, "BTC")
        self.assertGreaterEqual(t.score, 0)
        self.assertLessEqual(t.score, 100)


class TestTopRisk(unittest.TestCase):
    def test_valid(self):
        t = TopRisk(symbol="market", category="macro", severity="high", score=65, description="Dollar fort")
        self.assertEqual(t.severity, "high")


# ── Executive State ────────────────────────────────────────────────────────

class TestExecutiveState(unittest.TestCase):
    def test_canonical_valid(self):
        state = CANONICAL_EXECUTIVE_STATE
        self.assertEqual(state.contract, "executive_state.v1")
        self.assertIsNotNone(state.regime)
        self.assertGreater(len(state.leaders), 0)
        self.assertGreater(len(state.influences), 0)
        self.assertGreater(len(state.changes), 0)
        self.assertGreaterEqual(state.overall_confidence, 0)
        self.assertLessEqual(state.overall_confidence, 100)

    def test_schema_validation(self):
        schema = json.loads((SCHEMA_DIR / "executive_state_v1.json").read_text())
        payload = CANONICAL_EXECUTIVE_STATE.model_dump(by_alias=True, mode="json")
        jsonschema.validate(payload, schema, cls=jsonschema.Draft202012Validator)

    def test_minimal_valid(self):
        state = ExecutiveState(snapshot_id="snap_01")
        self.assertEqual(state.overall_confidence, 50)
        self.assertEqual(state.source_count, 0)

    def test_serialization(self):
        d = CANONICAL_EXECUTIVE_STATE.model_dump(by_alias=True)
        self.assertIn("schema", d)
        self.assertIn("leaders", d)


# ── Executive Briefing ─────────────────────────────────────────────────────

class TestExecutiveBriefing(unittest.TestCase):
    def test_canonical_valid(self):
        brief = CANONICAL_BRIEFING
        self.assertEqual(brief.contract, "executive_briefing.v1")
        self.assertGreater(len(brief.summary), 0)
        self.assertGreater(len(brief.leaders), 0)
        self.assertGreater(len(brief.voice_one_liner), 0)
        self.assertGreater(len(brief.voice_briefing), 0)

    def test_schema_validation(self):
        schema = json.loads((SCHEMA_DIR / "executive_briefing_v1.json").read_text())
        payload = CANONICAL_BRIEFING.model_dump(by_alias=True, mode="json")
        jsonschema.validate(payload, schema, cls=jsonschema.Draft202012Validator)

    def test_voice_one_liner_under_300(self):
        brief = CANONICAL_BRIEFING
        self.assertLessEqual(len(brief.voice_one_liner), 300)

    def test_voice_briefing_under_600(self):
        brief = CANONICAL_BRIEFING
        self.assertLessEqual(len(brief.voice_briefing), 600)

    def test_minimal_valid(self):
        brief = ExecutiveBriefing(briefing_id="b1", market_regime="unknown")
        self.assertEqual(brief.overall_confidence, 50)
        self.assertEqual(brief.leaders, [])

    def test_serialization(self):
        d = CANONICAL_BRIEFING.model_dump(by_alias=True)
        self.assertIn("schema", d)
        self.assertIn("leaders", d)


# ── Evidence ────────────────────────────────────────────────────────────────

class TestRegimeEvidence(unittest.TestCase):
    def test_defaults(self):
        e = RegimeEvidence()
        self.assertEqual(e.dxy_trend, "unknown")

    def test_fear_greed_bounds(self):
        e = RegimeEvidence(fear_greed=0)
        self.assertEqual(e.fear_greed, 0)
        e2 = RegimeEvidence(fear_greed=100)
        self.assertEqual(e2.fear_greed, 100)
        with self.assertRaises(Exception):
            RegimeEvidence(fear_greed=101)


# ── JSON Schema structural validity ────────────────────────────────────────

class TestJSONSchemasValid(unittest.TestCase):
    def test_executive_state_schema_self_validates(self):
        path = SCHEMA_DIR / "executive_state_v1.json"
        schema = json.loads(path.read_text())
        jsonschema.Draft202012Validator.check_schema(schema)

    def test_market_regime_schema_self_validates(self):
        path = SCHEMA_DIR / "market_regime_v1.json"
        schema = json.loads(path.read_text())
        jsonschema.Draft202012Validator.check_schema(schema)

    def test_executive_briefing_schema_self_validates(self):
        path = SCHEMA_DIR / "executive_briefing_v1.json"
        schema = json.loads(path.read_text())
        jsonschema.Draft202012Validator.check_schema(schema)


if __name__ == "__main__":
    unittest.main()
