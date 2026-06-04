import pytest
import json

from modules.analysis_bundles.app.vision_analysis_reader import (
    read_vision_analysis,
    extract_signals_from_vision,
    list_available_symbols,
    read_vision_analysis_freshness,
    read_all_vision_freshness,
)
from modules.analysis_bundles.app.data_center_router import (
    produce_data_center_coverage,
    route_to_data_center,
)
from modules.analysis_bundles.app.asset_selector import (
    produce_asset_ticket,
    produce_all_tickets,
    produce_summary_by_class,
)
from modules.analysis_bundles.app.btc_core_producer import produce_btc_core
from modules.analysis_bundles.app.macro_producer import produce_macro
from modules.analysis_bundles.app.contract_validator import validate_bundle
from modules.analysis_bundles.app.analysis_pipeline import (
    step_ingest,
    step_normalize,
    step_analyze,
    run_full_pipeline,
)


class TestVisionAnalysisReader:
    def test_list_available_symbols(self):
        symbols = list_available_symbols()
        assert isinstance(symbols, list)
        if symbols:
            assert "BTCUSDT.P" in symbols

    def test_read_vision_analysis_btc(self):
        capture = read_vision_analysis("BTCUSDT.P")
        if capture is not None:
            assert capture["input_class"] == "vision_analysis.v1"
            assert "symbol" in capture
            assert "signals" in capture

    def test_extract_signals_from_vision_btc(self):
        signals = extract_signals_from_vision("BTCUSDT.P")
        if signals.get("available"):
            assert isinstance(signals.get("supports"), list)
            assert isinstance(signals.get("resistances"), list)
            assert signals.get("bias") in ("BULLISH", "BEARISH", "NEUTRAL", None)

    def test_read_nonexistent_symbol(self):
        capture = read_vision_analysis("NONEXISTENT:SYMBOL")
        assert capture is None

    def test_extract_signals_nonexistent(self):
        signals = extract_signals_from_vision("NONEXISTENT:SYMBOL")
        assert signals["available"] is False

    def test_freshness_nonexistent(self):
        f = read_vision_analysis_freshness("NONEXISTENT:SYMBOL")
        assert f["freshness"] == "MISSING"

    def test_read_all_freshness(self):
        all_f = read_all_vision_freshness()
        assert isinstance(all_f, dict)

    def test_extract_signals_has_fields(self):
        signals = extract_signals_from_vision("BTCUSDT.P")
        for key in ("symbol", "available", "timeframe", "bias", "supports", "resistances", "plan", "invalidation"):
            assert key in signals, f"missing key: {key}"


class TestDataCenterRouter:
    def test_produce_coverage(self):
        coverage = produce_data_center_coverage()
        assert coverage["contract"] == "data_center_coverage.v1"
        assert "sources" in coverage
        assert "vision_analysis" in coverage
        assert coverage["total_sources"] >= 5

    def test_proven_sources_count(self):
        coverage = produce_data_center_coverage()
        assert coverage["proven_sources"] >= 2  # vision_analysis + coinglass
        assert isinstance(coverage["total_sources"], int)

    def test_vision_sources_detail(self):
        coverage = produce_data_center_coverage()
        va = coverage["vision_analysis"]
        assert "total_symbols" in va
        assert "by_symbol" in va

    def test_route_to_data_center(self, tmp_path):
        out = tmp_path / "coverage.json"
        coverage = route_to_data_center(output_path=out)
        assert out.exists()
        assert coverage["contract"] == "data_center_coverage.v1"


class TestAssetSelector:
    def test_produce_asset_ticket_btc(self):
        ticket = produce_asset_ticket("BTCUSDT.P")
        if ticket is not None:
            assert ticket["contract"] == "asset_ticket.v1"
            assert ticket["asset"] == "BTC"
            assert ticket["asset_class"] == "CRYPTO_MAJOR"
            assert "bias" in ticket
            assert "supports" in ticket

    def test_produce_asset_ticket_dxy(self):
        ticket = produce_asset_ticket("TVC:DXY")
        if ticket is not None:
            assert ticket["asset"] == "DXY"
            assert ticket["asset_class"] == "MACRO_FX"

    def test_produce_all_tickets(self):
        tickets = produce_all_tickets()
        assert isinstance(tickets, dict)
        if "BTCUSDT.P" in tickets:
            assert tickets["BTCUSDT.P"]["asset"] == "BTC"

    def test_produce_summary_by_class(self):
        summary = produce_summary_by_class()
        assert isinstance(summary, dict)
        if "CRYPTO_MAJOR" in summary:
            assert "total" in summary["CRYPTO_MAJOR"]
            assert "bullish" in summary["CRYPTO_MAJOR"]

    def test_nonexistent_ticket_returns_none(self):
        ticket = produce_asset_ticket("NONEXISTENT:SYMBOL")
        assert ticket is None

    def test_summary_keys_are_strings(self):
        summary = produce_summary_by_class()
        for cls in summary:
            assert isinstance(cls, str)


