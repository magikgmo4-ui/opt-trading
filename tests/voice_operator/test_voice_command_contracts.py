"""Test that every voice command handler returns the required contract fields."""
from __future__ import annotations
import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestVoiceCommandContracts(unittest.TestCase):
    """Every /voice command must return: one_line, rich.spoken_text, rich.cards."""

    def test_handle_composite_unknown_type_returns_contract(self):
        """Unknown composite_type still returns valid contract."""
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("__unknown_test_type__")
        self.assertIn("one_line", result)
        self.assertIn("rich", result)
        self.assertTrue(result["rich"]["spoken_text"] != "" or result.get("missing"))
        self.assertIn("missing", result)
        self.assertIn("next_action", result)
        self.assertIn("generated_at", result)

    def test_handle_composite_unknown_type_has_missing_fields(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("__no_such_type_xyzzy__")
        missing = result.get("missing", [])
        self.assertIn("cards", missing)
        self.assertIn("one_line", missing)

    def test_contract_missing_is_list(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("__empty_test_type__")
        self.assertTrue(isinstance(result["missing"], list))

    def test_contract_next_action_is_list(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("__empty_test_type__")
        self.assertTrue(isinstance(result["next_action"], list))

    def test_handle_composite_market_view_contract(self):
        from modules.localcms.app.main import _handle_composite
        with patch("modules.voice_operator.engine.read_api_client.call", return_value={"ok": True, "price": 170.0}):
            with patch("modules.voice_operator.api.readers.perf_reader.read_open_trades", return_value={"open": []}):
                result = _handle_composite("market_view")
                self.assertIn("one_line", result)
                self.assertIn("rich", result)
                self.assertIn("cards", result["rich"])
                self.assertIn("spoken_text", result["rich"])
                self.assertIsInstance(result["rich"]["spoken_text"], str)
                self.assertTrue(len(result["rich"]["spoken_text"]) > 0)

    def test_all_ui_button_intents_have_handlers(self):
        """Verify the composite handler has a branch for every registered intent."""
        from modules.voice_operator.engine.intent_router import INTENT_PATTERNS
        composite_types = set()
        for _, _, endpoint, params in INTENT_PATTERNS:
            if endpoint == "/read/composite":
                composite_types.add(params.get("type", ""))
        expected = {"market_view", "btc_full", "gold_full", "spcx_full", "telegram_alerts",
                     "setups_all", "setup_detail", "score_detail", "daily_report",
                     "priorities", "attention", "exec_summary", "top_movers",
                     "watchlist_ia", "watchlist_spatial", "morning_brief"}
        for t in expected:
            self.assertIn(t, composite_types, f"Missing composite type: {t}")

    def test_contract_monitor_only_badges(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("__any_type__")
        badges = result.get("rich", {}).get("badges", [])
        self.assertIn("MONITOR-ONLY", badges)
