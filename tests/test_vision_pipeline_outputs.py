"""Validate vision pipeline output schemas, formats, and contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "capture_mapping"
PROFILES_DIR = Path(__file__).resolve().parent.parent / "modules" / "bot_vision" / "headless_capture"


# ── Helpers ───────────────────────────────────────────────

def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ── Capture Metadata Schema ───────────────────────────────

class TestCaptureMetadata:
    FIXTURE = "capture_metadata_sample.json"

    def test_required_fields(self):
        data = load_fixture(self.FIXTURE)
        assert "producer" in data
        assert data["producer"] == "bot_vision_headless"
        assert "source" in data
        assert "symbol" in data
        assert "timeframe" in data
        assert "url" in data
        assert "status" in data
        assert "created_at_utc" in data
        assert "output_png" in data
        assert "output_json" in data

    def test_valid_status(self):
        data = load_fixture(self.FIXTURE)
        assert data["status"] in ("ready", "blocked", "invalid_visual")

    def test_png_path_optional_when_present_is_string(self):
        data = load_fixture(self.FIXTURE)
        if "png_path" in data:
            assert isinstance(data["png_path"], str)

    def test_valid_screen_types(self):
        data = load_fixture(self.FIXTURE)
        valid = {
            "CHART_TECHNICAL", "DASHBOARD_MACRO",
            "LIQUIDITY_COINGLASS", "FUNDING_COINGLASS",
            "OI_COINGLASS", "LS_RATIO_COINGLASS",
            "ETF_CRYPTO", "SCREENER_STOCKS", "NEWS_SENTIMENT",
        }
        assert data["screen_type"] in valid

    def test_viewport_shape(self):
        data = load_fixture(self.FIXTURE)
        vp = data.get("viewport", {})
        if vp:
            assert vp["width"] >= 1280
            assert vp["height"] >= 720


# ── Vision Analysis Schema ────────────────────────────────

class TestVisionAnalysisV1:
    FIXTURE = "vision_analysis_v1_sample.json"

    def test_required_fields(self):
        data = load_fixture(self.FIXTURE)
        assert data["input_class"] == "vision_analysis.v1"
        assert "capture_id" in data
        assert "symbol" in data
        assert "timeframe" in data
        assert "analysis_ts" in data
        assert "source_module" in data
        assert "freshness_state" in data
        assert "signals" in data

    def test_signals_structure(self):
        data = load_fixture(self.FIXTURE)
        for sig in data["signals"]:
            assert "type" in sig
            assert "value" in sig
            assert "confidence" in sig
            assert isinstance(sig["confidence"], (int, float))
            assert 0 <= sig["confidence"] <= 1.0

    def test_analysis_ts_format(self):
        data = load_fixture(self.FIXTURE)
        ts = data["analysis_ts"]
        assert ts.endswith("Z") or "+" in ts or "-" in ts[10:]

    def test_freshness_values(self):
        data = load_fixture(self.FIXTURE)
        assert data["freshness_state"] in ("fresh", "stale", "unknown")


# ── Data Center Ingest Format ─────────────────────────────

class TestDataCenterIngest:
    FIXTURE = "data_center_ingest_sample.jsonl"

    def test_jsonl_format(self):
        text = (FIXTURES_DIR / self.FIXTURE).read_text(encoding="utf-8")
        lines = [l for l in text.split("\n") if l.strip()]
        assert len(lines) >= 1
        for line in lines:
            obj = json.loads(line)
            assert "input_class" in obj
            assert obj["input_class"] == "vision_analysis.v1"
            assert "capture_id" in obj
            assert "symbol" in obj
            assert "signals" in obj

    def test_multiple_entries(self):
        text = (FIXTURES_DIR / self.FIXTURE).read_text(encoding="utf-8")
        lines = [l for l in text.split("\n") if l.strip()]
        assert len(lines) >= 2


# ── DeskPro Reader Format ─────────────────────────────────

class TestDeskProVision:
    FIXTURE = "deskpro_vision_sample.json"

    def test_reader_compatible(self):
        """Check that DeskPro's vision_analysis_reader can parse this format."""
        data = load_fixture(self.FIXTURE)
        assert data["input_class"] == "vision_analysis.v1"
        assert isinstance(data.get("signals"), list)
        # vision_analysis_reader checks input_class and returns dict
        keys_needed = {"input_class", "capture_id", "symbol"}
        assert keys_needed.issubset(data.keys())

    def test_minimal_fields_for_reader(self):
        data = load_fixture(self.FIXTURE)
        assert data["input_class"] == "vision_analysis.v1"
        # The reader only validates input_class, the rest is type-checked
        assert isinstance(data, dict)