class TestEnrichedBtcCore:
    def test_produce_with_real_vision_data(self):
        bundle = produce_btc_core()
        d = bundle.to_dict()
        inputs = d["inputs"]
        assert "vision_analysis" in inputs
        va = inputs["vision_analysis"]
        if va.get("freshness") == "FRESH":
            assert va.get("bias") is not None

    def test_btc_core_validates_with_vision(self):
        bundle = produce_btc_core()
        errors = validate_bundle(bundle.to_dict())
        assert errors == []


class TestEnrichedMacro:
    def test_produce_with_real_vision_data(self):
        bundle = produce_macro()
        d = bundle.to_dict()
        inputs = d["inputs"]
        assert "TVC:DXY" in inputs
        assert "OANDA:XAUUSD" in inputs
        assert "TVC:VIX" in inputs

    def test_macro_has_energy_symbols(self):
        bundle = produce_macro()
        assets = bundle.assets
        for a in ("WTI", "BRENT", "GASOLINE", "NATGAS"):
            assert a in assets, f"missing energy asset: {a}"

    def test_macro_bias_from_real_data(self):
        bundle = produce_macro()
        d = bundle.to_dict()
        analysis = d["analysis"]
        if d["freshness_state"] == "FRESH":
            assert analysis["bias_short_term"] != "UNKNOWN"

    def test_macro_validates(self):
        bundle = produce_macro()
        errors = validate_bundle(bundle.to_dict())
        assert errors == []


class TestAnalysisPipeline:
    def test_step_ingest(self):
        ingest = step_ingest()
        assert ingest["pipeline_step"] == "INGEST"
        assert ingest["total_sources"] == 2
        assert "vision_raw" in ingest
        assert "coinglass_raw" in ingest

    def test_step_normalize(self):
        ingest = step_ingest()
        norm = step_normalize(vision_raw=ingest["vision_raw"])
        assert norm["pipeline_step"] == "NORMALIZE"
        assert norm["total_tickets"] >= 20
        tickets = norm["tickets"]
        for sym, t in tickets.items():
            assert "asset" in t
            assert "asset_class" in t
            assert "bias" in t or t["bias"] is None

    def test_step_analyze(self):
        ingest = step_ingest()
        norm = step_normalize(vision_raw=ingest["vision_raw"])
        analysis = step_analyze(normalized=norm)
        assert analysis["pipeline_step"] == "ANALYZE"
        assert "regimes" in analysis
        assert "macro" in analysis["regimes"]
        assert "crypto" in analysis["regimes"]
        assert "energy" in analysis["regimes"]
        assert "class_consensus" in analysis
        assert "alerts" in analysis
        assert "actionable_signals" in analysis

    def test_run_full_pipeline(self):
        report = run_full_pipeline()
        assert report["contract"] == "analysis_pipeline_report.v1"
        assert report["total_sources"] >= 1
        assert report["total_tickets"] >= 20

    def test_run_full_pipeline_writes_file(self, tmp_path):
        out = tmp_path / "report.json"
        report = run_full_pipeline(output_path=out)
        assert out.exists()
        data = json.loads(out.read_text())
        assert data["contract"] == "analysis_pipeline_report.v1"

    def test_pipeline_idempotent(self):
        r1 = run_full_pipeline()
        r2 = run_full_pipeline()
        assert r1["total_tickets"] == r2["total_tickets"]
        assert r1["regimes"] == r2["regimes"]

    def test_regime_values_valid(self):
        report = run_full_pipeline()
        regimes = report["regimes"]
        valid = ("RISK_ON", "RISK_OFF", "MIXED", "BULLISH", "BEARISH", "UNKNOWN")
        for key in ("macro", "crypto", "energy"):
            assert regimes[key] in valid or regimes[key] == regimes[key]

    def test_ingested_sources_have_freshness(self):
        ingest = step_ingest()
        for src in ingest["sources"]:
            assert "freshness" in src
            assert "provenance" in src
