"""Tests for GO_OPT_TRADING_DESKPRO_UI_ERROR_DIAGNOSTICS_PANEL_01.

Verifies:
- errorDiagnostics div present in static HTML
- refreshErrors() function defined in JS
- "aucune erreur" state rendered when count=0
- error table rendered when count>0
- next action suggestion present per probe type
- old inline error block removed from refreshStatus()
- refreshErrors() called from refreshStatus()
- no secrets
- regression: prior sections intact
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.desk_pro.ui.page import render_ui_html


class TestErrorDiagnosticsStaticElement(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_error_diagnostics_div_present(self):
        self.assertIn('id="errorDiagnostics"', self.html)

    def test_error_diagnostics_inside_runtime_health_card(self):
        pos_card = self.html.index('id="runtimeHealthCard"')
        pos_diag = self.html.index('id="errorDiagnostics"')
        self.assertGreater(pos_diag, pos_card,
                           "errorDiagnostics must be inside runtimeHealthCard")

    def test_error_diagnostics_before_script_tag(self):
        pos_diag = self.html.index('id="errorDiagnostics"')
        pos_script = self.html.index('<script>')
        self.assertLess(pos_diag, pos_script)

    def test_error_diagnostics_below_pipeline_summary(self):
        pos_summary = self.html.index('id="pipelineSummary"')
        pos_diag = self.html.index('id="errorDiagnostics"')
        self.assertGreater(pos_diag, pos_summary)


class TestRefreshErrorsFunction(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()
        script_start = self.html.rindex('<script>')
        self.script = self.html[script_start:]

    def test_refresh_errors_function_defined(self):
        self.assertIn("async function refreshErrors", self.script)

    def test_refresh_errors_fetches_desk_errors(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("'/desk/errors'", fn)

    def test_no_error_state_rendered(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("aucune erreur", fn)

    def test_no_error_state_has_green_color(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("#2e7d32", fn)

    def test_error_count_displayed_in_red(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("#c62828", fn)
        self.assertIn("j.count", fn)

    def test_next_action_suggestion_present(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("Action sugg", fn)

    def test_next_action_webhook_case(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("webhook", fn)

    def test_next_action_perf_case(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("perf", fn)

    def test_error_table_rendered(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("<table", fn)
        self.assertIn("<thead>", fn)
        self.assertIn("e.probe", fn)
        self.assertIn("e.error", fn)

    def test_overflow_link_to_errors_log(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("/desk/errors", fn)

    def test_error_diagnostics_updated_in_fn(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("el('errorDiagnostics').innerHTML", fn)

    def test_unreachable_fallback_message(self):
        start = self.script.index("async function refreshErrors")
        end = self.script.index("\nasync function refreshSnap")
        fn = self.script[start:end]
        self.assertIn("inaccessible", fn)


class TestRefreshErrorsCalledFromStatus(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()
        script_start = self.html.rindex('<script>')
        self.script = self.html[script_start:]

    def test_refresh_errors_called_inside_refresh_status(self):
        start = self.script.index("async function refreshStatus")
        end = self.script.index("\nasync function refreshErrors")
        fn = self.script[start:end]
        self.assertIn("refreshErrors();", fn)

    def test_old_inline_error_block_removed(self):
        start = self.script.index("async function refreshStatus")
        end = self.script.index("\nasync function refreshErrors")
        fn = self.script[start:end]
        self.assertNotIn("j.error_count > 0", fn)
        self.assertNotIn("j.recent_errors", fn)


class TestErrorDiagnosticsSafety(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_no_secret_in_html(self):
        self.assertNotIn("BOT_TOKEN", self.html)
        self.assertNotIn("TELEGRAM_BOT", self.html)
        self.assertNotIn("ALERT_WEBHOOK_URL", self.html)


class TestRegressionAfterErrorDiagnostics(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_action_panel_still_present(self):
        self.assertIn('id="actionPanel"', self.html)

    def test_runtime_health_heading_still_present(self):
        self.assertIn("Runtime Health", self.html)

    def test_analysis_tools_details_still_present(self):
        self.assertIn('id="analysisTools"', self.html)

    def test_guidance_banner_still_present(self):
        self.assertIn('id="healthGuidance"', self.html)

    def test_healthbadge_function_still_present(self):
        self.assertIn("function healthBadge", self.html)

    def test_dynamic_tab_title_still_present(self):
        self.assertIn("document.title", self.html)

    def test_form_card_still_present(self):
        self.assertIn('id="formCard"', self.html)
