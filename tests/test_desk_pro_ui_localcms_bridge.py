"""Tests for GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01.

Verifies:
- localcms link in action panel (static, target=_blank, port 8000)
- port conflict note present and visible (id=portConflictNote)
- note mentions both localcms and webhook server
- note mentions port 8000
- bridge doc exists with expected content
- no secrets
- regression: action panel, runtime health, error diagnostics intact
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.desk_pro.ui.page import render_ui_html


class TestLocalcmsLinkInActionPanel(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_localcms_link_present(self):
        self.assertIn('id="localcmsLink"', self.html)

    def test_localcms_link_points_to_port_8000(self):
        self.assertIn('href="http://127.0.0.1:8000"', self.html)

    def test_localcms_link_opens_new_tab(self):
        pos = self.html.index('id="localcmsLink"')
        fragment = self.html[pos - 200:pos + 200]
        self.assertIn('target="_blank"', fragment)

    def test_localcms_link_static_in_html(self):
        pos_link = self.html.index('id="localcmsLink"')
        pos_script = self.html.index('<script>')
        self.assertLess(pos_link, pos_script,
                        "localcmsLink must be in static HTML, not injected by JS")

    def test_localcms_link_inside_action_panel(self):
        pos_panel = self.html.index('id="actionPanel"')
        pos_link = self.html.index('id="localcmsLink"')
        # Find end of action panel div (next closing </div> after panel start)
        panel_close = self.html.index('</div>', pos_panel)
        self.assertLess(pos_link, panel_close,
                        "localcmsLink must be inside actionPanel")

    def test_localcms_link_title_mentions_conflict(self):
        pos = self.html.index('id="localcmsLink"')
        fragment = self.html[pos - 200:pos + 300]
        self.assertIn("incompatible", fragment)

    def test_localcms_link_has_action_link_class(self):
        pos = self.html.index('id="localcmsLink"')
        fragment = self.html[pos - 200:pos + 50]
        self.assertIn('class="action-link"', fragment)


class TestPortConflictNote(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_port_conflict_note_present(self):
        self.assertIn('id="portConflictNote"', self.html)

    def test_port_conflict_note_mentions_port_8000(self):
        pos = self.html.index('id="portConflictNote"')
        fragment = self.html[pos:pos + 400]
        self.assertIn("8000", fragment)

    def test_port_conflict_note_mentions_localcms(self):
        pos = self.html.index('id="portConflictNote"')
        fragment = self.html[pos:pos + 400]
        self.assertIn("localcms", fragment)

    def test_port_conflict_note_mentions_webhook(self):
        pos = self.html.index('id="portConflictNote"')
        fragment = self.html[pos:pos + 400]
        self.assertIn("webhook", fragment)

    def test_port_conflict_note_static_before_script(self):
        pos_note = self.html.index('id="portConflictNote"')
        pos_script = self.html.index('<script>')
        self.assertLess(pos_note, pos_script)

    def test_port_conflict_note_before_runtime_card(self):
        pos_note = self.html.index('id="portConflictNote"')
        pos_card = self.html.index('id="runtimeHealthCard"')
        self.assertLess(pos_note, pos_card)


class TestBridgeDocExists(unittest.TestCase):

    def test_bridge_doc_file_exists(self):
        p = PROJECT_ROOT / "docs/chantiers/GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01/10_BRIDGE_DOC.md"
        self.assertTrue(p.exists(), f"Bridge doc not found at {p}")

    def test_bridge_doc_mentions_port_conflict(self):
        p = PROJECT_ROOT / "docs/chantiers/GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01/10_BRIDGE_DOC.md"
        content = p.read_text()
        self.assertIn("8000", content)
        self.assertIn("localcms", content)
        self.assertIn("webhook", content)

    def test_bridge_doc_mentions_desk_pro_port(self):
        p = PROJECT_ROOT / "docs/chantiers/GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01/10_BRIDGE_DOC.md"
        content = p.read_text()
        self.assertIn("8010", content)

    def test_bridge_doc_has_smoke_section(self):
        p = PROJECT_ROOT / "docs/chantiers/GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01/10_BRIDGE_DOC.md"
        content = p.read_text()
        self.assertIn("/health", content)
        self.assertIn("curl", content)

    def test_bridge_doc_no_secrets(self):
        p = PROJECT_ROOT / "docs/chantiers/GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01/10_BRIDGE_DOC.md"
        content = p.read_text()
        self.assertNotIn("BOT_TOKEN", content)
        self.assertNotIn("TELEGRAM_BOT", content)
        self.assertNotIn("ALERT_WEBHOOK_URL", content)


class TestLocalcmsBridgeSafety(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_no_secret_in_html(self):
        self.assertNotIn("BOT_TOKEN", self.html)
        self.assertNotIn("TELEGRAM_BOT", self.html)
        self.assertNotIn("ALERT_WEBHOOK_URL", self.html)

    def test_no_localcms_data_merged_in_desk_pro(self):
        # localcms API calls must not be present in Desk Pro UI
        self.assertNotIn("/api/shared", self.html)
        self.assertNotIn("/api/installer", self.html)
        self.assertNotIn("/api/config", self.html)


class TestRegressionAfterBridgeLinks(unittest.TestCase):

    def setUp(self):
        self.html = render_ui_html()

    def test_action_panel_still_present(self):
        self.assertIn('id="actionPanel"', self.html)

    def test_runtime_health_heading_still_present(self):
        self.assertIn("Runtime Health", self.html)

    def test_error_diagnostics_still_present(self):
        self.assertIn('id="errorDiagnostics"', self.html)

    def test_analysis_tools_still_present(self):
        self.assertIn('id="analysisTools"', self.html)

    def test_guidance_banner_still_present(self):
        self.assertIn('id="healthGuidance"', self.html)

    def test_prior_action_links_still_present(self):
        self.assertIn('href="/desk/errors"', self.html)
        self.assertIn('href="/desk/toolbox"', self.html)
        self.assertIn('href="/desk/logs/latest"', self.html)
