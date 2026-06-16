"""
Tests for market_thesis.models — Pydantic v2 model validation.

Covers:
- Model instantiation with valid data
- Model rejects invalid data (probabilities, confidence bounds)
- ActionPlan readiness locked to monitor_only
- Canonical BTC fixture is valid
- Serialization round-trip
"""

from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone

from modules.market_thesis.models import (
    ActionPlan,
    CANONICAL_BTC_THESIS,
    FreshnessStatus,
    FlowSection,
    MarketContext,
    MarketThesis,
    NewsSection,
    ProbabilitySet,
    RiskItem,
    SourceRef,
    TechnicalSection,
    ThesisMetadata,
)


class TestThesisMetadata(unittest.TestCase):
    """ThesisMetadata model tests."""

    def test_minimal_valid(self):
        m = ThesisMetadata(thesis_id="thesis_BTC_20260615T120000Z")
        self.assertEqual(m.contract, "market_thesis.v1")
        self.assertEqual(m.ttl_seconds, 300)
        self.assertEqual(m.version, "1.0.0")
        self.assertIsInstance(m.generated_at, datetime)

    def test_custom_ttl(self):
        m = ThesisMetadata(thesis_id="t1", ttl_seconds=600)
        self.assertEqual(m.ttl_seconds, 600)

    def test_serialization(self):
        m = ThesisMetadata(
            thesis_id="thesis_BTC_20260615T120000Z",
            generated_at=datetime(2026, 6, 15, 12, 0, 0, tzinfo=timezone.utc),
        )
        d = m.model_dump(by_alias=True)
        self.assertEqual(d["thesis_id"], "thesis_BTC_20260615T120000Z")
        self.assertEqual(d["schema"], "market_thesis.v1")
        self.assertIn("generated_at", d)


class TestMarketContext(unittest.TestCase):
    """MarketContext model tests."""

    def test_defaults(self):
        ctx = MarketContext()
        self.assertEqual(ctx.macro_regime, "unknown")
        self.assertEqual(ctx.market_phase, "unknown")
        self.assertEqual(ctx.narrative, "")

    def test_full(self):
        ctx = MarketContext(
            macro_regime="risk_on",
            dxy_trend="bearish",
            vix_state="low",
            spy_trend="bullish",
            market_phase="markup",
            narrative="Contexte favorable.",
        )
        d = ctx.model_dump()
        self.assertEqual(d["macro_regime"], "risk_on")
        self.assertEqual(d["narrative"], "Contexte favorable.")


class TestTechnicalSection(unittest.TestCase):
    """TechnicalSection model tests."""

    def test_defaults(self):
        t = TechnicalSection()
        self.assertEqual(t.htf_bias, "neutral")
        self.assertEqual(t.alignment, "neutral")
        self.assertEqual(t.key_support, [])
        self.assertIsNone(t.vwap)

    def test_with_levels(self):
        t = TechnicalSection(
            htf_bias="bullish",
            ltf_bias="bearish",
            alignment="divergent",
            key_support=[65000.0, 62000.0],
            key_resistance=[72000.0],
            vwap=66450.0,
            active_setups=["btc_vwap_reclaim"],
        )
        self.assertEqual(len(t.key_support), 2)
        self.assertEqual(t.vwap, 66450.0)


class TestFlowSection(unittest.TestCase):
    """FlowSection model tests."""

    def test_all_none_default(self):
        f = FlowSection()
        self.assertIsNone(f.open_interest)
        self.assertIsNone(f.funding_rate)
        self.assertIsNone(f.etf_flow)

    def test_with_data(self):
        f = FlowSection(
            open_interest=28_500_000_000.0,
            funding_rate=0.0035,
            long_short_ratio=1.8,
            liquidations_long=45_000_000.0,
            liquidations_short=12_000_000.0,
            etf_flow="inflow",
        )
        self.assertEqual(f.open_interest, 28_500_000_000.0)
        self.assertEqual(f.etf_flow, "inflow")


class TestNewsSection(unittest.TestCase):
    """NewsSection model tests."""

    def test_defaults(self):
        n = NewsSection()
        self.assertEqual(n.sentiment, "unknown")
        self.assertEqual(n.sentiment_score, 0.0)
        self.assertEqual(n.key_drivers, [])

    def test_sentiment_score_bounds_valid(self):
        n1 = NewsSection(sentiment_score=1.0)
        self.assertEqual(n1.sentiment_score, 1.0)
        n2 = NewsSection(sentiment_score=-1.0)
        self.assertEqual(n2.sentiment_score, -1.0)


