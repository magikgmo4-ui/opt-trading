"""
Tests for runtime_registry — data/data_center/_registry/producers.json lifecycle.
"""
import shutil
import tempfile
import unittest
from pathlib import Path

from modules.data_center.runtime_registry import (
    load_runtime_registry,
    update_producer_last_write,
)

_RUNTIME_PATH = Path("data/data_center/_registry/producers.json")


class TestUpdateProducerLastWrite(unittest.TestCase):
    def setUp(self):
        self.td = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.td)

    def test_creates_runtime_registry_file(self):
        self.assertFalse((self.td / _RUNTIME_PATH).exists())
        update_producer_last_write(
            "derivatives_collector__bitget", "market_metrics.v1",
            "data/data_center/derivatives/derivatives_collector__bitget/latest.json",
            root=self.td,
        )
        self.assertTrue((self.td / _RUNTIME_PATH).exists())

    def test_entry_has_producer_id(self):
        update_producer_last_write(
            "derivatives_collector__bitget", "market_metrics.v1", "some/path.json",
            root=self.td,
        )
        rt = load_runtime_registry(root=self.td)
        self.assertEqual(
            rt["producers"]["derivatives_collector__bitget"]["producer_id"],
            "derivatives_collector__bitget",
        )

    def test_entry_has_contract_class(self):
        update_producer_last_write(
            "derivatives_collector__binance", "market_metrics.v1", "some/path.json",
            root=self.td,
        )
        rt = load_runtime_registry(root=self.td)
        self.assertEqual(
            rt["producers"]["derivatives_collector__binance"]["contract_class"],
            "market_metrics.v1",
        )

    def test_entry_has_last_write(self):
        update_producer_last_write(
            "derivatives_collector__bitget", "market_metrics.v1", "some/path.json",
            root=self.td,
        )
        rt = load_runtime_registry(root=self.td)
        last_write = rt["producers"]["derivatives_collector__bitget"]["last_write"]
        self.assertIsNotNone(last_write)
        self.assertIn("2026", last_write)

    def test_entry_has_status_ok_by_default(self):
        update_producer_last_write(
            "derivatives_collector__bitget", "market_metrics.v1", "p.json",
            root=self.td,
        )
        rt = load_runtime_registry(root=self.td)
        self.assertEqual(rt["producers"]["derivatives_collector__bitget"]["status"], "ok")

    def test_entry_has_last_output_path(self):
        path = "data/data_center/derivatives/derivatives_collector__bitget/latest.json"
        update_producer_last_write(
            "derivatives_collector__bitget", "market_metrics.v1", path,
            root=self.td,
        )
        rt = load_runtime_registry(root=self.td)
        self.assertEqual(
            rt["producers"]["derivatives_collector__bitget"]["last_output_path"],
            path,
        )

    def test_entry_has_evidence(self):
        update_producer_last_write(
            "derivatives_collector__bitget", "market_metrics.v1", "p.json",
            root=self.td,
            evidence={"symbol": "BTCUSDT", "provider_id": "bitget"},
        )
        rt = load_runtime_registry(root=self.td)
        ev = rt["producers"]["derivatives_collector__bitget"]["evidence"]
        self.assertEqual(ev["symbol"], "BTCUSDT")
        self.assertEqual(ev["provider_id"], "bitget")

    def test_accumulates_two_producers(self):
        update_producer_last_write(
            "derivatives_collector__bitget", "market_metrics.v1", "a.json",
            root=self.td,
        )
        update_producer_last_write(
            "derivatives_collector__binance", "market_metrics.v1", "b.json",
            root=self.td,
        )
        rt = load_runtime_registry(root=self.td)
        self.assertIn("derivatives_collector__bitget", rt["producers"])
        self.assertIn("derivatives_collector__binance", rt["producers"])

    def test_second_update_overwrites_for_same_producer(self):
        update_producer_last_write(
            "derivatives_collector__bitget", "market_metrics.v1", "first.json",
            root=self.td,
        )
        update_producer_last_write(
            "derivatives_collector__bitget", "market_metrics.v1", "second.json",
            root=self.td,
        )
        rt = load_runtime_registry(root=self.td)
        self.assertEqual(
            rt["producers"]["derivatives_collector__bitget"]["last_output_path"],
            "second.json",
        )
        self.assertEqual(len(rt["producers"]), 1)

    def test_registry_version_is_v1(self):
        update_producer_last_write(
            "derivatives_collector__bitget", "market_metrics.v1", "p.json",
            root=self.td,
        )
        rt = load_runtime_registry(root=self.td)
        self.assertEqual(rt["runtime_registry_version"], "v1")


class TestLoadRuntimeRegistry(unittest.TestCase):
    def setUp(self):
        self.td = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.td)

    def test_returns_empty_if_no_file(self):
        rt = load_runtime_registry(root=self.td)
        self.assertEqual(rt["producers"], {})
        self.assertEqual(rt["runtime_registry_version"], "v1")
