from __future__ import annotations

"""Unit tests for the Voice Operator dispatcher.

Tests command routing and intent matching.
read_spcx_score() is mocked — no file I/O, no live API calls.
"""

import unittest
from unittest.mock import patch, MagicMock

from modules.desk_pro.service.voice_operator import dispatch_command

# ---------------------------------------------------------------------------
# Mock score result (realistic, matches score_spcx() contract)
# ---------------------------------------------------------------------------

_MOCK_SCORE = {
    "symbol": "SPCX",
    "score": 60,
    "grade": "A",
    "events": ["VWAP_RECLAIM", "ORB_HIGH_BREAK", "SPACEX_WIRE"],
    "bias": "bullish",
    "setup_state": "active",
    "levels": {"price": 173.77, "vwap": 164.74, "orb_high": 168.75, "orb_low": None},
    "risk_notes": ["extended_above_vwap"],
    "invalidation": {
        "vwap_loss": {"level": 164.74, "note": "price closes below VWAP"},
        "orb_loss": {"level": 168.75, "note": "price recedes below ORB high"},
    },
    "monitor_only": True,
    "data_source": {"cdp_events": 2, "wire_events": 1, "total_input_events": 3},
}

_EMPTY_SCORE = {
    "symbol": "SPCX",
    "score": 0,
    "grade": "C",
    "events": [],
    "bias": "neutral",
    "setup_state": "watch",
    "levels": {"price": None, "vwap": None, "orb_high": None, "orb_low": None},
    "risk_notes": [],
    "invalidation": {},
    "monitor_only": True,
    "data_source": {"cdp_events": 0, "wire_events": 0, "total_input_events": 0},
}

# read_spcx_score is imported at module level in voice_operator.py,
# so we patch the name as it exists in the voice_operator namespace.
_PATCH = "modules.desk_pro.service.voice_operator.read_spcx_score"


# ---------------------------------------------------------------------------
# 1. Intent routing
# ---------------------------------------------------------------------------

class TestIntentRouting(unittest.TestCase):
    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_score_spcx_lowercase(self, _):
        result = dispatch_command("score spcx")
        self.assertTrue(result["matched"])
        self.assertEqual(result["intent"], "spcx_score")

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_score_spcx_uppercase(self, _):
        result = dispatch_command("SCORE SPCX")
        self.assertTrue(result["matched"])
        self.assertEqual(result["intent"], "spcx_score")

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_spcx_score_reversed_order(self, _):
        result = dispatch_command("spcx score")
        self.assertTrue(result["matched"])
        self.assertEqual(result["intent"], "spcx_score")

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_spcx_alone(self, _):
        result = dispatch_command("spcx")
        self.assertTrue(result["matched"])
        self.assertEqual(result["intent"], "spcx_score")

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_score_spacex_variant(self, _):
        result = dispatch_command("score spacex")
        self.assertTrue(result["matched"])
        self.assertEqual(result["intent"], "spcx_score")

    def test_help_keyword(self):
        result = dispatch_command("help")
        self.assertTrue(result["matched"])
        self.assertEqual(result["intent"], "help")

    def test_question_mark(self):
        result = dispatch_command("?")
        self.assertTrue(result["matched"])
        self.assertEqual(result["intent"], "help")

    def test_unknown_command(self):
        result = dispatch_command("buy 100 shares")
        self.assertFalse(result["matched"])
        self.assertEqual(result["intent"], "unknown")

    def test_empty_string(self):
        result = dispatch_command("")
        self.assertFalse(result["matched"])
        self.assertEqual(result["intent"], "empty")

    def test_whitespace_only(self):
        result = dispatch_command("   ")
        self.assertFalse(result["matched"])
        self.assertEqual(result["intent"], "empty")


# ---------------------------------------------------------------------------
# 2. Output structure
# ---------------------------------------------------------------------------

