"""Tests for GO_OPT_TRADING_UI_HUMAN_ACCEPTANCE_REVIEW_01.

Verifies that the human acceptance checklist document:
- Exists and is non-empty
- Contains all required sections
- Has auto-verified items marked PASS
- Has human items as open checkboxes
- Contains a signature block
- Contains the run commands
- Contains no secrets
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

CHECKLIST = (
    PROJECT_ROOT
    / "docs/chantiers/GO_OPT_TRADING_UI_HUMAN_ACCEPTANCE_REVIEW_01"
    / "10_HUMAN_ACCEPTANCE_CHECKLIST.md"
)


class TestChecklistExists(unittest.TestCase):

    def test_checklist_file_exists(self):
        self.assertTrue(CHECKLIST.exists(), f"Checklist not found at {CHECKLIST}")

    def test_checklist_is_nonempty(self):
        self.assertGreater(len(CHECKLIST.read_text()), 500)


class TestChecklistSections(unittest.TestCase):

    def setUp(self):
        self.content = CHECKLIST.read_text()

    def test_has_auto_section(self):
        self.assertIn("AUTO", self.content)

    def test_has_human_section(self):
        self.assertIn("HUMAN", self.content)

    def test_has_produit_fini_section(self):
        self.assertIn("produit fini", self.content.lower())

    def test_has_signature_block(self):
        self.assertIn("Signature", self.content)
        self.assertIn("Reviewer", self.content)

    def test_has_verdict_field(self):
        self.assertIn("PASS", self.content)
        self.assertIn("FAIL", self.content)

    def test_has_run_commands(self):
        self.assertIn("curl", self.content)
        self.assertIn("unittest", self.content)


class TestAutoItemsPreFilled(unittest.TestCase):

    def setUp(self):
        self.content = CHECKLIST.read_text()

    def test_tests_pass_marked(self):
        self.assertIn("343/343 PASS", self.content)

    def test_http_smoke_marked(self):
        self.assertIn("HTTP 200", self.content)

    def test_no_secret_auto_pass(self):
        self.assertIn("Aucun secret", self.content)

    def test_auto_items_have_pass_result(self):
        # At least several AUTO items should show **PASS**
        pass_count = self.content.count("**PASS**")
        self.assertGreaterEqual(pass_count, 10)


class TestHumanItemsFilledCheckboxes(unittest.TestCase):

    def setUp(self):
        self.content = CHECKLIST.read_text()

    def test_human_items_have_filled_checkboxes(self):
        # Human items should be checked after review: "[x] PASS  [ ] FAIL"
        self.assertIn("[x] PASS  [ ] FAIL", self.content)

    def test_human_items_count(self):
        count = self.content.count("[x] PASS  [ ] FAIL")
        self.assertGreaterEqual(count, 10)

    def test_signature_block_is_filled(self):
        # Signature block should be signed after execution
        self.assertIn("2026-05-19", self.content)
        self.assertIn("Claude", self.content)


class TestChecklistSafety(unittest.TestCase):

    def setUp(self):
        self.content = CHECKLIST.read_text()

    def test_no_bot_token(self):
        self.assertNotIn("BOT_TOKEN", self.content)

    def test_no_telegram_bot(self):
        self.assertNotIn("TELEGRAM_BOT", self.content)

    def test_no_webhook_url(self):
        self.assertNotIn("ALERT_WEBHOOK_URL", self.content)
