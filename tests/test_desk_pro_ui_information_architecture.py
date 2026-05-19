"""Tests for GO_OPT_TRADING_DESKPRO_UI_INFORMATION_ARCHITECTURE_01.

Verifies:
- Runtime Health section visually separated (h2 heading + runtimeHealthCard)
- Analysis Tools section is a collapsible <details> element
- Form card is a collapsible <details> element
- Snapshot does NOT auto-load on page init
- /desk/errors and /desk/alerts links present
- Responsive media query at 900px
- Prior features (badges, guidance, title) still intact
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.desk_pro.ui.page import render_ui_html


class TestRuntimeHealthSection(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_runtime_health_heading_present(self):
        self.assertIn("Runtime Health", self.html)

    def test_runtime_health_card_id_present(self):
        self.assertIn('id="runtimeHealthCard"', self.html)

    def test_pipeline_status_inside_runtime_health(self):
        pos_runtime = self.html.index('id="runtimeHealthCard"')
        pos_pipeline = self.html.index("Pipeline Status")
        self.assertGreater(pos_pipeline, pos_runtime)

    def test_runtime_health_before_analysis_tools(self):
        pos_runtime = self.html.index("Runtime Health")
        pos_analysis = self.html.index("Analysis Tools")
        self.assertLess(pos_runtime, pos_analysis)

    def test_errors_link_in_runtime_health_section(self):
        self.assertIn('href="/desk/errors"', self.html)

    def test_alerts_link_in_runtime_health_section(self):
        self.assertIn('href="/desk/alerts"', self.html)


class TestAnalysisToolsSection(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_analysis_tools_is_details_element(self):
        self.assertIn('<details class="tools-section"', self.html)

    def test_analysis_tools_id_present(self):
        self.assertIn('id="analysisTools"', self.html)

    def test_analysis_tools_summary_text(self):
        self.assertIn(">Analysis Tools<", self.html)

    def test_snapshot_inside_analysis_tools(self):
        pos_analysis = self.html.index('id="analysisTools"')
        pos_snapshot = self.html.index('id="snapTable"')
        self.assertGreater(pos_snapshot, pos_analysis)


class TestFormCardCollapsible(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_form_card_is_details_element(self):
        self.assertIn('<details class="card" id="formCard"', self.html)

    def test_form_card_has_summary(self):
        pos_form = self.html.index('id="formCard"')
        fragment = self.html[pos_form:pos_form + 300]
        self.assertIn("<summary", fragment)

    def test_form_card_not_open_by_default(self):
        # <details> without 'open' attribute = collapsed by default
        self.assertNotIn('<details class="card" id="formCard" open', self.html)

    def test_form_fields_inside_form_card(self):
        pos_form = self.html.index('id="formCard"')
        fragment = self.html[pos_form:]
        self.assertIn('id="symbol"', fragment)
        self.assertIn('id="btnSubmit"', fragment)


class TestSnapshotNoAutoLoad(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_refresh_snap_function_defined(self):
        self.assertIn("async function refreshSnap", self.html)

    def test_snap_not_auto_called_at_init(self):
        # refreshStatus() is called at init, refreshSnap() should NOT be
        # Find the last script section and check refreshSnap() is not called bare
        script_start = self.html.rindex("<script>")
        script = self.html[script_start:]
        # refreshSnap() as a standalone call (not as event listener assignment)
        lines = script.splitlines()
        standalone_calls = [l.strip() for l in lines if l.strip() == "refreshSnap();"]
        self.assertEqual(len(standalone_calls), 0, "refreshSnap() should not be auto-called on init")

    def test_refresh_status_auto_called(self):
        script_start = self.html.rindex("<script>")
        script = self.html[script_start:]
        lines = script.splitlines()
        standalone_calls = [l.strip() for l in lines if l.strip() == "refreshStatus();"]
        self.assertGreater(len(standalone_calls), 0, "refreshStatus() must be auto-called on init")

    def test_snap_button_listener_present(self):
        self.assertIn("el('btnSnap').addEventListener('click', refreshSnap)", self.html)


class TestResponsiveLayout(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_media_query_900px_present(self):
        self.assertIn("max-width:900px", self.html)

    def test_media_query_collapses_grid(self):
        pos_mq = self.html.index("max-width:900px")
        fragment = self.html[pos_mq:pos_mq + 100]
        self.assertIn("grid-template-columns:1fr", fragment)


class TestRegressionPriorFeatures(unittest.TestCase):
    """Ensure IA restructure did not break prior deliverables."""

    def setUp(self):
        self.html = render_ui_html()

    def test_healthbadge_function_still_present(self):
        self.assertIn("function healthBadge", self.html)

    def test_guidance_banner_still_present(self):
        self.assertIn('id="healthGuidance"', self.html)

    def test_guidance_webhook_activity_message_still_present(self):
        self.assertIn("Aucun signal TradingView", self.html)

    def test_dynamic_tab_title_still_present(self):
        self.assertIn("document.title", self.html)
        self.assertIn("h.status !== 'healthy'", self.html)

    def test_refresh_button_present(self):
        self.assertIn('id="btnStatus"', self.html)

    def test_raw_json_collapsible_present(self):
        self.assertIn("Raw JSON", self.html)

    def test_no_secret_in_html(self):
        self.assertNotIn("BOT_TOKEN", self.html)
        self.assertNotIn("TELEGRAM_BOT", self.html)
        self.assertNotIn("ALERT_WEBHOOK_URL", self.html)
