"""Tests for GO_OPT_TRADING_UI_VISUAL_REGRESSION_SMOKE_01.

Structural regression tests on HTML captures and page source.
- HTML captures exist in docs/screenshots/
- desk_ui.html contains all key structural elements
- desk_toolbox.html is non-empty HTML
- JSON captures have expected structure
- Expected state matrix doc exists
- Smoke manifest exists
- No secrets in captures
"""
from __future__ import annotations
import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SCREENSHOTS = PROJECT_ROOT / "docs" / "screenshots"


class TestCaptureFilesExist(unittest.TestCase):

    def test_screenshots_dir_exists(self):
        self.assertTrue(SCREENSHOTS.exists())

    def test_desk_ui_capture_exists(self):
        self.assertTrue((SCREENSHOTS / "desk_ui.html").exists())

    def test_desk_toolbox_capture_exists(self):
        self.assertTrue((SCREENSHOTS / "desk_toolbox.html").exists())

    def test_desk_status_capture_exists(self):
        self.assertTrue((SCREENSHOTS / "desk_status.json").exists())

    def test_desk_errors_capture_exists(self):
        self.assertTrue((SCREENSHOTS / "desk_errors.json").exists())

    def test_desk_health_capture_exists(self):
        self.assertTrue((SCREENSHOTS / "desk_health.json").exists())

    def test_smoke_manifest_exists(self):
        self.assertTrue((SCREENSHOTS / "00_SMOKE_MANIFEST.md").exists())

    def test_expected_state_matrix_exists(self):
        p = PROJECT_ROOT / "docs/chantiers/GO_OPT_TRADING_UI_VISUAL_REGRESSION_SMOKE_01/10_EXPECTED_STATE_MATRIX.md"
        self.assertTrue(p.exists())


class TestDeskUiCaptureStructure(unittest.TestCase):

    def setUp(self):
        self.html = (SCREENSHOTS / "desk_ui.html").read_text(encoding="utf-8")

    def test_capture_is_nonempty(self):
        self.assertGreater(len(self.html), 5000)

    def test_page_title_present(self):
        self.assertIn("Desk Pro", self.html)

    def test_action_panel_present(self):
        self.assertIn('id="actionPanel"', self.html)

    def test_btn_status_present(self):
        self.assertIn('id="btnStatus"', self.html)

    def test_btn_test_alert_present(self):
        self.assertIn('id="btnTestAlert"', self.html)

    def test_errors_link_present(self):
        self.assertIn('href="/desk/errors"', self.html)

    def test_alerts_link_present(self):
        self.assertIn('href="/desk/alerts"', self.html)

    def test_logs_link_present(self):
        self.assertIn('href="/desk/logs/latest"', self.html)

    def test_toolbox_link_present(self):
        self.assertIn('href="/desk/toolbox"', self.html)

    def test_localcms_link_present(self):
        self.assertIn('href="http://127.0.0.1:8000"', self.html)

    def test_port_conflict_note_present(self):
        self.assertIn('id="portConflictNote"', self.html)

    def test_runtime_health_card_present(self):
        self.assertIn('id="runtimeHealthCard"', self.html)

    def test_pipeline_summary_present(self):
        self.assertIn('id="pipelineSummary"', self.html)

    def test_error_diagnostics_present(self):
        self.assertIn('id="errorDiagnostics"', self.html)

    def test_analysis_tools_present(self):
        self.assertIn('id="analysisTools"', self.html)

    def test_form_card_present(self):
        self.assertIn('id="formCard"', self.html)

    def test_snap_table_present(self):
        self.assertIn('id="snapTable"', self.html)

    def test_responsive_media_query_present(self):
        self.assertIn("max-width:900px", self.html)

    def test_guidance_logic_present(self):
        self.assertIn("healthGuidance", self.html)

    def test_dynamic_tab_title_present(self):
        self.assertIn("document.title", self.html)

    def test_no_secret_in_capture(self):
        self.assertNotIn("BOT_TOKEN", self.html)
        self.assertNotIn("TELEGRAM_BOT", self.html)
        self.assertNotIn("ALERT_WEBHOOK_URL", self.html)


class TestDeskToolboxCaptureStructure(unittest.TestCase):

    def setUp(self):
        self.html = (SCREENSHOTS / "desk_toolbox.html").read_text(encoding="utf-8")

    def test_capture_is_nonempty(self):
        self.assertGreater(len(self.html), 1000)

    def test_is_html(self):
        self.assertIn("<html", self.html.lower())

    def test_no_secret_in_capture(self):
        self.assertNotIn("BOT_TOKEN", self.html)
        self.assertNotIn("TELEGRAM_BOT", self.html)


class TestJsonCapturesStructure(unittest.TestCase):

    def test_desk_health_ok_true(self):
        d = json.loads((SCREENSHOTS / "desk_health.json").read_text())
        self.assertTrue(d.get("ok"))

    def test_desk_errors_ok_true(self):
        d = json.loads((SCREENSHOTS / "desk_errors.json").read_text())
        self.assertTrue(d.get("ok"))
        self.assertIn("count", d)
        self.assertIn("errors", d)

    def test_desk_status_has_health(self):
        d = json.loads((SCREENSHOTS / "desk_status.json").read_text())
        self.assertIn("health", d)
        self.assertIn("status", d["health"])
        self.assertIn("checks", d["health"])

    def test_desk_status_has_ts(self):
        d = json.loads((SCREENSHOTS / "desk_status.json").read_text())
        self.assertIn("ts", d)

    def test_desk_status_no_secret(self):
        content = (SCREENSHOTS / "desk_status.json").read_text()
        self.assertNotIn("BOT_TOKEN", content)
        self.assertNotIn("TELEGRAM_BOT", content)


class TestSmokeManifestContent(unittest.TestCase):

    def setUp(self):
        self.manifest = (SCREENSHOTS / "00_SMOKE_MANIFEST.md").read_text()

    def test_manifest_mentions_desk_ui(self):
        self.assertIn("/desk/ui", self.manifest)

    def test_manifest_mentions_desk_toolbox(self):
        self.assertIn("/desk/toolbox", self.manifest)

    def test_manifest_has_sha256(self):
        self.assertIn("sha-256", self.manifest.lower())

    def test_manifest_mentions_http_200(self):
        self.assertIn("200", self.manifest)