# ── Telegram Filter Output ────────────────────────────────

class TestTelegramFilterOutput:
    FIXTURE = "telegram_summary_sample.json"

    def test_required_fields(self):
        data = load_fixture(self.FIXTURE)
        assert "send" in data
        assert "reason" in data
        assert "summary" in data
        assert "filtered_signal_count" in data

    def test_send_decision(self):
        data = load_fixture(self.FIXTURE)
        if data["send"]:
            assert data["filtered_signal_count"] > 0
        else:
            assert data["filtered_signal_count"] == 0

    def test_summary_not_empty(self):
        data = load_fixture(self.FIXTURE)
        assert len(data["summary"]) > 0

    def test_telegram_payload(self):
        data = load_fixture(self.FIXTURE)
        payload = data.get("telegram_payload", {})
        assert "message" in payload
        assert len(payload["message"]) > 0
        assert payload.get("disable_web_page_preview") is True


# ── Capture Map Registry ──────────────────────────────────

class TestCaptureMap:
    def test_exists_and_valid(self):
        path = PROFILES_DIR / "capture_map.json"
        assert path.exists(), f"capture_map.json not found at {path}"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "$schema" in data
        assert "assets" in data
        assert len(data["assets"]) > 0

    def test_asset_required_fields(self):
        path = PROFILES_DIR / "capture_map.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for asset in data["assets"]:
            assert "symbol" in asset
            assert "category" in asset
            assert "screens" in asset
            assert len(asset["screens"]) > 0

    def test_screen_types_referenced(self):
        path = PROFILES_DIR / "capture_map.json"
        reg_path = PROFILES_DIR / "screen_types.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        registry = json.loads(reg_path.read_text(encoding="utf-8"))
        valid_types = {st["id"] for st in registry["screen_types"]}
        for asset in data["assets"]:
            for screen in asset["screens"]:
                assert screen["screen_type"] in valid_types, (
                    f"Unknown screen_type '{screen['screen_type']}' in asset '{asset['symbol']}'"
                )

    def test_asset_priority_is_positive(self):
        path = PROFILES_DIR / "capture_map.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for asset in data["assets"]:
            for screen in asset["screens"]:
                prio = screen.get("priority", 5)
                assert isinstance(prio, int) and prio > 0


# ── Screen Types Registry ─────────────────────────────────

class TestScreenTypesRegistry:
    def test_exists_and_valid(self):
        path = PROFILES_DIR / "screen_types.json"
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "$schema" in data
        assert len(data["screen_types"]) > 0

    def test_each_type_has_required_fields(self):
        path = PROFILES_DIR / "screen_types.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for st in data["screen_types"]:
            assert "id" in st
            assert "label" in st
            assert "source" in st
            assert "layout" in st
            assert st["layout"] in ("single", "quad")


# ── Trigger Config ────────────────────────────────────────

class TestTriggerConfig:
    def test_exists(self):
        path = PROFILES_DIR / "trigger_config.json"
        assert path.exists()

    def test_schedule_definitions(self):
        path = PROFILES_DIR / "trigger_config.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "schedules" in data
        for sched_id, sched in data["schedules"].items():
            assert "interval_seconds" in sched
            assert sched["interval_seconds"] >= 60

    def test_screen_type_defaults(self):
        path = PROFILES_DIR / "trigger_config.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "screen_type_defaults" in data
        reg_path = PROFILES_DIR / "screen_types.json"
        registry = json.loads(reg_path.read_text(encoding="utf-8"))
        for st in registry["screen_types"]:
            assert st["id"] in data["screen_type_defaults"], (
                f"Missing default schedule for screen type '{st['id']}'"
            )


# ── Run Pipeline Script ───────────────────────────────────