class TestRiskItem(unittest.TestCase):
    """RiskItem model tests."""

    def test_valid(self):
        r = RiskItem(
            category="concentration",
            severity="high",
            description="Crowding long élevé.",
        )
        self.assertEqual(r.category, "concentration")
        self.assertEqual(r.severity, "high")


class TestProbabilitySet(unittest.TestCase):
    """ProbabilitySet model tests with invariant: bull + range + bear == 100."""

    def test_valid_exact_100(self):
        p = ProbabilitySet(bull=50, range=30, bear=20)
        d = p.model_dump()
        self.assertEqual(d["bull"], 50)
        self.assertEqual(d["range"], 30)
        self.assertEqual(d["bear"], 20)

    def test_valid_all_bull(self):
        p = ProbabilitySet(bull=100, range=0, bear=0)
        self.assertEqual(p.bull, 100)

    def test_valid_all_range(self):
        p = ProbabilitySet(bull=0, range=100, bear=0)
        self.assertEqual(p.range, 100)

    def test_rejects_invalid_total(self):
        with self.assertRaises(ValueError):
            ProbabilitySet(bull=60, range=30, bear=20)

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            ProbabilitySet(bull=-10, range=50, bear=60)

    def test_rejects_over_100_individual(self):
        with self.assertRaises(ValueError):
            ProbabilitySet(bull=110, range=-10, bear=0)

    def test_rejects_total_not_100_various(self):
        invalid_cases = [
            (33, 33, 33),   # 99
            (34, 33, 33),   # 100 → would pass, skip
            (0, 0, 0),      # 0
            (100, 1, 0),    # 101
        ]
        for bull, rng, bear in invalid_cases:
            if bull + rng + bear == 100:
                continue
            with self.assertRaises(ValueError, msg=f"bull={bull}, range={rng}, bear={bear}"):
                ProbabilitySet(bull=bull, range=rng, bear=bear)


class TestActionPlan(unittest.TestCase):
    """ActionPlan model tests — readiness locked to monitor_only."""

    def test_default_is_monitor_only(self):
        a = ActionPlan()
        self.assertEqual(a.readiness, "monitor_only")
        self.assertEqual(a.direction, "neutral")

    def test_with_direction(self):
        a = ActionPlan(
            direction="bullish",
            key_levels=["Entry: 66450", "Invalidation: 65000"],
            narrative="Attendre confirmation.",
            voice_one_liner="BTC haussier modéré.",
        )
        self.assertEqual(a.direction, "bullish")
        self.assertEqual(a.readiness, "monitor_only")

    def test_serialization(self):
        a = ActionPlan(
            direction="wait",
            voice_one_liner="BTC en attente.",
        )
        d = a.model_dump()
        self.assertEqual(d["readiness"], "monitor_only")
        self.assertEqual(d["direction"], "wait")


class TestSourceRef(unittest.TestCase):
    """SourceRef model tests."""

    def test_used(self):
        s = SourceRef(name="Binance spot", contract="market_metrics.v1", status="used", age_minutes=3.2)
        self.assertEqual(s.status, "used")
        self.assertEqual(s.age_minutes, 3.2)

    def test_missing_no_age(self):
        s = SourceRef(name="Coinglass", contract="vision_context.coinglass.v1", status="missing")
        self.assertIsNone(s.age_minutes)


class TestFreshnessStatus(unittest.TestCase):
    """FreshnessStatus model tests."""

    def test_valid(self):
        f = FreshnessStatus(overall="fresh", max_age_minutes=8.5, source_count=6, fresh_count=5)
        self.assertEqual(f.overall, "fresh")
        self.assertEqual(f.source_count, 6)

    def test_partial(self):
        f = FreshnessStatus(overall="partial", max_age_minutes=30.0, source_count=6, fresh_count=2)
        self.assertEqual(f.fresh_count, 2)


