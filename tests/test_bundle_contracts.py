import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from modules.analysis_bundles.app.schema import (
    BundleOutput,
    BundleAnalysis,
    BundleInput,
    VALID_FRESHNESS_STATES,
    VALID_BIAS,
    VALID_REGIME,
    VALID_SQUEEZE,
    VALID_CONFIDENCE,
)
from modules.analysis_bundles.app.contract_validator import validate_bundle
from modules.analysis_bundles.app.btc_core_producer import produce_btc_core
from modules.analysis_bundles.app.macro_producer import produce_macro


def _make_valid_bundle(**overrides) -> dict:
    base = {
        "contract": "bundle.btc_core.v1",
        "bundle_id": "btc.core.v1",
        "produced_at": "2026-01-01T00:00:00Z",
        "freshness_state": "FRESH",
        "assets": ["BTC", "BTCUSDT"],
        "inputs": {
            "market_metrics": {
                "source": "market_metrics.v1",
                "freshness": "FRESH",
                "produced_at": "2026-01-01T00:00:00Z",
            },
        },
        "analysis": {
            "timeframe": "1H",
            "bias_short_term": "BULLISH",
            "bias_intraday": "NEUTRAL",
            "regime": "TRENDING",
            "squeeze_or_stress_level": "LOW",
            "invalidation": "BTC < 86000",
            "confidence": "MEDIUM",
        },
        "missing_inputs": [],
        "source_refs": ["/path/to/source.json"],
    }
    base.update(overrides)
    return base


class TestBundleOutput:
    def test_to_dict_includes_all_fields(self):
        b = BundleOutput(
            contract="bundle.test.v1",
            bundle_id="test.v1",
            produced_at="2026-01-01T00:00:00Z",
            freshness_state="FRESH",
            assets=["BTC"],
            inputs={},
            analysis={},
        )
        d = b.to_dict()
        assert d["contract"] == "bundle.test.v1"
        assert d["bundle_id"] == "test.v1"
        assert d["freshness_state"] == "FRESH"
        assert d["assets"] == ["BTC"]
        assert d["missing_inputs"] == []
        assert d["source_refs"] == []

    def test_missing_inputs_defaults_to_empty(self):
        b = BundleOutput(
            contract="bundle.test.v1",
            bundle_id="test.v1",
            produced_at="2026-01-01T00:00:00Z",
            freshness_state="FRESH",
            assets=[],
            inputs={},
            analysis={},
        )
        assert b.missing_inputs == []
        assert b.source_refs == []


class TestBundleInput:
    def test_to_dict_includes_produced_at_when_set(self):
        inp = BundleInput(source="mm.v1", freshness="FRESH", produced_at="2026-01-01T00:00:00Z")
        d = inp.to_dict()
        assert d["produced_at"] == "2026-01-01T00:00:00Z"

    def test_to_dict_omits_produced_at_when_none(self):
        inp = BundleInput(source="mm.v1", freshness="FRESH")
        d = inp.to_dict()
        assert "produced_at" not in d


class TestBundleAnalysis:
    def test_to_dict_omits_none_values(self):
        a = BundleAnalysis(timeframe="1H", bias_short_term="BULLISH")
        d = a.to_dict()
        assert d["timeframe"] == "1H"
        assert d["bias_short_term"] == "BULLISH"
        assert "invalidation" not in d
        assert "notes" not in d

    def test_defaults_are_unknown(self):
        a = BundleAnalysis()
        assert a.bias_short_term == "UNKNOWN"
        assert a.confidence == "UNKNOWN"


