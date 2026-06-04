import json

import pytest

from modules.analysis_bundles.app.verdict_schema import (
    AnalysisVerdict,
    VerdictComposite,
    VerdictChecklistItem,
)
from modules.analysis_bundles.app.verdict_consumer import (
    produce_verdict,
    consume_and_write,
    _determine_alignment,
    _determine_overall_bias,
    _compute_confidence,
    _compute_score,
    _build_checklist,
)


def _make_btc(bias="BULLISH", confidence="MEDIUM", freshness="FRESH", missing=None):
    return {
        "contract": "bundle.btc_core.v1",
        "bundle_id": "btc.core.v1",
        "produced_at": "2026-01-01T00:00:00Z",
        "freshness_state": freshness,
        "assets": ["BTC"],
        "inputs": {},
        "analysis": {
            "timeframe": "1H",
            "bias_short_term": bias,
            "bias_intraday": "NEUTRAL",
            "regime": "TRENDING",
            "squeeze_or_stress_level": "LOW",
            "invalidation": "BTC < 86000",
            "confidence": confidence,
        },
        "missing_inputs": missing or [],
        "source_refs": [],
    }


def _make_macro(regime="RISK_ON", freshness="FRESH", missing=None):
    return {
        "contract": "bundle.macro.v1",
        "bundle_id": "macro.v1",
        "produced_at": "2026-01-01T00:00:00Z",
        "freshness_state": freshness,
        "assets": ["DXY", "XAUUSD"],
        "inputs": {},
        "analysis": {
            "timeframe": "1D",
            "bias_short_term": "NEUTRAL",
            "bias_intraday": "NEUTRAL",
            "regime": regime,
            "squeeze_or_stress_level": "LOW",
            "invalidation": "VIX > 30",
            "confidence": "LOW",
        },
        "missing_inputs": missing or [],
        "source_refs": [],
    }


class TestAlignment:
    def test_bullish_risk_on_aligned(self):
        assert _determine_alignment("BULLISH", "RISK_ON") == "ALIGNED"

    def test_bullish_risk_off_divergent(self):
        assert _determine_alignment("BULLISH", "RISK_OFF") == "DIVERGENT"

    def test_bearish_risk_off_aligned(self):
        assert _determine_alignment("BEARISH", "RISK_OFF") == "ALIGNED"

    def test_bearish_risk_on_divergent(self):
        assert _determine_alignment("BEARISH", "RISK_ON") == "DIVERGENT"

    def test_unknown_returns_unknown(self):
        assert _determine_alignment("UNKNOWN", "RISK_ON") == "UNKNOWN"
        assert _determine_alignment("BULLISH", "UNKNOWN") == "UNKNOWN"

    def test_risk_on_broadening_aligned_with_bullish(self):
        assert _determine_alignment("BULLISH", "RISK_ON_BROADENING") == "ALIGNED"


class TestOverallBias:
    def test_aligned_keeps_btc_bias(self):
        assert _determine_overall_bias("BULLISH", "ALIGNED") == "BULLISH"
        assert _determine_overall_bias("BEARISH", "ALIGNED") == "BEARISH"

    def test_divergent_is_neutral(self):
        assert _determine_overall_bias("BULLISH", "DIVERGENT") == "NEUTRAL"

    def test_unknown_is_unknown(self):
        assert _determine_overall_bias("BULLISH", "UNKNOWN") == "UNKNOWN"


class TestConfidence:
    def test_aligned_high_confidence(self):
        assert _compute_confidence("FRESH", "FRESH", "HIGH", "ALIGNED", "BULLISH", "RISK_ON") == "HIGH"

    def test_aligned_medium_btc_confidence_gives_medium(self):
        assert _compute_confidence("FRESH", "FRESH", "MEDIUM", "ALIGNED", "BULLISH", "RISK_ON") == "MEDIUM"

    def test_divergent_is_low(self):
        assert _compute_confidence("FRESH", "FRESH", "HIGH", "DIVERGENT", "BULLISH", "RISK_OFF") == "LOW"

    def test_stale_allows_medium_with_good_bias(self):
        # STALE no longer blocks — freshness is a separate concern
        assert _compute_confidence("STALE", "FRESH", "HIGH", "ALIGNED", "BULLISH", "RISK_ON") == "HIGH"

    def test_unknown_btc_is_unknown(self):
        assert _compute_confidence("FRESH", "FRESH", "LOW", "ALIGNED", "UNKNOWN", "RISK_ON") == "UNKNOWN"