class TestRunPipelineScript:
    def test_imports(self):
        import importlib.util
        path = PROFILES_DIR / "scripts" / "run_vision_pipeline.py"
        spec = importlib.util.spec_from_file_location("run_vision_pipeline", str(path))
        assert spec is not None, f"Cannot load spec from {path}"
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Module import failed: {e}"

    def test_has_main(self):
        import importlib.util
        path = PROFILES_DIR / "scripts" / "run_vision_pipeline.py"
        source = path.read_text(encoding="utf-8")
        assert "def main()" in source

    def test_has_vision_analysis_writer_ref(self):
        path = PROFILES_DIR / "scripts" / "run_vision_pipeline.py"
        source = path.read_text(encoding="utf-8")
        assert "vision_analysis_writer" in source

    def test_has_telegram_filter_ref(self):
        path = PROFILES_DIR / "scripts" / "run_vision_pipeline.py"
        source = path.read_text(encoding="utf-8")
        assert "telegram_filter" in source

    def test_has_news_sentiment_ref(self):
        path = PROFILES_DIR / "scripts" / "run_vision_pipeline.py"
        source = path.read_text(encoding="utf-8")
        assert "news_sentiment_analyzer" in source

    def test_has_signal_validator_ref(self):
        path = PROFILES_DIR / "scripts" / "run_vision_pipeline.py"
        source = path.read_text(encoding="utf-8")
        assert "signal_validator" in source

    def test_has_telegram_claim_writer_ref(self):
        path = PROFILES_DIR / "scripts" / "run_vision_pipeline.py"
        source = path.read_text(encoding="utf-8")
        assert "telegram_claim_writer" in source

    def test_resolve_png_falls_back_to_processed_dir(self, tmp_path):
        import importlib.util
        path = PROFILES_DIR / "scripts" / "run_vision_pipeline.py"
        spec = importlib.util.spec_from_file_location("run_vision_pipeline_png", str(path))
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        inbox = tmp_path / "vision_inbox"
        processed = tmp_path / "vision_processed"
        inbox.mkdir()
        processed.mkdir()
        png_name = "screen_tradingview_BTCUSDT.P_H1_2026-05-31_02-07-43.png"
        (processed / png_name).write_bytes(b"png")

        resolved = mod._resolve_png({"output_png": png_name}, inbox)
        assert resolved == str(processed / png_name)


# ── Vision Analysis Writer ────────────────────────────────

class TestVisionAnalysisWriter:
    def test_imports(self):
        import importlib.util
        path = PROFILES_DIR / "scripts" / "vision_analysis_writer.py"
        spec = importlib.util.spec_from_file_location("vision_analysis_writer", str(path))
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Module import failed: {e}"

    def test_has_extract_functions(self):
        import importlib.util
        path = PROFILES_DIR / "scripts" / "vision_analysis_writer.py"
        source = path.read_text(encoding="utf-8")
        assert "extract_signals_from_text" in source
        assert "extract_signals_from_json" in source
        assert "build_vision_analysis" in source

    def test_signal_extraction_from_text(self):
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from vision_analysis_writer import extract_signals_from_text
        finally:
            sys.path.pop(0)

        text = "Support à 65000, résistance à 68500, tendance haussier"
        signals = extract_signals_from_text(text)
        types = {s["type"] for s in signals}
        assert "support_level" in types
        assert "resistance_level" in types
        assert "trend_direction" in types

    def test_signal_extraction_from_json_block(self):
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from vision_analysis_writer import extract_signals_from_json
        finally:
            sys.path.pop(0)

        text = '''Some text before
```json
{
  "charts": [
    {"symbol": "BTCUSDT", "bias": "bullish", "supports": [65000, 64000], "resistances": [68500]}
  ]
}
```
Some text after'''
        signals = extract_signals_from_json(text)
        assert len(signals) >= 3  # 2 supports + 1 resistance
        types = {s["type"] for s in signals}
        assert "support_level" in types
        assert "resistance_level" in types


# ── Telegram Filter Script ────────────────────────────────

