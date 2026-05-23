import sys
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.derivatives_collector.app.market_metrics_v1 import (
    MarketMetricsV1,
    ProviderCoverage,
    MetricsPayload,
    Refs,
)

REFS = Refs(
    primary_output="data/derivatives/derivatives_20260523_000000.json",
    meta_output="data/derivatives/derivatives_20260523_000000.meta.json",
    latest="data/derivatives/latest.json",
    status="data/derivatives/status.json",
)


def _bitget_partial() -> MarketMetricsV1:
    return MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="derivatives_collector",
        provider_id="bitget",
        symbol="BTCUSDT",
        metrics_ts="2026-05-23T00:00:00Z",
        freshness_state="fresh",
        provider_coverage=ProviderCoverage(
            status="partial",
            collectable_metrics=["open_interest", "funding_rate", "volume_futures"],
            missing_metrics=["long_short_ratio", "liquidations_long", "liquidations_short"],
        ),
        metrics=MetricsPayload(
            open_interest=18234.56,
            funding_rate=0.0001,
            volume_futures=67890123.45,
        ),
        refs=REFS,
        warnings=["provider missing metrics are explicit and not synthesized"],
    )


def _binance_deriv_partial() -> MarketMetricsV1:
    return MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="derivatives_collector",
        provider_id="binance_derivatives",
        symbol="BTCUSDT",
        metrics_ts="2026-05-23T00:00:00Z",
        freshness_state="fresh",
        provider_coverage=ProviderCoverage(
            status="partial",
            collectable_metrics=["open_interest", "funding_rate", "volume_futures", "long_short_ratio"],
            missing_metrics=["liquidations_long", "liquidations_short"],
        ),
        metrics=MetricsPayload(
            open_interest=72145.89,
            funding_rate=0.000125,
            volume_futures=4890123456.78,
            long_short_ratio=1.8234,
        ),
        refs=REFS,
        warnings=["liquidations not available from binance_derivatives adapter"],
    )


def _coinglass_not_proven() -> MarketMetricsV1:
    return MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="derivatives_collector",
        provider_id="coinglass",
        symbol="BTCUSDT",
        metrics_ts="2026-05-23T00:00:00Z",
        freshness_state="unknown",
        provider_coverage=ProviderCoverage(
            status="not_proven_runtime_adapter",
            collectable_metrics=[],
            missing_metrics=[
                "open_interest", "funding_rate", "volume_futures",
                "long_short_ratio", "liquidations_long", "liquidations_short",
            ],
        ),
        metrics=MetricsPayload(),
        refs=REFS,
        warnings=["no adapter file found in repo"],
    )


class TestMarketMetricsV1Bitget(unittest.TestCase):
    # TC-BITGET-01
    def test_bitget_partial_valid(self):
        m = _bitget_partial()
        self.assertTrue(m.validate())
        self.assertEqual(m.provider_coverage.status, "partial")
        self.assertIn("open_interest", m.provider_coverage.collectable_metrics)
        self.assertIn("long_short_ratio", m.provider_coverage.missing_metrics)
        self.assertEqual(m.metrics.open_interest, 18234.56)
        self.assertIsNone(m.metrics.long_short_ratio)
        self.assertIsNone(m.metrics.liquidations_long)
        self.assertTrue(m.warnings)

    # TC-BITGET-01 serialisation
    def test_bitget_to_json_roundtrip(self):
        m = _bitget_partial()
        d = json.loads(m.to_json())
        self.assertEqual(d["contract_version"], "v1")
        self.assertEqual(d["input_class"], "market_metrics.v1")
        self.assertIsNone(d["metrics"]["long_short_ratio"])
        self.assertEqual(d["metrics"]["open_interest"], 18234.56)

    # TC-BITGET-02: long_short_ratio non-null but in missing_metrics → BLOCKED
    def test_bitget_missing_metric_not_null_rejected(self):
        m = _bitget_partial()
        m.metrics.long_short_ratio = 1.5
        with self.assertRaises(ValueError) as ctx:
            m.validate()
        self.assertIn("long_short_ratio", str(ctx.exception))
        self.assertIn("missing_metrics", str(ctx.exception))

    # TC-BITGET-03: funding_rate absent from collectable but non-null → BLOCKED
    def test_bitget_collectable_missing_value_rejected(self):
        m = _bitget_partial()
        m.provider_coverage.collectable_metrics = ["open_interest", "volume_futures"]
        with self.assertRaises(ValueError) as ctx:
            m.validate()
        self.assertIn("funding_rate", str(ctx.exception))
        self.assertIn("collectable_metrics", str(ctx.exception))


