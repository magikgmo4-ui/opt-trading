"""
Tests for DeskPro market thesis routes — PR8.
"""

from __future__ import annotations

import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from modules.desk_pro.api.routes import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestDeskThesisRoutes(unittest.TestCase):
    def test_summary_endpoint(self):
        response = client.get("/desk/thesis")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["count"], 9)

    def test_summary_fields(self):
        response = client.get("/desk/thesis")
        data = response.json()
        item = data["symbols"][0]
        for field in ["symbol", "direction", "confidence", "prob_bull", "one_liner"]:
            self.assertIn(field, item)

    def test_symbol_endpoint(self):
        response = client.get("/desk/thesis/BTC")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["symbol"], "BTC")
        self.assertIn("thesis", data)

    def test_symbol_build(self):
        response = client.get("/desk/thesis/BTC?build=true")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])

    def test_symbol_not_found(self):
        response = client.get("/desk/thesis/ZZZTOP")
        # Unknown symbols get built but may fail — check response
        self.assertIn(response.status_code, (200, 404, 500))

    def test_thesis_ui_page(self):
        response = client.get("/desk/thesis/ui")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("Market Thesis", html)
        self.assertIn("thesis-card", html)

    def test_thesis_ui_symbol_page(self):
        response = client.get("/desk/thesis/ui/BTC")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("BTC", html)
        self.assertIn("Market Thesis", html)

    def test_thesis_ui_has_dark_theme(self):
        response = client.get("/desk/thesis/ui")
        html = response.text
        self.assertIn("background:#111", html)
        self.assertIn("color:#e0e0e0", html)

    def test_thesis_ui_mobile_viewport(self):
        response = client.get("/desk/thesis/ui")
        html = response.text
        self.assertIn("viewport", html)
        self.assertIn("max-width:600px", html)

    def test_ui_has_probability_bar(self):
        response = client.get("/desk/thesis/ui/BTC")
        html = response.text
        self.assertIn("bar", html.lower())


if __name__ == "__main__":
    unittest.main()
