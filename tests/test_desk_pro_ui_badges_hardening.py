"""Tests for /desk/ui badges hardening — contextual guidance and tab title."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.desk_pro.ui.page import render_ui_html


class TestHealthBadgePresence(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_healthbadge_function_present(self):
        self.assertIn("function healthBadge", self.html)

    def test_healthbadge_colors_defined(self):
        self.assertIn("'healthy'", self.html)
        self.assertIn("'degraded'", self.html)
        self.assertIn("'down'", self.html)

    def test_badge_function_present(self):
        self.assertIn("function badge", self.html)


class TestGuidanceLogic(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_guidance_block_rendered_for_degraded_or_down(self):
        self.assertIn("h.status === 'down' || h.status === 'degraded'", self.html)

    def test_webhook_activity_guidance_message(self):
        self.assertIn("Aucun signal TradingView", self.html)

    def test_webhook_activity_dev_context(self):
        self.assertIn("normal en dev local", self.html)

    def test_webhook_port_guidance_message(self):
        self.assertIn("Port 8000 injoignable", self.html)

    def test_perf_guidance_message(self):
        self.assertIn("Module Perf injoignable", self.html)

    def test_probe_errors_guidance_message(self):
        self.assertIn("/desk/errors", self.html)

    def test_guidance_div_has_id_for_testability(self):
        self.assertIn('id="healthGuidance"', self.html)

    def test_guidance_styled_as_warning_banner(self):
        self.assertIn("border-left:3px solid #f9a825", self.html)
        self.assertIn("background:#fff8e1", self.html)

    def test_causes_array_uses_check_field(self):
        self.assertIn("c.check", self.html)
        self.assertIn("causes.includes('webhook_activity')", self.html)
        self.assertIn("causes.includes('webhook')", self.html)
        self.assertIn("causes.includes('perf')", self.html)


class TestTabTitleUpdate(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_document_title_update_present(self):
        self.assertIn("document.title", self.html)

    def test_title_includes_desk_pro(self):
        self.assertIn("'Desk Pro'", self.html)

    def test_title_appends_status_when_not_healthy(self):
        self.assertIn("h.status !== 'healthy'", self.html)
        self.assertIn("h.status.toUpperCase()", self.html)


class TestUIStructureIntegrity(unittest.TestCase):
    """Regression: existing structure still intact after patch."""

    def setUp(self):
        self.html = render_ui_html()

    def test_pipeline_status_card_present(self):
        self.assertIn("Pipeline Status", self.html)

    def test_refresh_button_present(self):
        self.assertIn('id="btnStatus"', self.html)

    def test_test_alert_button_injected(self):
        self.assertIn("btnTestAlert", self.html)

    def test_snapshot_card_present(self):
        self.assertIn("Snapshot", self.html)

    def test_form_card_present(self):
        self.assertIn("Formulaire", self.html)

    def test_raw_json_collapsible_present(self):
        self.assertIn("Raw JSON", self.html)

    def test_no_secret_in_html(self):
        self.assertNotIn("BOT_TOKEN", self.html)
        self.assertNotIn("TELEGRAM_BOT", self.html)
        self.assertNotIn("ALERT_WEBHOOK_URL", self.html)
