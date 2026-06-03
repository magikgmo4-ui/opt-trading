"""Validate gaps-fill implementation: Telegram integration, market hours, profiles."""

from __future__ import annotations

import json
import importlib.util
from pathlib import Path

PROFILES_DIR = Path(__file__).resolve().parent.parent / "modules" / "bot_vision" / "headless_capture"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ── Supplementary Profiles ────────────────────────────────

class TestSupplementaryProfiles:
    PROFILE_FILE = PROFILES_DIR / "profiles.supplementary.json"

    def test_exists(self):
        assert self.PROFILE_FILE.exists()

    def test_valid_json(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        assert isinstance(data, list)
        assert len(data) > 0

    def test_contains_total(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        symbols = {p.get("symbol") for p in data}
        assert "CRYPTOCAP:TOTAL" in symbols

    def test_contains_btcd(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        symbols = {p.get("symbol") for p in data}
        assert "CRYPTOCAP:BTC.D" in symbols

    def test_contains_fbtc(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        symbols = {p.get("symbol") for p in data}
        assert "NASDAQ:FBTC" in symbols

    def test_contains_gbtc(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        symbols = {p.get("symbol") for p in data}
        assert "OTC:GBTC" in symbols or "GBTC" in symbols

    def test_contains_bitb(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        symbols = {p.get("symbol") for p in data}
        assert "NASDAQ:BITB" in symbols

    def test_contains_arkb(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        symbols = {p.get("symbol") for p in data}
        assert "NASDAQ:ARKB" in symbols

    def test_contains_brent(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        symbols = {p.get("symbol") for p in data}
        assert "BITGET:BZUSDT" in symbols

    def test_required_fields_per_entry(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        for entry in data:
            assert "source" in entry
            assert "symbol" in entry
            assert "timeframe" in entry
            assert "screen_type" in entry
            assert "url" in entry
            assert "layout" in entry

    def test_no_duplicate_page_ids(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        ids = [p.get("page_id") for p in data if p.get("page_id")]
        assert len(ids) == len(set(ids)), f"Duplicate page_ids: {ids}"


# ── Market Hours in capture_headless.js ───────────────────

class TestMarketHoursImplementation:
    JS_PATH = PROFILES_DIR / "capture_headless.js"

    def test_market_hours_enabled_flag(self):
        source = self.JS_PATH.read_text(encoding="utf-8")
        assert "MARKET_HOURS_ENABLED" in source

    def test_market_hours_function(self):
        source = self.JS_PATH.read_text(encoding="utf-8")
        assert "function isInMarketHours" in source

    def test_market_hours_map(self):
        source = self.JS_PATH.read_text(encoding="utf-8")
        assert "MARKET_HOURS_MAP" in source
        assert "us_market" in source
        assert "24h" in source
        assert "forex" in source

    def test_us_market_rule(self):
        source = self.JS_PATH.read_text(encoding="utf-8")
        assert "us_market" in source
        assert "9.5" in source  # 09:30 start
        assert "16" in source   # 16:00 end

    def test_crypto_assets_24h(self):
        source = self.JS_PATH.read_text(encoding="utf-8")
        assert "USDT" in source
        assert "BZUSDT" in source
        assert "BITGET:BZUSDT" in source

    def test_skipped_outside_hours(self):
        source = self.JS_PATH.read_text(encoding="utf-8")
        assert "OUTSIDE_MARKET_HOURS" in source

    def test_env_disable(self):
        source = self.JS_PATH.read_text(encoding="utf-8")
        assert "BOT_VISION_MARKET_HOURS" in source


# ── Telegram Integration in run_vision_pipeline.py ────────

class TestTelegramIntegration:
    SCRIPT_PATH = PROFILES_DIR / "scripts" / "run_vision_pipeline.py"

    def test_telegram_flag(self):
        source = self.SCRIPT_PATH.read_text(encoding="utf-8")
        assert "--no-telegram" in source

    def test_telegram_threshold_flag(self):
        source = self.SCRIPT_PATH.read_text(encoding="utf-8")
        assert "--telegram-threshold" in source

    def test_telegram_send_call(self):
        source = self.SCRIPT_PATH.read_text(encoding="utf-8")
        assert "send_to_channel" in source or "send_photo_to_channel" in source
        assert "shared.telegram_channels" in source

    def test_telegram_decision_based_on_filter(self):
        source = self.SCRIPT_PATH.read_text(encoding="utf-8")
        assert "tg_data.get" in source
        assert "should_send" in source

    def test_telegram_not_no_telegram_flag(self):
        source = self.SCRIPT_PATH.read_text(encoding="utf-8")
        assert "no_telegram" in source


# ── Run script import smoke test ──────────────────────────

class TestPipelineScriptImport:
    def test_import_ok(self):
        path = PROFILES_DIR / "scripts" / "run_vision_pipeline.py"
        spec = importlib.util.spec_from_file_location("gaps_run_vision_pipeline", str(path))
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"

    def test_market_hours_env_var_documented(self):
        path = PROFILES_DIR / "capture_headless.js"
        source = path.read_text(encoding="utf-8")
        assert "MARKET_HOURS_ENABLED" in source
        assert "BOT_VISION_MARKET_HOURS" in source


# ── Capture Map version check ─────────────────────────────

class TestCaptureMapUpdated:
    def test_version_bumped(self):
        path = PROFILES_DIR / "capture_map.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["version"] >= "1.1.0"

    def test_has_all_required_assets(self):
        path = PROFILES_DIR / "capture_map.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        symbols = {a["symbol"] for a in data["assets"]}
        required = {"TOTAL", "TOTAL2", "TOTAL3", "BTC.D", "NASDAQ:FBTC", "GBTC", "BITB", "ARKB", "BITGET:BZUSDT", "NYMEX:RB1!"}
        missing = required - symbols
        assert not missing, f"Missing assets in capture_map: {missing}"


# ── Remaining screener profiles ───────────────────────────

class TestRemainingScreeners:
    PROFILE_FILE = PROFILES_DIR / "profiles.supplementary.json"

    def test_all_screeners_present(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        screener_symbols = {p.get("symbol") for p in data if p.get("screen_type") == "SCREENER_STOCKS"}
        expected = {"SCREENER_BIGGEST_CAPS", "SCREENER_TRENDING", "SCREENER_AI",
                    "SCREENER_DEFENSE", "SCREENER_SPATIAL", "SCREENER_CRYPTO_STOCKS", "SCREENER_ENERGY"}
        missing = expected - screener_symbols
        assert not missing, f"Missing screener profiles: {missing}"

    def test_rb1_essence_present(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        symbols = {p.get("symbol") for p in data}
        assert "NYMEX:RB1!" in symbols

    def test_screener_required_fields(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        for entry in data:
            if entry.get("screen_type") == "SCREENER_STOCKS":
                assert entry.get("source") == "tradingview_screener"
                assert "url" in entry
                assert entry.get("page_id", "").startswith("tv_screener_")
                assert entry.get("quality_retry_enabled") is True
                assert entry.get("quality_retry_extra_wait_ms", 0) >= 20000

    def test_no_duplicate_screener_page_ids(self):
        data = json.loads(self.PROFILE_FILE.read_text(encoding="utf-8"))
        screener_ids = [p.get("page_id") for p in data if p.get("screen_type") == "SCREENER_STOCKS"]
        assert len(screener_ids) == len(set(screener_ids)), f"Duplicate screener page_ids: {screener_ids}"


# ── Data Center Registry ──────────────────────────────────

class TestDataCenterRegistry:
    DC_REGISTRY_DIR = Path(__file__).resolve().parent.parent / "modules" / "data_center" / "registry"

    def test_producers_include_bot_vision(self):
        data = json.loads((self.DC_REGISTRY_DIR / "producers.json").read_text(encoding="utf-8"))
        producer_ids = {p["producer_id"] for p in data["producers"]}
        assert "bot_vision_headless" in producer_ids
        assert "bot_vision_headless__coinglass" in producer_ids

    def test_consumers_include_vision_analysis(self):
        data = json.loads((self.DC_REGISTRY_DIR / "consumers.json").read_text(encoding="utf-8"))
        consumer_ids = {c["consumer_id"] for c in data["consumers"]}
        assert "desk_pro__vision_analysis" in consumer_ids
        assert "desk_pro__vision_context_coinglass" in consumer_ids
        assert "dashboards__vision_analysis_history" in consumer_ids

    def test_producer_contracts_correct(self):
        data = json.loads((self.DC_REGISTRY_DIR / "producers.json").read_text(encoding="utf-8"))
        for p in data["producers"]:
            if p["producer_id"] == "bot_vision_headless":
                assert p["contract_class"] == "vision_analysis.v1"
            if p["producer_id"] == "bot_vision_headless__coinglass":
                assert p["contract_class"] == "vision_context.coinglass.v1"


class TestQualityStrategy:
    DC_REGISTRY_DIR = Path(__file__).resolve().parent.parent / "modules" / "data_center" / "registry"

    def test_capture_map_declares_improve_before_reject(self):
        path = PROFILES_DIR / "capture_map.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["quality_strategy"]["principle"] == "improve_before_reject"

    def test_producer_family_vision(self):
        data = json.loads((self.DC_REGISTRY_DIR / "producers.json").read_text(encoding="utf-8"))
        for p in data["producers"]:
            if "bot_vision" in p["producer_id"]:
                assert p["family"] == "vision"