class TestOutputStructure(unittest.TestCase):
    _REQUIRED = {"matched", "intent", "response", "data"}

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_spcx_result_has_all_keys(self, _):
        result = dispatch_command("score spcx")
        self.assertEqual(result.keys(), self._REQUIRED)

    def test_help_result_has_all_keys(self):
        result = dispatch_command("help")
        self.assertEqual(result.keys(), self._REQUIRED)

    def test_unknown_result_has_all_keys(self):
        result = dispatch_command("random thing")
        self.assertEqual(result.keys(), self._REQUIRED)

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_spcx_data_is_score_dict(self, _):
        result = dispatch_command("spcx")
        self.assertIsInstance(result["data"], dict)
        self.assertIn("score", result["data"])
        self.assertIn("grade", result["data"])
        self.assertIn("monitor_only", result["data"])

    def test_help_data_is_empty_dict(self):
        result = dispatch_command("help")
        self.assertEqual(result["data"], {})

    def test_unknown_data_is_empty_dict(self):
        result = dispatch_command("xyz")
        self.assertEqual(result["data"], {})


# ---------------------------------------------------------------------------
# 3. Response text content
# ---------------------------------------------------------------------------

class TestResponseText(unittest.TestCase):
    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_spcx_response_contains_grade(self, _):
        result = dispatch_command("score spcx")
        self.assertIn("A", result["response"])

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_spcx_response_contains_score(self, _):
        result = dispatch_command("score spcx")
        self.assertIn("60", result["response"])

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_spcx_response_contains_state(self, _):
        result = dispatch_command("score spcx")
        self.assertIn("ACTIVE", result["response"])

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_spcx_response_contains_monitor_only(self, _):
        result = dispatch_command("score spcx")
        self.assertIn("monitor_only", result["response"])

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_spcx_response_contains_price(self, _):
        result = dispatch_command("score spcx")
        self.assertIn("173.77", result["response"])

    def test_help_response_contains_score_spcx(self):
        result = dispatch_command("help")
        self.assertIn("score spcx", result["response"].lower())

    def test_unknown_response_mentions_help(self):
        result = dispatch_command("some garbage")
        self.assertIn("help", result["response"].lower())

    @patch(_PATCH, return_value=_EMPTY_SCORE)
    def test_empty_score_response_shows_grade_c(self, _):
        result = dispatch_command("spcx")
        self.assertIn("C", result["response"])


# ---------------------------------------------------------------------------
# 4. Scorer called exactly once per SPCX command
# ---------------------------------------------------------------------------

class TestScorerCallCount(unittest.TestCase):
    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_scorer_called_once(self, mock_reader):
        dispatch_command("score spcx")
        mock_reader.assert_called_once()

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_scorer_not_called_for_help(self, mock_reader):
        dispatch_command("help")
        mock_reader.assert_not_called()

    @patch(_PATCH, return_value=_MOCK_SCORE)
    def test_scorer_not_called_for_unknown(self, mock_reader):
        dispatch_command("buy bitcoin")
        mock_reader.assert_not_called()


# ---------------------------------------------------------------------------
# 5. UI HTML sanity checks
# ---------------------------------------------------------------------------

class TestUIHtml(unittest.TestCase):
    """Verify page.py contains the SPCX and Voice Operator sections."""

    @classmethod
    def setUpClass(cls):
        from modules.desk_pro.ui.page import render_ui_html
        cls.html = render_ui_html()

    def test_spcx_panel_present(self):
        self.assertIn("spcxPanel", self.html)

    def test_spcx_score_endpoint_referenced(self):
        self.assertIn("/desk/spacex/score", self.html)

    def test_voice_panel_present(self):
        self.assertIn("voicePanel", self.html)

    def test_voice_endpoint_referenced(self):
        self.assertIn("/desk/voice", self.html)

    def test_refresh_spcx_js_function_present(self):
        self.assertIn("refreshSpcx", self.html)

    def test_send_voice_command_js_function_present(self):
        self.assertIn("sendVoiceCommand", self.html)

    def test_render_spcx_card_js_function_present(self):
        self.assertIn("renderSpcxCard", self.html)

    def test_monitor_only_label_in_ui(self):
        self.assertIn("monitor_only", self.html)


if __name__ == "__main__":
    unittest.main()
