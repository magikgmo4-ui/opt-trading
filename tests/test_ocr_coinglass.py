"""Validate Coinglass OCR analyzer, vision_context_writer, and integration."""

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


# ── OCR Analyzer import smoke ─────────────────────────────

class TestCoinglassOCRAnalyzerImport:
    def test_import_ok(self):
        import importlib.util
        path = SCRIPTS_DIR / "coinglass_ocr_analyzer.py"
        spec = importlib.util.spec_from_file_location("coinglass_ocr_analyzer", str(path))
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"

    def test_has_analyze_function(self):
        path = SCRIPTS_DIR / "coinglass_ocr_analyzer.py"
        source = path.read_text(encoding="utf-8")
        assert "def analyze" in source

    def test_valid_screen_types(self):
        path = SCRIPTS_DIR / "coinglass_ocr_analyzer.py"
        source = path.read_text(encoding="utf-8")
        for st in ["LIQUIDITY_COINGLASS", "FUNDING_COINGLASS", "OI_COINGLASS", "LS_RATIO_COINGLASS"]:
            assert st in source


# ── Stub mode output ──────────────────────────────────────

class TestCoinglassOCRAnalyzerStub:
    def test_analyze_returns_valid_schema(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from coinglass_ocr_analyzer import analyze
        finally:
            sys.path.pop(0)

        sidecar = {
            "screen_type": "LIQUIDITY_COINGLASS",
            "symbol": "BTCUSDT.P",
            "source": "coinglass",
            "created_at_utc": "2026-05-30T12:00:00Z",
        }
        result = analyze(sidecar, use_real_ocr=False)
        assert result["input_class"] == "vision_context.coinglass.v1"
        assert result["symbol"] == "BTCUSDT.P"
        assert len(result["detections"]) > 0

    def test_stub_detections_have_required_fields(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from coinglass_ocr_analyzer import analyze
        finally:
            sys.path.pop(0)

        for st in ["LIQUIDITY_COINGLASS", "FUNDING_COINGLASS", "OI_COINGLASS", "LS_RATIO_COINGLASS"]:
            sidecar = {"screen_type": st, "symbol": "BTCUSDT.P", "source": "coinglass"}
            result = analyze(sidecar)
            for det in result["detections"]:
                assert "extracted_value" in det
                assert "detected_metric_type" in det
                assert "confidence" in det
                assert isinstance(det["confidence"], (int, float))
                assert 0 <= det["confidence"] <= 1.0

    def test_stub_values_vary_by_symbol(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from coinglass_ocr_analyzer import analyze
        finally:
            sys.path.pop(0)

        btc = analyze({"screen_type": "LIQUIDITY_COINGLASS", "symbol": "BTCUSDT.P", "source": "coinglass"})
        eth = analyze({"screen_type": "LIQUIDITY_COINGLASS", "symbol": "ETHUSDT.P", "source": "coinglass"})
        btc_val = btc["detections"][0]["extracted_value"]
        eth_val = eth["detections"][0]["extracted_value"]
        assert btc_val != eth_val, "Stub values should differ by symbol"

    def test_analyze_pipe_via_stdin(self):
        sidecar = json.dumps({"screen_type": "LIQUIDITY_COINGLASS", "symbol": "BTCUSDT.P", "source": "coinglass"})
        cmd = [sys.executable, str(SCRIPTS_DIR / "coinglass_ocr_analyzer.py"), "--stdin"]
        result = subprocess.run(cmd, input=sidecar, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        assert data["input_class"] == "vision_context.coinglass.v1"
        assert len(data["detections"]) > 0


class TestCoinglassOCRRuntimePath:
    def test_parse_numeric_token_handles_suffixes(self):
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from coinglass_ocr_analyzer import _parse_numeric_token
        finally:
            sys.path.pop(0)

        assert _parse_numeric_token("42.5M") == 42_500_000.0
        assert _parse_numeric_token("1.2B") == 1_200_000_000.0
        assert _parse_numeric_token("67.5K") == 67_500.0
        assert _parse_numeric_token("0.12%") == 0.12

    def test_extract_with_ocr_text_liquidity(self):
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from coinglass_ocr_analyzer import _extract_with_ocr_text
        finally:
            sys.path.pop(0)

        detections = _extract_with_ocr_text("Long 42.5M Short 38.2M Heatmap 67.5K", "LIQUIDITY_COINGLASS")
        assert len(detections) >= 2
        assert detections[0]["detected_metric_type"] == "liquidations_long"
        assert detections[1]["detected_metric_type"] == "liquidations_short"

    def test_extract_with_ocr_text_funding(self):
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from coinglass_ocr_analyzer import _extract_with_ocr_text
        finally:
            sys.path.pop(0)

        detections = _extract_with_ocr_text("Binance +0.012% Bybit -0.008%", "FUNDING_COINGLASS")
        assert len(detections) >= 2
        assert all(det["detected_metric_type"] == "funding_rate" for det in detections)

    def test_extract_with_ocr_text_oi(self):
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from coinglass_ocr_analyzer import _extract_with_ocr_text
        finally:
            sys.path.pop(0)

        detections = _extract_with_ocr_text("OI 72.1B Change 1.2B", "OI_COINGLASS")
        assert len(detections) >= 2
        assert detections[0]["detected_metric_type"] == "open_interest"

    def test_extract_with_ocr_text_ls_ratio(self):
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from coinglass_ocr_analyzer import _extract_with_ocr_text
        finally:
            sys.path.pop(0)

        detections = _extract_with_ocr_text("Binance 1.25 OKX 1.18", "LS_RATIO_COINGLASS")
        assert len(detections) >= 2
        assert all(det["detected_metric_type"] == "long_short_ratio" for det in detections)

    def test_real_ocr_fallback_reports_stub_method(self, monkeypatch, tmp_path):
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            import coinglass_ocr_analyzer as mod
        finally:
            sys.path.pop(0)

        png = tmp_path / "cg.png"
        png.write_bytes(b"fake")
        monkeypatch.setattr(mod, "_extract_with_ocr", lambda image_path, screen_type: [])

        result = mod.analyze(
            {
                "screen_type": "LIQUIDITY_COINGLASS",
                "symbol": "BTCUSDT.P",
                "source": "coinglass",
                "png_path": str(png),
            },
            use_real_ocr=True,
        )
        assert result["detection_method"] == "stub"
        assert "real_ocr_requested_but_no_metrics_extracted" in result["warnings"]
        assert result["refs"]["requested_real_ocr"] is True

    def test_real_ocr_success_reports_ocr_method(self, monkeypatch, tmp_path):
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            import coinglass_ocr_analyzer as mod
        finally:
            sys.path.pop(0)

        png = tmp_path / "cg.png"
        png.write_bytes(b"fake")
        monkeypatch.setattr(
            mod,
            "_extract_with_ocr",
            lambda image_path, screen_type: [{
                "extracted_value": 42_500_000.0,
                "detected_metric_type": "liquidations_long",
                "confidence": 0.61,
                "detection_method": "ocr_raw",
                "unit": "USD",
            }],
        )

        result = mod.analyze(
            {
                "screen_type": "LIQUIDITY_COINGLASS",
                "symbol": "BTCUSDT.P",
                "source": "coinglass",
                "png_path": str(png),
            },
            use_real_ocr=True,
        )
        assert result["detection_method"] == "ocr_real"
        assert result["detections"][0]["detected_metric_type"] == "liquidations_long"
        assert result["warnings"] == []

    def test_real_ocr_missing_png_adds_warning(self):
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            import coinglass_ocr_analyzer as mod
        finally:
            sys.path.pop(0)

        result = mod.analyze(
            {
                "screen_type": "LIQUIDITY_COINGLASS",
                "symbol": "BTCUSDT.P",
                "source": "coinglass",
                "png_path": "/does/not/exist.png",
            },
            use_real_ocr=True,
        )
        assert result["detection_method"] == "stub"
        assert "real_ocr_requested_but_image_missing" in result["warnings"]


# ── Vision Context Writer ─────────────────────────────────

class TestVisionContextWriter:
    def test_import_ok(self):
        import importlib.util
        path = SCRIPTS_DIR / "vision_context_writer.py"
        spec = importlib.util.spec_from_file_location("vision_context_writer", str(path))
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
            from vision_context_writer import validate
        finally:
            sys.path.pop(0)

        assert validate({"input_class": "wrong"}) is False
        assert validate({"input_class": "vision_context.coinglass.v1", "detections": []}) is True

    def test_pipe_via_stdin(self):
        data = load_fixture("vision_context_coinglass_v1_sample.json")
        cmd = [sys.executable, str(SCRIPTS_DIR / "vision_context_writer.py"), "--dry-run", "--stdin"]
        result = subprocess.run(cmd, input=json.dumps(data), capture_output=True, text=True, timeout=15)
        assert result.returncode == 0


# ── Fixture validation ────────────────────────────────────

class TestCoinglassFixture:
    FIXTURE = "vision_context_coinglass_v1_sample.json"

    def test_required_fields(self):
        data = load_fixture(self.FIXTURE)
        assert data["input_class"] == "vision_context.coinglass.v1"
        assert "symbol" in data
        assert "source_id" in data
        assert "freshness_state" in data
        assert "detections" in data

    def test_detection_structure(self):
        data = load_fixture(self.FIXTURE)
        for det in data["detections"]:
            assert "extracted_value" in det
            assert "detected_metric_type" in det
            assert "confidence" in det
            assert "unit" in det

    def test_known_metric_types(self):
        data = load_fixture(self.FIXTURE)
        valid_types = {
            "liquidations_long", "liquidations_short", "long_short_ratio",
            "open_interest", "liquidation_heatmap_level", "funding_rate",
        }
        for det in data["detections"]:
            assert det["detected_metric_type"] in valid_types, f"Unknown metric type: {det['detected_metric_type']}"


# ── Pipeline integration ──────────────────────────────────

class TestPipelineIntegration:
    def test_has_coinglass_ocr_ref(self):
        path = SCRIPTS_DIR / "run_vision_pipeline.py"
        source = path.read_text(encoding="utf-8")
        assert "coinglass_ocr_analyzer" in source
        assert "vision_context_writer" in source

    def test_has_ocr_dispatch(self):
        path = SCRIPTS_DIR / "run_vision_pipeline.py"
        source = path.read_text(encoding="utf-8")
        assert "Coinglass OCR analyzer" in source
        assert "vision_context.coinglass.v1" in source

    def test_has_real_ocr_flag(self):
        path = SCRIPTS_DIR / "run_vision_pipeline.py"
        source = path.read_text(encoding="utf-8")
        assert "--real-ocr" in source

    def test_import_ok(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "run_vision_pipeline_ocr",
            str(SCRIPTS_DIR / "run_vision_pipeline.py"),
        )
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"