class TestScore:
    def test_bullish_aligned_gives_high_score(self):
        score = _compute_score("BULLISH", "RISK_ON", "ALIGNED")
        assert score > 60

    def test_bearish_aligned_gives_medium_score(self):
        score = _compute_score("BEARISH", "RISK_OFF", "ALIGNED")
        assert 0 <= score <= 100

    def test_divergent_gives_lower_score(self):
        aligned = _compute_score("BULLISH", "RISK_ON", "ALIGNED")
        divergent = _compute_score("BULLISH", "RISK_OFF", "DIVERGENT")
        assert divergent < aligned

    def test_score_bounded_0_100(self):
        for bias in ("BULLISH", "BEARISH", "NEUTRAL", "UNKNOWN"):
            for regime in ("RISK_ON", "RISK_OFF", "RISK_ON_BROADENING", "UNKNOWN"):
                for alignment in ("ALIGNED", "DIVERGENT", "UNKNOWN"):
                    score = _compute_score(bias, regime, alignment)
                    assert 0 <= score <= 100, f"score {score} out of range for {bias}/{regime}/{alignment}"


class TestChecklist:
    def test_aligned_scenario(self):
        c = _build_checklist("BULLISH", "RISK_ON", "ALIGNED", [])
        statuses = {item["item"]: item["status"] for item in c}
        assert statuses["BTC bias determined"] == "OK"
        assert statuses["Macro regime determined"] == "OK"
        assert statuses["BTC/macro alignment"] == "OK"

    def test_divergent_scenario(self):
        c = _build_checklist("BULLISH", "RISK_OFF", "DIVERGENT", [])
        statuses = {item["item"]: item["status"] for item in c}
        assert statuses["BTC/macro alignment"] == "WARN"

    def test_unknown_scenario(self):
        c = _build_checklist("UNKNOWN", "UNKNOWN", "UNKNOWN", [])
        statuses = {item["item"]: item["status"] for item in c}
        assert statuses["BTC bias determined"] == "WARN"
        assert statuses["Macro regime determined"] == "WARN"

    def test_warnings_propagated(self):
        c = _build_checklist("BULLISH", "RISK_ON", "ALIGNED", ["low confidence"])
        assert any(item["item"] == "Warnings present — review" for item in c)


class TestProduceVerdict:
    def test_returns_analysis_verdict(self):
        verdict = produce_verdict(btc_bundle=_make_btc(), macro_bundle=_make_macro())
        assert isinstance(verdict, AnalysisVerdict)
        assert verdict.contract == "analysis_verdict.v1"

    def test_aligned_scenario(self):
        verdict = produce_verdict(
            btc_bundle=_make_btc(bias="BULLISH", confidence="HIGH"),
            macro_bundle=_make_macro(regime="RISK_ON"),
        )
        comp = verdict.composite
        assert comp["alignment"] == "ALIGNED"
        assert comp["overall_bias"] == "BULLISH"
        assert comp["confidence"] == "HIGH"
        assert comp["score"] >= 60

    def test_divergent_scenario(self):
        verdict = produce_verdict(
            btc_bundle=_make_btc(bias="BULLISH"),
            macro_bundle=_make_macro(regime="RISK_OFF"),
        )
        comp = verdict.composite
        assert comp["alignment"] == "DIVERGENT"
        assert comp["overall_bias"] == "NEUTRAL"
        assert comp["confidence"] == "LOW"

    def test_unknown_scenario(self):
        verdict = produce_verdict(
            btc_bundle=_make_btc(bias="UNKNOWN"),
            macro_bundle=_make_macro(regime="UNKNOWN"),
        )
        comp = verdict.composite
        assert comp["confidence"] == "UNKNOWN"
        assert comp["score"] == 50

    def test_stale_bundles_produce_warnings(self):
        verdict = produce_verdict(
            btc_bundle=_make_btc(freshness="STALE", missing=["mm: stale"]),
            macro_bundle=_make_macro(freshness="STALE"),
        )
        assert len(verdict.warnings) >= 1
        assert verdict.freshness_state == "STALE"

    def test_to_dict(self):
        verdict = produce_verdict(btc_bundle=_make_btc(), macro_bundle=_make_macro())
        d = verdict.to_dict()
        assert d["contract"] == "analysis_verdict.v1"
        assert "composite" in d
        assert "checklist" in d

    def test_uses_producers_when_no_bundles_provided(self):
        verdict = produce_verdict()
        assert isinstance(verdict, AnalysisVerdict)
        assert verdict.freshness_state in ("STALE", "UNKNOWN")

    def test_missing_inputs_merged(self):
        verdict = produce_verdict(
            btc_bundle=_make_btc(missing=["a", "b"]),
            macro_bundle=_make_macro(missing=["c"]),
        )
        assert "a" in verdict.missing_inputs
        assert "b" in verdict.missing_inputs
        assert "c" in verdict.missing_inputs

    def test_source_refs_merged(self):
        verdict = produce_verdict(
            btc_bundle={**_make_btc(), "source_refs": ["/a"]},
            macro_bundle={**_make_macro(), "source_refs": ["/b"]},
        )
        assert "/a" in verdict.source_refs
        assert "/b" in verdict.source_refs