class TestContractValidator:
    def test_valid_bundle_passes(self):
        errors = validate_bundle(_make_valid_bundle())
        assert errors == []

    def test_missing_contract_key(self):
        d = _make_valid_bundle()
        del d["contract"]
        errors = validate_bundle(d)
        assert any("contract" in e for e in errors)

    def test_contract_must_start_with_bundle(self):
        d = _make_valid_bundle(contract="not.a.bundle")
        errors = validate_bundle(d)
        assert any("bundle." in e for e in errors)

    def test_invalid_freshness_state(self):
        d = _make_valid_bundle(freshness_state="INVALID")
        errors = validate_bundle(d)
        assert any("freshness_state" in e for e in errors)

    def test_assets_must_be_list_of_strings(self):
        d = _make_valid_bundle(assets="BTC")
        errors = validate_bundle(d)
        assert any("assets" in e for e in errors)

    def test_assets_with_non_string_element(self):
        d = _make_valid_bundle(assets=[1, 2])
        errors = validate_bundle(d)
        assert any("assets" in e for e in errors)

    def test_inputs_must_be_dict(self):
        d = _make_valid_bundle(inputs="not_a_dict")
        errors = validate_bundle(d)
        assert any("inputs" in e for e in errors)

    def test_input_entry_missing_source(self):
        d = _make_valid_bundle()
        d["inputs"]["market_metrics"] = {"freshness": "FRESH"}
        errors = validate_bundle(d)
        assert any("source" in e for e in errors)

    def test_input_entry_missing_freshness(self):
        d = _make_valid_bundle()
        d["inputs"]["market_metrics"] = {"source": "s"}
        errors = validate_bundle(d)
        assert any("freshness" in e for e in errors)

    def test_analysis_must_be_dict(self):
        d = _make_valid_bundle(analysis="str")
        errors = validate_bundle(d)
        assert any("analysis" in e for e in errors)

    def test_invalid_bias_short_term(self):
        d = _make_valid_bundle()
        d["analysis"]["bias_short_term"] = "INVALID"
        errors = validate_bundle(d)
        assert any("bias_short_term" in e for e in errors)

    def test_invalid_regime(self):
        d = _make_valid_bundle()
        d["analysis"]["regime"] = "INVALID"
        errors = validate_bundle(d)
        assert any("regime" in e for e in errors)

    def test_invalid_squeeze_level(self):
        d = _make_valid_bundle()
        d["analysis"]["squeeze_or_stress_level"] = "EXTREME"
        errors = validate_bundle(d)
        assert any("squeeze_or_stress_level" in e for e in errors)

    def test_invalid_confidence(self):
        d = _make_valid_bundle()
        d["analysis"]["confidence"] = "SUPER"
        errors = validate_bundle(d)
        assert any("confidence" in e for e in errors)

    def test_stale_with_empty_missing_inputs(self):
        d = _make_valid_bundle(freshness_state="STALE", missing_inputs=[])
        errors = validate_bundle(d)
        assert any("missing_inputs" in e for e in errors)

    def test_stale_with_non_empty_missing_inputs_ok(self):
        d = _make_valid_bundle(freshness_state="STALE", missing_inputs=["mm: stale"])
        errors = validate_bundle(d)
        assert errors == []

    def test_non_dict_input(self):
        errors = validate_bundle("not_a_dict")
        assert any("dict" in e for e in errors)

    def test_missing_multiple_keys(self):
        d = {}
        errors = validate_bundle(d)
        assert len(errors) >= 8

    def test_all_freshness_states_accepted(self):
        for state in VALID_FRESHNESS_STATES:
            d = _make_valid_bundle(freshness_state=state)
            if state == "STALE":
                d["missing_inputs"] = ["test: stale"]
            errors = validate_bundle(d)
            assert errors == [], f"failed for state={state}: {errors}"

    def test_hypothesis_state_accepted(self):
        d = _make_valid_bundle(freshness_state="HYPOTHESIS", missing_inputs=["ALL: HYPOTHESIS"])
        errors = validate_bundle(d)
        assert errors == []

    def test_missing_inputs_must_be_list(self):
        d = _make_valid_bundle(missing_inputs="not_a_list")
        errors = validate_bundle(d)
        assert any("missing_inputs" in e for e in errors)

    def test_source_refs_must_be_list(self):
        d = _make_valid_bundle(source_refs="not_a_list")
        errors = validate_bundle(d)
        assert any("source_refs" in e for e in errors)


