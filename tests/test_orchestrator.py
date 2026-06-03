"""Validate pipeline orchestrator: scheduling, dispatch, cooldown, market hours."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

PROFILES_DIR = Path(__file__).resolve().parent.parent / "modules" / "bot_vision" / "headless_capture"
SCRIPTS_DIR = PROFILES_DIR / "scripts"
SYSTEMD_DIR = PROFILES_DIR / "systemd"


# ── Orchestrator import ───────────────────────────────────

class TestOrchestratorImport:
    def test_import_ok(self):
        import importlib.util
        path = SCRIPTS_DIR / "schedule_orchestrator.py"
        spec = importlib.util.spec_from_file_location("schedule_orchestrator", str(path))
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"

    def test_has_main(self):
        source = (SCRIPTS_DIR / "schedule_orchestrator.py").read_text(encoding="utf-8")
        assert "def main()" in source

    def test_reads_configs(self):
        source = (SCRIPTS_DIR / "schedule_orchestrator.py").read_text(encoding="utf-8")
        assert "capture_map.json" in source
        assert "trigger_config.json" in source
        assert "screen_types.json" in source


# ── Schedule resolution ───────────────────────────────────

class TestScheduleResolution:
    def test_is_due_returns_true_for_new_profile(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from schedule_orchestrator import _is_due
        finally:
            sys.path.pop(0)

        trigger = {
            "schedules": {"every_1h": {"interval_seconds": 3600, "max_jitter_seconds": 120}},
            "screen_type_defaults": {"CHART_TECHNICAL": {"schedule": "every_1h"}},
            "asset_overrides": [],
        }
        profile = {"symbol": "BTCUSDT.P", "screen_type": "CHART_TECHNICAL", "page_id": "test_btc"}
        state = {}  # never run → due
        assert _is_due(profile, state, trigger) is True

    def test_is_due_returns_false_for_recently_run(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from schedule_orchestrator import _is_due
        finally:
            sys.path.pop(0)

        trigger = {
            "schedules": {"every_1h": {"interval_seconds": 3600, "max_jitter_seconds": 120}},
            "screen_type_defaults": {"CHART_TECHNICAL": {"schedule": "every_1h"}},
            "asset_overrides": [],
        }
        profile = {"symbol": "BTCUSDT.P", "screen_type": "CHART_TECHNICAL", "page_id": "test_btc"}
        state = {"test_btc": {"last_run_ts": time.time()}}  # just ran → not due
        assert _is_due(profile, state, trigger) is False

    def test_asset_override_takes_precedence(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from schedule_orchestrator import _schedule_key_for_profile
        finally:
            sys.path.pop(0)

        trigger = {
            "screen_type_defaults": {"CHART_TECHNICAL": {"schedule": "every_1h"}},
            "asset_overrides": [{"symbol": "BTCUSDT.P", "schedule": "every_15m"}],
        }
        profile = {"symbol": "BTCUSDT.P", "screen_type": "CHART_TECHNICAL"}
        assert _schedule_key_for_profile(profile, trigger) == "every_15m"

    def test_dry_run_does_not_execute(self):
        cmd = [sys.executable, str(SCRIPTS_DIR / "schedule_orchestrator.py"), "--dry-run"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0
        assert "DRY RUN" in result.stdout


# ── State management ──────────────────────────────────────

class TestStateManagement:
    def test_reset_state(self):
        cmd = [sys.executable, str(SCRIPTS_DIR / "schedule_orchestrator.py"), "--reset-state"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0
        assert "state reset" in result.stdout

    def test_dry_run_does_not_write_state(self, tmp_path, monkeypatch):
        import importlib.util

        path = SCRIPTS_DIR / "schedule_orchestrator.py"
        spec = importlib.util.spec_from_file_location("schedule_orchestrator", str(path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        state_path = tmp_path / "state.json"
        cooldown_path = tmp_path / "cooldown.json"
        monkeypatch.setattr(mod, "STATE_PATH", state_path)
        monkeypatch.setattr(mod, "COOLDOWN_PATH", cooldown_path)

        original_argv = sys.argv[:]
        try:
            sys.argv = ["schedule_orchestrator.py", "--dry-run", "--force-all"]
            rc = mod.main()
        finally:
            sys.argv = original_argv

        assert rc == 0
        assert not state_path.exists()
        assert not cooldown_path.exists()


# ── Profile loading ───────────────────────────────────────

class TestProfileLoading:
    def test_loads_all_profile_files(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from schedule_orchestrator import _load_all_profiles
        finally:
            sys.path.pop(0)

        profiles = _load_all_profiles()
        assert len(profiles) > 0
        symbols = {p.get("symbol") for p in profiles if p.get("symbol")}
        assert "BTCUSDT.P" in symbols


# ── Runner script ─────────────────────────────────────────

class TestRunnerScript:
    def test_runner_exists(self):
        path = SCRIPTS_DIR / "run_orchestrator.sh"
        assert path.exists()
        source = path.read_text(encoding="utf-8")
        assert "schedule_orchestrator.py" in source

    def test_runner_sets_env(self):
        path = SCRIPTS_DIR / "run_orchestrator.sh"
        source = path.read_text(encoding="utf-8")
        assert "BOT_VISION_MARKET_HOURS" in source
        assert "BOT_VISION_TMP" in source
        assert "BOT_VISION_OUT" in source


# ── Systemd units ─────────────────────────────────────────

class TestSystemdUnits:
    def test_service_exists(self):
        path = SYSTEMD_DIR / "bot-vision-orchestrator.service"
        assert path.exists()
        source = path.read_text(encoding="utf-8")
        assert "schedule_orchestrator" in source or "run_orchestrator" in source
        assert "oneshot" in source

    def test_timer_exists(self):
        path = SYSTEMD_DIR / "bot-vision-orchestrator.timer"
        assert path.exists()
        source = path.read_text(encoding="utf-8")
        assert "bot-vision-orchestrator.service" in source
        assert "OnUnitActiveSec" in source

    def test_timer_reasonable_interval(self):
        path = SYSTEMD_DIR / "bot-vision-orchestrator.timer"
        source = path.read_text(encoding="utf-8")
        # Extract interval value
        for line in source.split("\n"):
            if "OnUnitActiveSec" in line:
                val = line.split("=")[1].strip()
                assert val.endswith("min") or val.endswith("sec")
                break


# ── CLI flags ─────────────────────────────────────────────

class TestOrchestratorCLI:
    def test_help(self):
        cmd = [sys.executable, str(SCRIPTS_DIR / "schedule_orchestrator.py"), "--help"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0
        assert "--dry-run" in result.stdout
        assert "--force-all" in result.stdout
        assert "--reset-state" in result.stdout

    def test_force_all_flag(self):
        cmd = [sys.executable, str(SCRIPTS_DIR / "schedule_orchestrator.py"), "--dry-run", "--force-all"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        assert result.returncode == 0
        lines = [l for l in result.stdout.split("\n") if "CHART_TECHNICAL" in l or "LIQUIDITY" in l]
        assert len(lines) > 0  # at least one profile would be listed

    def test_once_profile(self):
        path = PROFILES_DIR / "profiles.btcusdt_poc.json"
        if path.exists():
            cmd = [sys.executable, str(SCRIPTS_DIR / "schedule_orchestrator.py"),
                   "--once", "--profile", str(path), "--dry-run"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            assert result.returncode == 0


class TestRunVisionPipelineHelpers:
    def test_build_coinglass_caption(self):
        import importlib.util

        path = SCRIPTS_DIR / "run_vision_pipeline.py"
        spec = importlib.util.spec_from_file_location("run_vision_pipeline", str(path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        payload = {
            "symbol": "BTCUSDT.P",
            "screen_type": "LIQUIDITY_COINGLASS",
            "detections": [
                {"detected_metric_type": "liquidations_long", "extracted_value": 42500000, "unit": "USD", "confidence": 0.78},
                {"detected_metric_type": "liquidation_heatmap_level", "extracted_value": 67500, "unit": "USD", "confidence": 0.82},
            ],
        }

        caption = mod._build_coinglass_caption(payload)
        assert "BTCUSDT.P" in caption
        assert "LIQUIDITY_COINGLASS" in caption
        assert "liquidations_long" in caption
        assert "42.50M" in caption

    def test_build_screener_caption(self):
        import importlib.util

        path = SCRIPTS_DIR / "run_vision_pipeline.py"
        spec = importlib.util.spec_from_file_location("run_vision_pipeline", str(path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        payload = {
            "screener_symbol": "SCREENER_AI",
            "avg_change_pct": 1.25,
            "top_gainers": [{"symbol": "NVDA", "change_pct": 2.8}],
            "top_losers": [{"symbol": "SNOW", "change_pct": -0.4}],
        }
        caption = mod._build_screener_caption(payload)
        assert "SCREENER_AI" in caption
        assert "NVDA" in caption
        assert "+2.80%" in caption

    def test_build_news_caption(self):
        import importlib.util

        path = SCRIPTS_DIR / "run_vision_pipeline.py"
        spec = importlib.util.spec_from_file_location("run_vision_pipeline", str(path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        payload = {
            "aggregate": {"sentiment_label": "positive", "average_sentiment_score": 0.65},
            "articles": [{"headline": "Bitcoin Holds Above $65K as ETF Inflows Resume"}],
        }
        caption = mod._build_news_caption(payload)
        assert "positive" in caption
        assert "+0.650" in caption
        assert "Bitcoin Holds Above" in caption
