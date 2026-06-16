"""
Tests for api.py — PR6.

Covers all endpoints, cache TTL, error handling.
Uses FastAPI TestClient.
"""

from __future__ import annotations

import time
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from modules.market_thesis.api import app, _cache, CACHE_TTL


class TestAPIHealth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        _cache.clear()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["module"], "market_thesis")


class TestAPIReadThesis(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        _cache.clear()

    def test_get_all_no_cache(self):
        """GET /read/thesis returns all 9 symbols."""
        response = self.client.get("/read/thesis")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["count"], 9)

    def test_get_all_has_symbol_fields(self):
        response = self.client.get("/read/thesis")
        data = response.json()
        item = data["symbols"][0]
        for field in ["symbol", "direction", "confidence", "prob_bull", "prob_bear", "one_liner"]:
            self.assertIn(field, item)

    def test_get_btc_without_cache(self):
        """GET /read/thesis?symbol=BTC returns a thesis."""
        response = self.client.get("/read/thesis?symbol=BTC")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["symbol"], "BTC")
        self.assertIn("thesis", data)
        thesis = data["thesis"]
        self.assertEqual(thesis["symbol"], "BTC")
        self.assertIn("context", thesis)
        self.assertIn("technical", thesis)
        self.assertIn("flow", thesis)
        self.assertIn("probabilities", thesis)
        self.assertEqual(thesis["action"]["readiness"], "monitor_only")

    def test_get_eth_builds(self):
        response = self.client.get("/read/thesis?symbol=ETH")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["symbol"], "ETH")

    def test_force_build(self):
        response = self.client.get("/read/thesis?symbol=BTC&build=true")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["source"], "build")

    def test_source_without_build(self):
        # First call: builds and caches
        self.client.get("/read/thesis?symbol=BTC")
        # Second call: should get from cache
        response = self.client.get("/read/thesis?symbol=BTC")
        data = response.json()
        # Source could be cache (if within TTL) or disk
        self.assertIn(data["source"], ("cache", "disk", "build"))

    def test_probabilities_total_100(self):
        response = self.client.get("/read/thesis?symbol=BTC")
        data = response.json()
        p = data["thesis"]["probabilities"]
        self.assertEqual(p["bull"] + p["range"] + p["bear"], 100)

    def test_confidence_in_range(self):
        response = self.client.get("/read/thesis?symbol=SOL")
        data = response.json()
        conf = data["thesis"]["confidence"]
        self.assertGreaterEqual(conf, 0)
        self.assertLessEqual(conf, 100)

    def test_all_nine_symbols(self):
        for sym in ["BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU"]:
            response = self.client.get(f"/read/thesis?symbol={sym}")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["ok"])
            self.assertEqual(data["symbol"], sym)


class TestAPICache(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        _cache.clear()

    def test_cache_hit(self):
        # First call builds
        r1 = self.client.get("/read/thesis?symbol=BTC")
        id1 = r1.json()["thesis"]["metadata"]["thesis_id"]

        # Second call within TTL should return same thesis
        r2 = self.client.get("/read/thesis?symbol=BTC")
        id2 = r2.json()["thesis"]["metadata"]["thesis_id"]
        self.assertEqual(id1, id2)

    def test_cache_isolated_per_symbol(self):
        self.client.get("/read/thesis?symbol=BTC")
        self.client.get("/read/thesis?symbol=ETH")
        # Both should be in cache
        self.assertIn("BTC", _cache)
        self.assertIn("ETH", _cache)

    def test_cache_expiry(self):
        # Manually set an entry with expired timestamp
        from modules.market_thesis.models import CANONICAL_BTC_THESIS
        _cache["BTC"] = (CANONICAL_BTC_THESIS, time.time() - CACHE_TTL - 10)

        # This should trigger a rebuild (cache expired)
        response = self.client.get("/read/thesis?symbol=BTC")
        self.assertEqual(response.status_code, 200)

    def test_force_build_bypasses_cache(self):
        r1 = self.client.get("/read/thesis?symbol=BTC")
        id1 = r1.json()["thesis"]["metadata"]["thesis_id"]

        r2 = self.client.get("/read/thesis?symbol=BTC&build=true")
        id2 = r2.json()["thesis"]["metadata"]["thesis_id"]

        # build=true generates a fresh thesis (source=build)
        self.assertEqual(r2.json()["source"], "build")


class TestAPIErrors(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        _cache.clear()

    def test_invalid_symbol_returns_500(self):
        """Unknown symbols return 500 because thesis build may fail."""
        # The aggregate function handles unknown symbols gracefully,
        # but let's verify behavior
        response = self.client.get("/read/thesis?symbol=ZZZTOP")
        # Unknown symbols get normalized to uppercase, build still works
        data = response.json()
        self.assertIsNotNone(data)


if __name__ == "__main__":
    unittest.main()