class TestBtcCoreProducer:
    def test_produce_returns_bundle_output(self):
        bundle = produce_btc_core()
        assert isinstance(bundle, BundleOutput)
        assert bundle.contract == "bundle.btc_core.v1"
        assert bundle.bundle_id == "btc.core.v1"

    def test_produce_validates(self):
        bundle = produce_btc_core()
        errors = validate_bundle(bundle.to_dict())
        assert errors == [], f"validation errors: {errors}"

    def test_produce_without_data_is_valid(self):
        bundle = produce_btc_core()
        d = bundle.to_dict()
        assert len(d["assets"]) == 2
        assert "inputs" in d
        assert "market_metrics" in d["inputs"]
        assert "coinglass_vision" in d["inputs"]
        assert "telegram_signals" in d["inputs"]

    def test_produce_freshness_is_stale_when_no_data(self):
        bundle = produce_btc_core()
        assert bundle.freshness_state in ("STALE", "UNKNOWN")

    def test_produce_with_custom_symbol(self):
        bundle = produce_btc_core(symbol="ETHUSDT", asset="ETH")
        assert "ETH" in bundle.assets
        assert "ETHUSDT" in bundle.assets


class TestMacroProducer:
    def test_produce_returns_bundle_output(self):
        bundle = produce_macro()
        assert isinstance(bundle, BundleOutput)
        assert bundle.contract == "bundle.macro.v1"
        assert bundle.bundle_id == "macro.v1"

    def test_produce_validates(self):
        bundle = produce_macro()
        errors = validate_bundle(bundle.to_dict())
        assert errors == [], f"validation errors: {errors}"

    def test_produce_includes_all_symbols(self):
        bundle = produce_macro()
        assets = bundle.assets
        for sym in ("DXY", "GOLD", "VIX", "SPX"):
            assert sym in assets, f"missing established symbol: {sym}"

    def test_macro_inputs_include_hypothesis(self):
        bundle = produce_macro()
        d = bundle.to_dict()
        inputs = d["inputs"]
        assert "TVC:DXY" in inputs
        assert "OANDA:XAUUSD" in inputs
        assert "TVC:VIX" in inputs
        assert "TVC:US10Y" in inputs
        assert "SPY" in inputs
        assert "NYMEX:CL1!" in inputs

    def test_hypothesis_inputs_are_marked_as_such(self):
        bundle = produce_macro()
        d = bundle.to_dict()
        inputs = d["inputs"]
        for sym in ("NYMEX:RB1!", "NYMEX:NG1!"):
            if sym in inputs:
                assert inputs[sym]["status"] == "HYPOTHESIS"


class TestBundleRoundTrip:
    def test_btc_core_to_dict_and_back(self):
        bundle = produce_btc_core()
        d = bundle.to_dict()
        errors = validate_bundle(d)
        assert errors == []

    def test_macro_to_dict_and_back(self):
        bundle = produce_macro()
        d = bundle.to_dict()
        errors = validate_bundle(d)
        assert errors == []


class TestSchemaEnums:
    def test_valid_freshness_states_contain_expected(self):
        assert "FRESH" in VALID_FRESHNESS_STATES
        assert "STALE" in VALID_FRESHNESS_STATES
        assert "UNKNOWN" in VALID_FRESHNESS_STATES
        assert "HYPOTHESIS" in VALID_FRESHNESS_STATES

    def test_valid_bias_contains_expected(self):
        for val in ("BULLISH", "BEARISH", "NEUTRAL", "UNKNOWN"):
            assert val in VALID_BIAS

    def test_valid_regime_contains_expected(self):
        for val in ("TRENDING", "RANGING", "LONG_SKEWED", "RISK_ON", "RISK_OFF", "UNKNOWN"):
            assert val in VALID_REGIME

    def test_valid_squeeze_contains_expected(self):
        for val in ("LOW", "MEDIUM", "ELEVATED", "HIGH", "UNKNOWN"):
            assert val in VALID_SQUEEZE

    def test_valid_confidence_contains_expected(self):
        for val in ("HIGH", "MEDIUM", "LOW", "UNKNOWN"):
            assert val in VALID_CONFIDENCE