class TestMarketThesis(unittest.TestCase):
    """Top-level MarketThesis model tests."""

    def test_canonical_btc_valid(self):
        """The CANONICAL_BTC_THESIS fixture must be a valid MarketThesis."""
        thesis = CANONICAL_BTC_THESIS
        self.assertEqual(thesis.symbol, "BTC")
        self.assertEqual(thesis.metadata.contract, "market_thesis.v1")
        self.assertEqual(thesis.probabilities.bull + thesis.probabilities.range + thesis.probabilities.bear, 100)
        self.assertEqual(thesis.action.readiness, "monitor_only")
        self.assertGreaterEqual(thesis.confidence, 0)
        self.assertLessEqual(thesis.confidence, 100)

    def test_confidence_bounds_valid(self):
        thesis = MarketThesis(
            metadata=ThesisMetadata(thesis_id="t1"),
            symbol="ETH",
            probabilities=ProbabilitySet(bull=40, range=40, bear=20),
            freshness=FreshnessStatus(overall="fresh", max_age_minutes=0, source_count=1, fresh_count=1),
            confidence=0,
        )
        self.assertEqual(thesis.confidence, 0)
        thesis2 = MarketThesis(
            metadata=ThesisMetadata(thesis_id="t2"),
            symbol="ETH",
            probabilities=ProbabilitySet(bull=40, range=40, bear=20),
            freshness=FreshnessStatus(overall="fresh", max_age_minutes=0, source_count=1, fresh_count=1),
            confidence=100,
        )
        self.assertEqual(thesis2.confidence, 100)

    def test_confidence_rejects_out_of_bounds(self):
        base = dict(
            metadata=ThesisMetadata(thesis_id="t1"),
            symbol="ETH",
            probabilities=ProbabilitySet(bull=40, range=40, bear=20),
            freshness=FreshnessStatus(overall="fresh", max_age_minutes=0, source_count=1, fresh_count=1),
        )
        with self.assertRaises(ValueError):
            MarketThesis(**base, confidence=-1)
        with self.assertRaises(ValueError):
            MarketThesis(**base, confidence=101)

    def test_action_always_monitor_only(self):
        thesis = MarketThesis(
            metadata=ThesisMetadata(thesis_id="t1"),
            symbol="SOL",
            probabilities=ProbabilitySet(bull=33, range=34, bear=33),
            freshness=FreshnessStatus(overall="fresh", max_age_minutes=0, source_count=1, fresh_count=1),
            confidence=50,
        )
        self.assertEqual(thesis.action.readiness, "monitor_only")

    def test_minimal_valid_thesis(self):
        thesis = MarketThesis(
            metadata=ThesisMetadata(thesis_id="thesis_MIN_01"),
            symbol="XRP",
            probabilities=ProbabilitySet(bull=30, range=40, bear=30),
            freshness=FreshnessStatus(overall="partial", max_age_minutes=60, source_count=2, fresh_count=1),
            confidence=30,
        )
        self.assertEqual(thesis.symbol, "XRP")
        self.assertEqual(thesis.context.macro_regime, "unknown")
        self.assertEqual(thesis.risks, [])

    def test_full_serialization_roundtrip(self):
        d = CANONICAL_BTC_THESIS.model_dump()
        thesis2 = MarketThesis(**d)
        self.assertEqual(thesis2.symbol, "BTC")
        self.assertEqual(thesis2.confidence, 55)
        self.assertEqual(thesis2.probabilities.bull, 50)
        self.assertEqual(thesis2.probabilities.range, 30)
        self.assertEqual(thesis2.probabilities.bear, 20)
        self.assertEqual(thesis2.sources[0].name, "Binance spot")
        self.assertEqual(thesis2.risks[0].category, "concentration")

    def test_json_serialization(self):
        json_str = CANONICAL_BTC_THESIS.model_dump_json(by_alias=True)
        d = json.loads(json_str)
        self.assertEqual(d["symbol"], "BTC")
        self.assertEqual(d["metadata"]["schema"], "market_thesis.v1")
        self.assertEqual(d["action"]["readiness"], "monitor_only")

    def test_all_nine_symbols(self):
        symbols = ["BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU"]
        for sym in symbols:
            thesis = MarketThesis(
                metadata=ThesisMetadata(thesis_id=f"thesis_{sym}_01"),
                symbol=sym,
                probabilities=ProbabilitySet(bull=33, range=34, bear=33),
                freshness=FreshnessStatus(overall="fresh", max_age_minutes=0, source_count=1, fresh_count=1),
                confidence=50,
            )
            self.assertEqual(thesis.symbol, sym)
            self.assertEqual(thesis.action.readiness, "monitor_only")


if __name__ == "__main__":
    unittest.main()
