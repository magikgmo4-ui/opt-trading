"""Test that missing[] correctly indicates when data is absent vs response is poor."""
from __future__ import annotations
import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestVoiceMissingFields(unittest.TestCase):
    """missing[] must differentiate: absent data vs poor response."""

    def test_composite_returns_missing_when_no_cards(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("__empty_test_type__")
        self.assertIn("missing", result)
        self.assertIn("cards", result["missing"])
        self.assertIn("one_line", result["missing"])

    def test_composite_returns_empty_missing_when_data_present(self):
        from modules.localcms.app.main import _handle_composite
        with patch("modules.voice_operator.engine.read_api_client.call", return_value={"ok": True, "price": 170.0}):
            with patch("modules.voice_operator.api.readers.perf_reader.read_open_trades", return_value={"open": []}):
                result = _handle_composite("market_view")
                missing = result.get("missing", [])
                cards = result.get("rich", {}).get("cards", [])
                spoken = result.get("rich", {}).get("spoken_text", "")
                if cards and spoken:
                    self.assertEqual(missing, [],
                                     f"Should have no missing when cards+spoken present, got {missing}")

    def test_missing_structure_is_list_of_strings(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("__empty_test_type__")
        missing = result.get("missing", [])
        self.assertIsInstance(missing, list)
        for item in missing:
            self.assertIsInstance(item, str, f"missing item should be string, got {type(item)}")

    def test_next_action_structure_is_list_of_strings(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("__empty_test_type__")
        next_action = result.get("next_action", [])
        self.assertIsInstance(next_action, list)
        for item in next_action:
            self.assertIsInstance(item, str, f"next_action item should be string, got {type(item)}")

    def test_setup_detail_missing_when_no_match(self):
        from modules.localcms.app.main import _handle_composite
        with patch("modules.voice_operator.engine.read_api_client.call", return_value={"active": 0, "items": [], "a_plus": 0}):
            result = _handle_composite("setup_detail", {"symbol": "XXX", "type": "setup_detail"})
            self.assertIn("missing", result)
            self.assertIn("one_line", result)
            self.assertIn("rich", result)
            # When source has no data, we show a status card — not empty
            cards = result.get("rich", {}).get("cards", [])
            self.assertGreater(len(cards), 0, f"Should have at least a status card when no setup data, got {cards}")

    def test_score_detail_handles_missing_true_value(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("score_detail", {"symbol": "UNKNOWN", "type": "score_detail"})
        self.assertIn("missing", result)
        self.assertIn("one_line", result)
        self.assertTrue(isinstance(result["missing"], list))

    def test_system_status_includes_dc_contracts(self):
        from modules.voice_operator.api.routes import read_system
        with patch("modules.voice_operator.api.routes.deskpro_reader.read_status", return_value={"ok": True}):
            with patch("modules.voice_operator.api.routes.perf_reader.read_summary", return_value={"total": 0}):
                with patch("modules.voice_operator.api.routes.localcms_reader.read_menu_state", return_value={"ok": True}):
                    with patch("modules.voice_operator.api.routes.memory_reader.read_status", return_value={"ok": True}):
                        with patch("modules.voice_operator.api.routes.deskpro_reader.read_alerts", return_value={"alerts": []}):
                            result = read_system()
                            self.assertIn("data_center_contracts", result)
                            self.assertIn("data_center_status", result)

    def test_read_score_handles_btc(self):
        from modules.voice_operator.api.routes import read_score
        result = read_score(symbol="BTC")
        self.assertIn("symbol", result)
        self.assertIn("one_line", result)
        self.assertIn("generated_at", result)

    def test_read_score_handles_xauusd(self):
        from modules.voice_operator.api.routes import read_score
        result = read_score(symbol="XAUUSD")
        self.assertIn("symbol", result)
        self.assertIn("one_line", result)
        self.assertIn("generated_at", result)