class TestTelegramFilterScript:
    def test_imports(self):
        import importlib.util
        path = PROFILES_DIR / "scripts" / "telegram_filter.py"
        spec = importlib.util.spec_from_file_location("telegram_filter", str(path))
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Module import failed: {e}"

    def test_filter_signals_by_confidence(self):
        import importlib.util
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from telegram_filter import filter_signals
        finally:
            sys.path.pop(0)

        summary = {
            "signals": [
                {"type": "a", "confidence": 0.90},
                {"type": "b", "confidence": 0.50},
                {"type": "c", "confidence": 0.80},
            ]
        }
        filtered = filter_signals(summary, min_confidence=0.70)
        assert len(filtered) == 2  # 0.90 and 0.80

    def test_filter_no_signals_above_threshold(self):
        import importlib.util
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from telegram_filter import filter_signals
        finally:
            sys.path.pop(0)

        summary = {
            "signals": [
                {"type": "a", "confidence": 0.50},
                {"type": "b", "confidence": 0.40},
            ]
        }
        filtered = filter_signals(summary, min_confidence=0.70)
        assert len(filtered) == 0

    def test_build_telegram_summary_sends_when_signals_found(self):
        import importlib.util
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from telegram_filter import build_telegram_summary
        finally:
            sys.path.pop(0)

        summary = {
            "run_id": "test_001",
            "analysis_text": "A) Résumé:\n- BTC haussier\nB) Support à 65000",
        }
        signals = [{"type": "support_level", "value": 65000, "confidence": 0.85}]
        result = build_telegram_summary(summary, signals, 0.70)
        assert result["send"] is True
        assert result["filtered_signal_count"] == 1


# ── Telegram Throttling ────────────────────────────────────

class TestTelegramThrottling:
    def test_signal_hash_is_deterministic(self):
        import importlib.util
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from telegram_filter import _signal_hash
        finally:
            sys.path.pop(0)

        sig = {"type": "support_level", "value": 65000, "symbol": "BTCUSDT"}
        assert _signal_hash(sig) == _signal_hash(sig)

    def test_signal_hash_differs_by_type(self):
        import importlib.util
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from telegram_filter import _signal_hash
        finally:
            sys.path.pop(0)

        sig1 = {"type": "support_level", "value": 65000, "symbol": "BTCUSDT"}
        sig2 = {"type": "resistance_level", "value": 65000, "symbol": "BTCUSDT"}
        assert _signal_hash(sig1) != _signal_hash(sig2)

    def test_signal_hash_differs_by_value(self):
        import importlib.util
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from telegram_filter import _signal_hash
        finally:
            sys.path.pop(0)

        sig1 = {"type": "support_level", "value": 65000, "symbol": "BTCUSDT"}
        sig2 = {"type": "support_level", "value": 64000, "symbol": "BTCUSDT"}
        assert _signal_hash(sig1) != _signal_hash(sig2)

    def test_filter_throttled_removes_recent(self):
        import importlib.util
        import time
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from telegram_filter import _filter_throttled, _signal_hash
        finally:
            sys.path.pop(0)

        sig = {"type": "support_level", "value": 65000, "symbol": "BTCUSDT"}
        h = _signal_hash(sig)
        state = {h: time.time()}  # just sent — still in cooldown
        allowed, skipped = _filter_throttled([sig], state, cooldown_seconds=300)
        assert len(allowed) == 0
        assert len(skipped) == 1

    def test_filter_throttled_allows_expired(self):
        import importlib.util
        import time
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from telegram_filter import _filter_throttled, _signal_hash
        finally:
            sys.path.pop(0)

        sig = {"type": "support_level", "value": 65000, "symbol": "BTCUSDT"}
        h = _signal_hash(sig)
        state = {h: time.time() - 3600}  # sent 1h ago — cooldown expired
        allowed, skipped = _filter_throttled([sig], state, cooldown_seconds=300)
        assert len(allowed) == 1
        assert len(skipped) == 0

    def test_filter_throttled_mixed(self):
        import importlib.util
        import time
        sys.path.insert(0, str(PROFILES_DIR / "scripts"))
        try:
            from telegram_filter import _filter_throttled, _signal_hash
        finally:
            sys.path.pop(0)

        sig_new = {"type": "support_level", "value": 65000, "symbol": "BTCUSDT"}
        sig_old = {"type": "resistance_level", "value": 68500, "symbol": "BTCUSDT"}
        h_new = _signal_hash(sig_new)
        h_old = _signal_hash(sig_old)
        state = {h_new: time.time(), h_old: time.time() - 3600}
        allowed, skipped = _filter_throttled([sig_new, sig_old], state, cooldown_seconds=300)
        assert len(allowed) == 1
        assert len(skipped) == 1
        assert allowed[0]["value"] == 68500  # old one allowed
