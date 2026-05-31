"""Validate Screener analyzer, writer, pipeline integration, and DC registry."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "capture_mapping"
PROFILES_DIR = Path(__file__).resolve().parent.parent / "modules" / "bot_vision" / "headless_capture"
SCRIPTS_DIR = PROFILES_DIR / "scripts"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


# ── Screener Analyzer import smoke ─────────────────────────

class TestScreenerAnalyzerImport:
    def test_import_ok(self):
        import importlib.util
        path = SCRIPTS_DIR / "screener_analyzer.py"
        spec = importlib.util.spec_from_file_location("screener_analyzer", str(path))
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"

    def test_has_analyze_function(self):
        source = (SCRIPTS_DIR / "screener_analyzer.py").read_text(encoding="utf-8")
        assert "def analyze" in source

    def test_all_screener_categories(self):
        source = (SCRIPTS_DIR / "screener_analyzer.py").read_text(encoding="utf-8")
        for cat in ["SCREENER_BIGGEST_CAPS", "SCREENER_TRENDING", "SCREENER_AI",
                     "SCREENER_DEFENSE", "SCREENER_SPATIAL", "SCREENER_CRYPTO_STOCKS", "SCREENER_ENERGY"]:
            assert cat in source


# ── Stub mode output ───────────────────────────────────────

class TestScreenerAnalyzerStub:
    def test_analyze_returns_valid_schema(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from screener_analyzer import analyze
        finally:
            sys.path.pop(0)

        sidecar = {
            "screen_type": "SCREENER_STOCKS",
            "symbol": "SCREENER_BIGGEST_CAPS",
            "source": "tradingview_screener",
            "created_at_utc": "2026-05-30T12:00:00Z",
        }
        result = analyze(sidecar, use_real_ocr=False)
        assert result["input_class"] == "vision_context.screener.v1"
        assert result["screener_symbol"] == "SCREENER_BIGGEST_CAPS"
        assert result["stock_count"] > 0
        assert len(result["stocks"]) > 0

    def test_stub_stocks_have_required_fields(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from screener_analyzer import analyze
        finally:
            sys.path.pop(0)

        for cat in ["SCREENER_BIGGEST_CAPS", "SCREENER_TRENDING", "SCREENER_AI",
                     "SCREENER_DEFENSE", "SCREENER_SPATIAL", "SCREENER_CRYPTO_STOCKS", "SCREENER_ENERGY"]:
            sidecar = {"screen_type": "SCREENER_STOCKS", "symbol": cat, "source": "tradingview_screener"}
            result = analyze(sidecar)
            for stock in result["stocks"]:
                assert "symbol" in stock
                assert "name" in stock
                assert "price" in stock
                assert "change_pct" in stock
                assert "confidence" in stock
                assert isinstance(stock["confidence"], (int, float))
                assert 0 <= stock["confidence"] <= 1.0

    def test_stub_values_vary_by_category(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from screener_analyzer import analyze
        finally:
            sys.path.pop(0)

        caps = analyze({"screen_type": "SCREENER_STOCKS", "symbol": "SCREENER_BIGGEST_CAPS", "source": "tradingview_screener"})
        ai = analyze({"screen_type": "SCREENER_STOCKS", "symbol": "SCREENER_AI", "source": "tradingview_screener"})
        caps_syms = {s["symbol"] for s in caps["stocks"]}
        ai_syms = {s["symbol"] for s in ai["stocks"]}
        assert caps_syms != ai_syms, "Stub stocks should differ by category"
        assert "NVDA" in caps_syms  # NVDA is in biggest caps
        assert "NVDA" in ai_syms    # NVDA is also in AI

    def test_analyze_pipe_via_stdin(self):
        sidecar = json.dumps({"screen_type": "SCREENER_STOCKS", "symbol": "SCREENER_TRENDING", "source": "tradingview_screener"})
        cmd = [sys.executable, str(SCRIPTS_DIR / "screener_analyzer.py"), "--stdin"]
        result = subprocess.run(cmd, input=sidecar, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        assert data["input_class"] == "vision_context.screener.v1"
        assert data["stock_count"] > 0

    def test_top_gainers_losers_computed(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from screener_analyzer import analyze
        finally:
            sys.path.pop(0)

        result = analyze({"screen_type": "SCREENER_STOCKS", "symbol": "SCREENER_BIGGEST_CAPS", "source": "tradingview_screener"})
        assert len(result["top_gainers"]) > 0
        assert "avg_change_pct" in result
        assert isinstance(result["avg_change_pct"], (int, float))


# ── Screener Writer ────────────────────────────────────────

class TestScreenerWriter:
    def test_import_ok(self):
        import importlib.util
        path = SCRIPTS_DIR / "screener_writer.py"
        spec = importlib.util.spec_from_file_location("screener_writer", str(path))
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"

    def test_validate_rejects_bad_input_class(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from screener_writer import validate
        finally:
            sys.path.pop(0)

        assert validate({"input_class": "wrong"}) is False
        assert validate({"input_class": "vision_context.screener.v1", "stocks": []}) is True

    def test_pipe_via_stdin(self):
        data = load_fixture("vision_context_screener_v1_sample.json")
        cmd = [sys.executable, str(SCRIPTS_DIR / "screener_writer.py"), "--dry-run", "--stdin"]
        result = subprocess.run(cmd, input=json.dumps(data), capture_output=True, text=True, timeout=15)
        assert result.returncode == 0


# ── Fixture validation ────────────────────────────────────

class TestScreenerFixture:
    FIXTURE = "vision_context_screener_v1_sample.json"

    def test_required_fields(self):
        data = load_fixture(self.FIXTURE)
        assert data["input_class"] == "vision_context.screener.v1"
        assert "screener_symbol" in data
        assert "screener_label" in data
        assert "stocks" in data
        assert "stock_count" in data
        assert "avg_change_pct" in data

    def test_stock_structure(self):
        data = load_fixture(self.FIXTURE)
        for stock in data["stocks"]:
            assert "symbol" in stock
            assert "name" in stock
            assert "price" in stock
            assert "change_pct" in stock
            assert "confidence" in stock

    def test_stock_count_matches(self):
        data = load_fixture(self.FIXTURE)
        assert data["stock_count"] == len(data["stocks"])


# ── Pipeline integration ──────────────────────────────────

class TestPipelineIntegration:
    def test_has_screener_analyzer_ref(self):
        source = (SCRIPTS_DIR / "run_vision_pipeline.py").read_text(encoding="utf-8")
        assert "screener_analyzer" in source
        assert "screener_writer" in source
        assert "SCREENER_TYPES" in source

    def test_has_screener_dispatch(self):
        source = (SCRIPTS_DIR / "run_vision_pipeline.py").read_text(encoding="utf-8")
        assert "Screener dispatch" in source or "screener_analyzer" in source

    def test_no_longer_says_tbd(self):
        source = (SCRIPTS_DIR / "run_vision_pipeline.py").read_text(encoding="utf-8")
        assert "Screener analyzer TBD" not in source
        assert "not yet implemented" not in source

    def test_orchestrator_has_screener_dispatch(self):
        source = (SCRIPTS_DIR / "schedule_orchestrator.py").read_text(encoding="utf-8")
        assert "screener_analyzer" in source or "screener_writer" in source
        assert "--dry-run" not in source.split("SCREENER_STOCKS")[1].split("\n")[0] if "SCREENER_STOCKS" in source else True

    def test_pipeline_import_ok(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "run_vision_pipeline_screener",
            str(SCRIPTS_DIR / "run_vision_pipeline.py"),
        )
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"


# ── Screen Types Registry ─────────────────────────────────

class TestScreenTypesUpdated:
    def test_screener_analyzer_ref_updated(self):
        data = json.loads((PROFILES_DIR / "screen_types.json").read_text(encoding="utf-8"))
        for st in data["screen_types"]:
            if st["id"] == "SCREENER_STOCKS":
                assert "screener_analyzer" in st["analyzer"]
                assert "A-08" in st["analyzer"]

    def test_coinglass_analyzer_ref_updated(self):
        data = json.loads((PROFILES_DIR / "screen_types.json").read_text(encoding="utf-8"))
        for st in data["screen_types"]:
            if st["id"] in ("LIQUIDITY_COINGLASS", "FUNDING_COINGLASS", "OI_COINGLASS", "LS_RATIO_COINGLASS"):
                assert "coinglass_ocr_analyzer" in st["analyzer"]
                assert "TBD" not in st["analyzer"]

    def test_news_sentiment_analyzer_ref(self):
        data = json.loads((PROFILES_DIR / "screen_types.json").read_text(encoding="utf-8"))
        for st in data["screen_types"]:
            if st["id"] == "NEWS_SENTIMENT":
                assert "news_sentiment_analyzer" in st["analyzer"]
                assert "A-09" in st["analyzer"]


# ── Data Center Registry ──────────────────────────────────

class TestDataCenterRegistryScreener:
    DC_REGISTRY_DIR = Path(__file__).resolve().parent.parent / "modules" / "data_center" / "registry"

    def test_producer_includes_screener(self):
        data = json.loads((self.DC_REGISTRY_DIR / "producers.json").read_text(encoding="utf-8"))
        producer_ids = {p["producer_id"] for p in data["producers"]}
        assert "bot_vision_headless__screener" in producer_ids

    def test_producer_contract_correct(self):
        data = json.loads((self.DC_REGISTRY_DIR / "producers.json").read_text(encoding="utf-8"))
        for p in data["producers"]:
            if p["producer_id"] == "bot_vision_headless__screener":
                assert p["contract_class"] == "vision_context.screener.v1"
                assert p["family"] == "vision"

    def test_consumer_includes_screener(self):
        data = json.loads((self.DC_REGISTRY_DIR / "consumers.json").read_text(encoding="utf-8"))
        consumer_ids = {c["consumer_id"] for c in data["consumers"]}
        assert "desk_pro__vision_context_screener" in consumer_ids
        assert "dashboards__screener_history" in consumer_ids
