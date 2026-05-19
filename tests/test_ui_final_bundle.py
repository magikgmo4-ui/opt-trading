"""Tests for GO_OPT_TRADING_UI_PRODUCT_FINAL_BUNDLE_01.

Verifies the final bundle ZIP:
- exists in dist/
- is non-empty
- SHA-256 matches documented value
- contains expected doc directories
- contains screenshots
- does NOT contain secrets/.env
- closeout doc exists with SHA-256
"""
from __future__ import annotations
import hashlib
import sys
import unittest
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

BUNDLE = PROJECT_ROOT / "dist" / "GO_OPT_TRADING_UI_PRODUCT_FINAL_BUNDLE_01.zip"
EXPECTED_SHA256 = "93c1cb94edb9590fdad30d5942a13c68463f01f75e8175fdd64dfb8a13305c71"

# ZIP is a local artifact excluded from git (*.zip in .gitignore).
# Tests that require the file are skipped on a fresh checkout.
_bundle_present = BUNDLE.exists()


@unittest.skipUnless(_bundle_present, "Bundle ZIP is a local artifact — run scripts/make_bundle.sh to regenerate")
class TestBundleExists(unittest.TestCase):

    def test_bundle_file_exists(self):
        self.assertTrue(BUNDLE.exists(), f"Bundle not found: {BUNDLE}")

    def test_bundle_is_nonempty(self):
        self.assertGreater(BUNDLE.stat().st_size, 10_000)

    def test_bundle_sha256_matches(self):
        h = hashlib.sha256(BUNDLE.read_bytes()).hexdigest()
        self.assertEqual(h, EXPECTED_SHA256,
                         f"SHA-256 mismatch: got {h}, expected {EXPECTED_SHA256}")


@unittest.skipUnless(_bundle_present, "Bundle ZIP is a local artifact — run scripts/make_bundle.sh to regenerate")
class TestBundleContents(unittest.TestCase):

    def setUp(self):
        self.zf = zipfile.ZipFile(BUNDLE)
        self.names = self.zf.namelist()

    def tearDown(self):
        self.zf.close()

    def _has_dir(self, prefix):
        return any(n.startswith(prefix) for n in self.names)

    def test_contains_mapping_kanban_docs(self):
        self.assertTrue(self._has_dir("docs/chantiers/GO_OPT_TRADING_UI_PRODUCTIZATION_MAPPING_AND_KANBAN_01"))

    def test_contains_shell_review_docs(self):
        self.assertTrue(self._has_dir("docs/chantiers/GO_OPT_TRADING_DESKPRO_UI_PRODUCT_SHELL_REVIEW_01"))

    def test_contains_badges_docs(self):
        self.assertTrue(self._has_dir("docs/chantiers/GO_OPT_TRADING_DESKPRO_UI_STATE_BADGES_HARDENING_01"))

    def test_contains_ia_docs(self):
        self.assertTrue(self._has_dir("docs/chantiers/GO_OPT_TRADING_DESKPRO_UI_INFORMATION_ARCHITECTURE_01"))

    def test_contains_action_panel_docs(self):
        self.assertTrue(self._has_dir("docs/chantiers/GO_OPT_TRADING_DESKPRO_UI_ACTION_PANEL_01"))

    def test_contains_error_diagnostics_docs(self):
        self.assertTrue(self._has_dir("docs/chantiers/GO_OPT_TRADING_DESKPRO_UI_ERROR_DIAGNOSTICS_PANEL_01"))

    def test_contains_localcms_bridge_docs(self):
        self.assertTrue(self._has_dir("docs/chantiers/GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01"))

    def test_contains_visual_regression_docs(self):
        self.assertTrue(self._has_dir("docs/chantiers/GO_OPT_TRADING_UI_VISUAL_REGRESSION_SMOKE_01"))

    def test_contains_human_acceptance_docs(self):
        self.assertTrue(self._has_dir("docs/chantiers/GO_OPT_TRADING_UI_HUMAN_ACCEPTANCE_REVIEW_01"))

    def test_contains_screenshots(self):
        self.assertTrue(self._has_dir("docs/screenshots/"))

    def test_contains_desk_ui_html(self):
        self.assertIn("docs/screenshots/desk_ui.html", self.names)

    def test_contains_smoke_manifest(self):
        self.assertIn("docs/screenshots/00_SMOKE_MANIFEST.md", self.names)

    def test_no_secrets_in_bundle(self):
        for name in self.names:
            self.assertNotIn("secrets/", name,
                             f"secrets/ found in bundle: {name}")

    def test_no_env_files_in_bundle(self):
        env_files = [n for n in self.names if n.endswith(".env")]
        self.assertEqual(env_files, [], f".env files found in bundle: {env_files}")


class TestBundleCloseoutDoc(unittest.TestCase):

    def setUp(self):
        p = PROJECT_ROOT / "docs/chantiers/GO_OPT_TRADING_UI_PRODUCT_FINAL_BUNDLE_01/90_CLOSEOUT.md"
        self.content = p.read_text()

    def test_closeout_has_sha256(self):
        self.assertIn(EXPECTED_SHA256, self.content)

    def test_closeout_mentions_tests_pass(self):
        self.assertIn("PASS", self.content)

    def test_closeout_mentions_no_secrets(self):
        self.assertIn("secret", self.content.lower())
