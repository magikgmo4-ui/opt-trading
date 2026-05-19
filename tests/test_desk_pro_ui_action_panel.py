"""Tests for GO_OPT_TRADING_DESKPRO_UI_ACTION_PANEL_01.

Verifies:
- Action Panel is static HTML (not JS-injected)
- btnTestAlert present in static HTML, wired at init
- btnStatus present, renamed to "Refresh Status"
- Diagnostic links: errors, alerts, logs, toolbox
- testAlertResult span static
- No dynamic injection of action buttons in refreshStatus()
- No secrets in action panel
- Prior features intact (badges, guidance, IA sections)
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.desk_pro.ui.page import render_ui_html


class TestActionPanelStatic(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_action_panel_id_present(self):
        self.assertIn('id="actionPanel"', self.html)

    def test_action_panel_has_class(self):
        self.assertIn('class="action-panel"', self.html)

    def test_btn_test_alert_static_in_html(self):
        # Must appear before <script> tag — i.e., in static HTML, not injected
        pos_btn = self.html.index('id="btnTestAlert"')
        pos_script = self.html.index('<script>')
        self.assertLess(pos_btn, pos_script,
                        "btnTestAlert must be in static HTML, not injected by JS")

    def test_btn_status_static_in_html(self):
        pos_btn = self.html.index('id="btnStatus"')
        pos_script = self.html.index('<script>')
        self.assertLess(pos_btn, pos_script)

    def test_test_alert_result_span_static(self):
        pos_span = self.html.index('id="testAlertResult"')
        pos_script = self.html.index('<script>')
        self.assertLess(pos_span, pos_script,
                        "testAlertResult span must be in static HTML")

    def test_status_ts_span_static(self):
        pos_span = self.html.index('id="statusTs"')
        pos_script = self.html.index('<script>')
        self.assertLess(pos_span, pos_script)

    def test_action_panel_before_runtime_health_card(self):
        pos_panel = self.html.index('id="actionPanel"')
        pos_card = self.html.index('id="runtimeHealthCard"')
        self.assertLess(pos_panel, pos_card)


class TestActionPanelLinks(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_errors_link_present(self):
        self.assertIn('href="/desk/errors"', self.html)

    def test_alerts_link_present(self):
        self.assertIn('href="/desk/alerts"', self.html)

    def test_logs_latest_link_present(self):
        self.assertIn('href="/desk/logs/latest"', self.html)

    def test_toolbox_link_present(self):
        self.assertIn('href="/desk/toolbox"', self.html)

    def test_action_link_class_present(self):
        self.assertIn('class="action-link"', self.html)

    def test_action_btn_class_present(self):
        self.assertIn('class="action-btn"', self.html)


class TestActionPanelJsWiring(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()
        script_start = self.html.rindex('<script>')
        self.script = self.html[script_start:]

    def test_test_alert_listener_wired_at_init(self):
        self.assertIn("el('btnTestAlert').addEventListener('click', testAlert)", self.script)

    def test_refresh_status_listener_wired_at_init(self):
        self.assertIn("el('btnStatus').addEventListener('click', refreshStatus)", self.script)

    def test_test_alert_not_dynamically_injected(self):
        # btnTestAlert should not appear inside refreshStatus() function body
        # Find refreshStatus function body
        start = self.script.index("async function refreshStatus")
        end = self.script.index("\nasync function refreshSnap")
        fn_body = self.script[start:end]
        self.assertNotIn('btnTestAlert', fn_body,
                         "btnTestAlert must not be dynamically injected inside refreshStatus()")

    def test_test_alert_result_not_dynamically_injected(self):
        start = self.script.index("async function refreshStatus")
        end = self.script.index("\nasync function refreshSnap")
        fn_body = self.script[start:end]
        self.assertNotIn('testAlertResult', fn_body,
                         "testAlertResult must not be dynamically injected inside refreshStatus()")

    def test_test_alert_function_defined(self):
        self.assertIn("async function testAlert", self.script)

    def test_refresh_status_auto_called_at_init(self):
        lines = self.script.splitlines()
        auto_calls = [l.strip() for l in lines if l.strip() == "refreshStatus();"]
        self.assertGreater(len(auto_calls), 0)


class TestActionPanelSafety(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_no_secret_in_html(self):
        self.assertNotIn("BOT_TOKEN", self.html)
        self.assertNotIn("TELEGRAM_BOT", self.html)
        self.assertNotIn("ALERT_WEBHOOK_URL", self.html)

    def test_no_destructive_action_buttons(self):
        # No stop/kill/delete/drop actions in the panel
        panel_start = self.html.index('id="actionPanel"')
        # Take just the panel section (until closing div)
        panel_fragment = self.html[panel_start:panel_start + 600]
        self.assertNotIn("stop", panel_fragment.lower().replace("Refresh Status", ""))
        self.assertNotIn("kill", panel_fragment.lower())
        self.assertNotIn("delete", panel_fragment.lower())


class TestRegressionAfterActionPanel(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_runtime_health_heading_present(self):
        self.assertIn("Runtime Health", self.html)

    def test_analysis_tools_details_present(self):
        self.assertIn('id="analysisTools"', self.html)

    def test_form_card_collapsible_present(self):
        self.assertIn('id="formCard"', self.html)

    def test_healthbadge_function_present(self):
        self.assertIn("function healthBadge", self.html)

    def test_guidance_banner_present(self):
        self.assertIn('id="healthGuidance"', self.html)

    def test_dynamic_tab_title_present(self):
        self.assertIn("document.title", self.html)

    def test_responsive_media_query_present(self):
        self.assertIn("max-width:900px", self.html)

    def test_raw_json_collapsible_present(self):
        self.assertIn("Raw JSON", self.html)
