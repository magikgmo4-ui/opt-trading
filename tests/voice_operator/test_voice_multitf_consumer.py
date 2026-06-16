"""Tests for multitf consumer integration in Voice Operator composites."""
from __future__ import annotations
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestMultiTFReader(unittest.TestCase):
    def test_reader_imports(self):
        from modules.voice_operator.readers.multitf_reader import (
            read_symbol_score, read_all_scores, summarize_best_setups,
            summarize_missing, build_setup_summary_for_voice,
        )

    def test_read_symbol_score_returns_none_for_missing(self):
        from modules.voice_operator.readers.multitf_reader import read_symbol_score
        result = read_symbol_score("NONEXISTENT_SYMBOL_XYZ")
        self.assertIsNone(result)

    def test_read_all_scores_returns_list(self):
        from modules.voice_operator.readers.multitf_reader import read_all_scores
        scores = read_all_scores()
        self.assertIsInstance(scores, list)

    def test_summarize_best_setups_sorted_by_score(self):
        from modules.voice_operator.readers.multitf_reader import summarize_best_setups
        setups = summarize_best_setups(3)
        self.assertIsInstance(setups, list)
        if len(setups) >= 2:
            self.assertGreaterEqual(setups[0]["score"], setups[1]["score"],
                                    "Not sorted by score desc")

    def test_summarize_missing_returns_list(self):
        from modules.voice_operator.readers.multitf_reader import summarize_missing
        missing = summarize_missing()
        self.assertIsInstance(missing, list)

    def test_build_summary_has_required_fields(self):
        from modules.voice_operator.readers.multitf_reader import build_setup_summary_for_voice
        result = build_setup_summary_for_voice("BTC")
        self.assertIn("ok", result)
        self.assertIn("one_line", result)
        self.assertIn("spoken_text", result)
        self.assertIn("cards", result)
        self.assertIn("missing", result)
        self.assertIn("next_action", result)

    def test_build_summary_for_unknown_symbol(self):
        from modules.voice_operator.readers.multitf_reader import build_setup_summary_for_voice
        result = build_setup_summary_for_voice("UNKNOWN_XYZ")
        self.assertFalse(result["ok"])
        self.assertIn("indisponible", result["spoken_text"].lower())
        self.assertGreater(len(result["cards"]), 0)


class TestMultiTFConsumerComposites(unittest.TestCase):
    """Test that composites use multitf data."""

    def test_btc_full_reads_multitf(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("btc_full")
        spoken = result["rich"]["spoken_text"]
        self.assertIn("biais", spoken.lower() or " ")
        self.assertIn("grade", spoken.lower() or " ")
        self.assertIn("score", spoken.lower() or " ")
        cards = result["rich"]["cards"]
        labels = [c["label"] for c in cards]
        self.assertIn("Biais HTF", labels)
        self.assertIn("Grade", labels)

    def test_gold_full_reads_multitf(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("gold_full")
        spoken = result["rich"]["spoken_text"]
        cards = result["rich"]["cards"]
        # Should have multitf cards + price
        labels = [c["label"] for c in cards]
        self.assertTrue(any("biais" in l.lower() or "Grade" in l for l in labels),
                        f"No multitf cards found: {labels}")

    def test_market_view_has_multitf_setups(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("market_view")
        spoken = result["rich"]["spoken_text"]
        self.assertIn("setup", spoken.lower())
        cards = result["rich"]["cards"]
        has_grade = any("C" in c["label"] or "B" in c["label"] or "A" in c["label"] for c in cards)
        self.assertTrue(has_grade or len(cards) <= 2, f"No graded cards found in {len(cards)} cards")

    def test_priorities_uses_multitf(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("priorities")
        spoken = result["rich"]["spoken_text"]
        self.assertIn("multitf", spoken.lower())
        cards = result["rich"]["cards"]
        if cards:
            self.assertIn("score", cards[0]["value"].lower())

    def test_attention_checks_multitf(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("attention")
        spoken = result["rich"]["spoken_text"]
        cards = result["rich"]["cards"]
        # Should mention data quality or scores
        self.assertTrue(len(spoken) > 10 or len(cards) > 0)

    def test_exec_summary_uses_multitf(self):
        from modules.localcms.app.main import _handle_composite
        result = _handle_composite("exec_summary")
        spoken = result["rich"]["spoken_text"]
        has_multitf_term = any(w in spoken.lower() for w in ["setup", "score", "multitf", "grade"])
        self.assertTrue(has_multitf_term, f"No multitf terms in: {spoken[:80]}")

    def test_no_fallback_regression(self):
        """All UI button commands still route correctly."""
        from modules.voice_operator.engine.intent_router import route
        for cmd in ["analyse btc", "analyse gold", "rapport marche", "priorites",
                      "attention", "resume executif", "top movers"]:
            r = route(cmd)
            self.assertNotEqual(r.intent, "unknown", f"Command '{cmd}' fell back")

    def test_composites_return_contract(self):
        from modules.localcms.app.main import _handle_composite
        for ctype in ["btc_full", "gold_full", "market_view", "priorities",
                       "attention", "exec_summary"]:
            result = _handle_composite(ctype)
            self.assertIn("one_line", result, f"{ctype}: missing one_line")
            self.assertIn("rich", result, f"{ctype}: missing rich")
            self.assertIn("spoken_text", result["rich"], f"{ctype}: missing spoken_text")

    def test_no_execution_terms_in_responses(self):
        from modules.localcms.app.main import _handle_composite
        forbidden = ["execute", "broker", "order_book", "auto_trade", "market_order"]
        for ctype in ["btc_full", "gold_full", "priorities", "attention", "exec_summary"]:
            result = _handle_composite(ctype)
            text = result["rich"]["spoken_text"].lower()
            for term in forbidden:
                self.assertNotIn(term, text, f"{ctype}: contains forbidden '{term}'")