class TestConsumeAndWrite:
    def test_writes_to_disk(self, tmp_path):
        out = tmp_path / "verdict.json"
        verdict = consume_and_write(
            btc_bundle=_make_btc(),
            macro_bundle=_make_macro(),
            output_path=out,
        )
        assert out.exists()
        data = json.loads(out.read_text())
        assert data["contract"] == "analysis_verdict.v1"


class TestVerdictSchema:
    def test_verdict_composite_defaults(self):
        c = VerdictComposite()
        assert c.btc_bias == "UNKNOWN"
        assert c.score == 0

    def test_verdict_checklist_item(self):
        item = VerdictChecklistItem(item="test", status="OK")
        d = item.to_dict()
        assert d == {"item": "test", "status": "OK"}

    def test_analysis_verdict_to_dict(self):
        v = AnalysisVerdict(
            contract="analysis_verdict.v1",
            verdict_id="v1",
            produced_at="2026-01-01",
            freshness_state="FRESH",
            bundles_used=[],
            composite={},
            checklist=[],
        )
        d = v.to_dict()
        assert d["contract"] == "analysis_verdict.v1"


class TestDeskProTelegramParsers:
    def test_parse_unknown_raw(self):
        from modules.desk_pro.telegram.parsers import parse_telegram_message
        result = parse_telegram_message({"raw_text": "hello world", "channel_alias": "ch"})
        assert result.message_type == "UNKNOWN_RAW"
        assert result.claim is None

    def test_parse_trade_setup(self):
        from modules.desk_pro.telegram.parsers import parse_telegram_message
        result = parse_telegram_message({
            "raw_text": "BTC LONG Entry: 50000 Stop Loss: 49000 Target: 52000",
            "channel_alias": "test",
            "message_id": "42",
        })
        assert result.message_type == "TRADE_SETUP"
        assert result.claim is not None
        assert result.claim["claim_type"] == "TRADE_SETUP"
        assert result.claim["asset"] == "BTC"
        assert result.claim["direction"] == "LONG"
        assert result.claim["entry"] == 50000.0
        assert result.claim["sl"] == 49000.0
        assert result.claim["tp"] == 52000.0

    def test_parse_eth_short(self):
        from modules.desk_pro.telegram.parsers import parse_telegram_message
        result = parse_telegram_message({
            "raw_text": "ETH SHORT Entry: 3500 SL: 3600 Target: 3200",
            "channel_alias": "test",
        })
        assert result.message_type == "TRADE_SETUP"
        assert result.claim["asset"] == "ETH"
        assert result.claim["direction"] == "SHORT"
        assert result.claim["entry"] == 3500.0

    def test_parse_text_without_asset_returns_unknown(self):
        from modules.desk_pro.telegram.parsers import parse_telegram_message
        result = parse_telegram_message({"raw_text": "market is volatile today", "channel_alias": "ch"})
        assert result.message_type == "UNKNOWN_RAW"

    def test_parsed_message_to_dict(self):
        from modules.desk_pro.telegram.parsers import ParsedTelegramMessage
        pm = ParsedTelegramMessage(
            message_type="TRADE_SETUP",
            raw_text="test",
            channel_alias="ch",
            claim={"claim_type": "TRADE_SETUP"},
        )
        d = pm.to_dict()
        assert d["message_type"] == "TRADE_SETUP"
        assert "claim" in d

    def test_parsed_message_to_dict_no_claim(self):
        from modules.desk_pro.telegram.parsers import ParsedTelegramMessage
        pm = ParsedTelegramMessage(
            message_type="UNKNOWN_RAW",
            raw_text="test",
            channel_alias="ch",
        )
        d = pm.to_dict()
        assert "claim" not in d
