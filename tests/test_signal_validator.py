"""Validate cross-validation: multi-timeframe signal confirmation, dedup."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "modules" / "bot_vision" / "headless_capture" / "scripts"


# ── Import smoke ──────────────────────────────────────────

class TestSignalValidatorImport:
    def test_import_ok(self):
        import importlib.util
        path = SCRIPTS_DIR / "signal_validator.py"
        spec = importlib.util.spec_from_file_location("signal_validator", str(path))
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"

    def test_has_cross_validate_function(self):
        source = (SCRIPTS_DIR / "signal_validator.py").read_text(encoding="utf-8")
        assert "def cross_validate" in source

    def test_has_tf_order_map(self):
        source = (SCRIPTS_DIR / "signal_validator.py").read_text(encoding="utf-8")
        assert "TF_ORDER" in source
        assert "15m" in source


# ── Core logic ────────────────────────────────────────────

class TestCrossValidate:
    def test_empty_input_returns_valid_schema(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        result = cross_validate({})
        assert "validated_at" in result
        assert result["raw_signal_count"] == 0
        assert len(result["validated_signals"]) == 0

    def test_single_tf_no_dedup(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        by_tf = {
            "1h": [
                {"type": "support_level", "value": 65000, "confidence": 0.70},
                {"type": "resistance_level", "value": 68500, "confidence": 0.70},
            ]
        }
        result = cross_validate(by_tf)
        assert result["raw_signal_count"] == 2
        assert result["validated_signal_count"] == 2
        assert result["deduped_count"] == 0

    def test_duplicate_signals_deduped(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        by_tf = {
            "15m": [{"type": "support_level", "value": 65000, "confidence": 0.70}],
            "1h": [{"type": "support_level", "value": 65000, "confidence": 0.72}],
        }
        result = cross_validate(by_tf)
        assert result["raw_signal_count"] == 2
        assert result["validated_signal_count"] == 1  # deduped
        assert result["deduped_count"] == 1

    def test_multi_tf_confirms_with_boost(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        by_tf = {
            "15m": [{"type": "support_level", "value": 65000, "confidence": 0.70}],
            "1h": [{"type": "support_level", "value": 65000, "confidence": 0.72}],
        }
        result = cross_validate(by_tf)
        assert result["confirmed_count"] >= 1
        validated_sig = result["validated_signals"][0]
        assert validated_sig["confidence"] >= 0.70
        assert validated_sig.get("cross_validated") is True
        assert len(validated_sig.get("confirmed_by_timeframes", [])) >= 2

    def test_multi_tf_higher_weight_boost(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        by_tf = {
            "15m": [{"type": "support_level", "value": 65000, "confidence": 0.70}],
            "4h": [{"type": "support_level", "value": 65000, "confidence": 0.75}],
        }
        result = cross_validate(by_tf)
        validated_sig = result["validated_signals"][0]
        assert validated_sig["cross_validated"] is True

    def test_different_values_not_deduped(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        by_tf = {
            "15m": [{"type": "support_level", "value": 65000, "confidence": 0.70}],
            "1h": [{"type": "support_level", "value": 63000, "confidence": 0.72}],
        }
        result = cross_validate(by_tf)
        assert result["validated_signal_count"] == 2
        assert result["deduped_count"] == 0

    def test_signal_with_string_value_not_deduped_wrongly(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        by_tf = {
            "15m": [{"type": "trend_direction", "value": "bullish", "confidence": 0.65}],
            "1h": [{"type": "trend_direction", "value": "bullish", "confidence": 0.70}],
        }
        result = cross_validate(by_tf)
        assert result["validated_signal_count"] == 1
        assert result["deduped_count"] == 1

    def test_output_sorted_by_confidence(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        by_tf = {
            "1h": [
                {"type": "support_level", "value": 65000, "confidence": 0.70},
                {"type": "resistance_level", "value": 68500, "confidence": 0.80},
                {"type": "key_level", "value": 66000, "confidence": 0.60},
            ]
        }
        result = cross_validate(by_tf)
        confidences = [s["confidence"] for s in result["validated_signals"]]
        assert confidences == sorted(confidences, reverse=True)

    def test_three_timeframes_gives_better_boost(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        by_tf_2 = {
            "15m": [{"type": "support_level", "value": 65000, "confidence": 0.70}],
            "1h": [{"type": "support_level", "value": 65000, "confidence": 0.72}],
        }
        by_tf_3 = {
            "15m": [{"type": "support_level", "value": 65000, "confidence": 0.70}],
            "1h": [{"type": "support_level", "value": 65000, "confidence": 0.72}],
            "4h": [{"type": "support_level", "value": 65000, "confidence": 0.75}],
        }
        r2 = cross_validate(by_tf_2)
        r3 = cross_validate(by_tf_3)
        c2 = r2["validated_signals"][0]["confidence"]
        c3 = r3["validated_signals"][0]["confidence"]
        assert c3 >= c2, "3-TF should have >= confidence than 2-TF"


# ── CLI smoke ─────────────────────────────────────────────

class TestSignalValidatorCLI:
    def test_stdin_pipe(self):
        data = json.dumps({
            "symbol": "BTCUSDT",
            "timeframe": "1h",
            "signals": [
                {"type": "support_level", "value": 65000, "confidence": 0.70},
                {"type": "resistance_level", "value": 68500, "confidence": 0.80},
            ]
        })
        cmd = [sys.executable, str(SCRIPTS_DIR / "signal_validator.py"), "--stdin"]
        result = subprocess.run(cmd, input=data, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0
        output = json.loads(result.stdout.strip())
        assert "validated_signals" in output
        assert output["raw_signal_count"] == 2

    def test_help(self):
        cmd = [sys.executable, str(SCRIPTS_DIR / "signal_validator.py"), "--help"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert result.returncode == 0
        assert "--symbol" in result.stdout
        assert "--stdin" in result.stdout


# ── Edge cases ────────────────────────────────────────────

class TestSignalValidatorEdgeCases:
    def test_non_numeric_values_handled(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        by_tf = {
            "1h": [
                {"type": "trend_direction", "value": "bullish", "confidence": 0.65},
                {"type": "analysis_note", "value": "Strong momentum", "confidence": 0.60},
            ]
        }
        result = cross_validate(by_tf)
        assert result["validated_signal_count"] == 2
        assert result["deduped_count"] == 0

    def test_confidence_capped_at_0_98(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from signal_validator import cross_validate
        finally:
            sys.path.pop(0)

        by_tf = {
            "15m": [{"type": "support_level", "value": 65000, "confidence": 0.90}],
            "1h": [{"type": "support_level", "value": 65000, "confidence": 0.92}],
            "4h": [{"type": "support_level", "value": 65000, "confidence": 0.95}],
            "1d": [{"type": "support_level", "value": 65000, "confidence": 0.95}],
        }
        result = cross_validate(by_tf)
        for sig in result["validated_signals"]:
            assert sig["confidence"] <= 1.0
            assert sig["confidence"] <= 0.98