class TestMarketMetricsV1BinanceDerivatives(unittest.TestCase):
    # TC-BINANCE-DERIV-01
    def test_binance_deriv_partial_with_lsr(self):
        m = _binance_deriv_partial()
        self.assertTrue(m.validate())
        self.assertIn("long_short_ratio", m.provider_coverage.collectable_metrics)
        self.assertEqual(m.metrics.long_short_ratio, 1.8234)
        self.assertIn("liquidations_long", m.provider_coverage.missing_metrics)

    # TC-BINANCE-DERIV-02: liquidations always null
    def test_binance_deriv_liquidations_null(self):
        m = _binance_deriv_partial()
        self.assertIsNone(m.metrics.liquidations_long)
        self.assertIsNone(m.metrics.liquidations_short)
        m.validate()


class TestMarketMetricsV1Coinglass(unittest.TestCase):
    # TC-COINGLASS-01
    def test_coinglass_not_proven_all_null(self):
        m = _coinglass_not_proven()
        self.assertTrue(m.validate())
        self.assertEqual(m.provider_coverage.status, "not_proven_runtime_adapter")
        self.assertEqual(m.provider_coverage.collectable_metrics, [])
        self.assertIsNone(m.metrics.open_interest)
        self.assertIsNone(m.metrics.liquidations_long)

    # TC-COINGLASS-02: liquidations non-null without proven adapter → BLOCKED
    def test_coinglass_fabricated_liquidations_rejected(self):
        m = _coinglass_not_proven()
        m.metrics.liquidations_long = 123.0
        with self.assertRaises(ValueError) as ctx:
            m.validate()
        self.assertIn("not_proven_runtime_adapter", str(ctx.exception))
        self.assertIn("liquidations_long", str(ctx.exception))

    def test_coinglass_with_collectable_metrics_rejected(self):
        m = _coinglass_not_proven()
        m.provider_coverage.collectable_metrics = ["open_interest"]
        with self.assertRaises(ValueError) as ctx:
            m.validate()
        self.assertIn("collectable_metrics", str(ctx.exception))


class TestMarketMetricsV1Invariants(unittest.TestCase):
    # TC-INVARIANT-01: 0 is a valid real value, not null
    def test_zero_is_valid_value(self):
        m = _bitget_partial()
        m.metrics.open_interest = 0.0
        self.assertTrue(m.validate())

    # TC-INVARIANT-02: status=partial with empty missing_metrics → BLOCKED
    def test_partial_with_empty_missing_metrics_rejected(self):
        m = _bitget_partial()
        m.provider_coverage.missing_metrics = []
        with self.assertRaises(ValueError) as ctx:
            m.validate()
        self.assertIn("missing_metrics is empty", str(ctx.exception))

    # TC-INVARIANT-03: freshness_state out of enum → BLOCKED
    def test_invalid_freshness_state_rejected(self):
        m = _bitget_partial()
        m.freshness_state = "expired"
        with self.assertRaises(ValueError) as ctx:
            m.validate()
        self.assertIn("freshness_state", str(ctx.exception))

    def test_invalid_coverage_status_rejected(self):
        m = _bitget_partial()
        m.provider_coverage.status = "unknown_status"
        with self.assertRaises(ValueError) as ctx:
            m.validate()
        self.assertIn("provider_coverage.status", str(ctx.exception))

    def test_wrong_contract_version_rejected(self):
        m = _bitget_partial()
        m.contract_version = "v2"
        with self.assertRaises(ValueError) as ctx:
            m.validate()
        self.assertIn("contract_version", str(ctx.exception))

    def test_wrong_input_class_rejected(self):
        m = _bitget_partial()
        m.input_class = "something_else"
        with self.assertRaises(ValueError) as ctx:
            m.validate()
        self.assertIn("input_class", str(ctx.exception))

    def test_stale_freshness_valid(self):
        m = _bitget_partial()
        m.freshness_state = "stale"
        self.assertTrue(m.validate())

    def test_unknown_freshness_valid(self):
        m = _coinglass_not_proven()
        self.assertTrue(m.validate())


if __name__ == "__main__":
    unittest.main()
