from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from modules.voice_operator.api.routes import app
from modules.voice_operator.menu import asset_shortcuts, grouped_intents, menu_sections, quick_commands


class TestVoiceMenuHelpers(unittest.TestCase):
    def test_grouped_intents_non_empty(self):
        groups = grouped_intents()
        self.assertGreater(len(groups), 0)
        self.assertTrue(any(g["group"] == "Executive" for g in groups))

    def test_quick_commands_contains_new_entries(self):
        cmds = quick_commands()
        for cmd in [
            "briefing quotidien",
            "briefing automatique",
            "fiche setup",
            "carte setup",
        ]:
            self.assertIn(cmd, cmds)

    def test_menu_sections_contains_executive_and_setups(self):
        sections = menu_sections()
        names = {s["section"] for s in sections}
        self.assertIn("Executive", names)
        self.assertIn("Setups", names)

    def test_asset_shortcuts_contains_btc_and_gold(self):
        shortcuts = asset_shortcuts()
        assets = {s["asset"] for s in shortcuts}
        self.assertIn("BTC", assets)
        self.assertIn("Gold", assets)


class TestVoiceMenuEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_grouped_intents_endpoint(self):
        r = self.client.get("/read/intents/grouped")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data["ok"])
        self.assertIn("groups", data)
        self.assertIn("quick_commands", data)
        self.assertIn("sections", data)
        self.assertIn("asset_shortcuts", data)

    def test_grouped_intents_exposes_new_commands(self):
        data = self.client.get("/read/intents/grouped").json()
        quick = data["quick_commands"]
        for cmd in ["briefing quotidien", "fiche setup"]:
            self.assertIn(cmd, quick)

    def test_ui_commands_html(self):
        r = self.client.get("/ui/commands")
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn("Voice Operator Commands", html)
        self.assertIn("briefing quotidien", html)
        self.assertIn("fiche setup", html)
        self.assertIn("viewport", html)
        self.assertIn("cmdSearch", html)
        self.assertIn("asset-grid", html)
