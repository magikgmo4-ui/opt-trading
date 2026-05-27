"""
Tests for localcms_health_reader — localcms__data_center_health consumer.
"""
import unittest

from modules.data_center.localcms_health_reader import read_data_center_health


class TestReadDataCenterHealth(unittest.TestCase):
    def setUp(self):
        self.result = read_data_center_health()

    def test_ok_is_true(self):
        self.assertTrue(self.result["ok"])

    def test_consumer_id(self):
        self.assertEqual(self.result["consumer_id"], "localcms__data_center_health")

    def test_source(self):
        self.assertEqual(self.result["source"], "data_center_registry")

    def test_producer_count_is_correct(self):
        self.assertGreaterEqual(self.result["producer_count"], 3)

    def test_consumer_count_is_correct(self):
        self.assertGreaterEqual(self.result["consumer_count"], 7)

    def test_implemented_consumers_is_list(self):
        self.assertIsInstance(self.result["implemented_consumers"], list)

    def test_localcms_is_in_implemented_consumers(self):
        self.assertIn("localcms__data_center_health", self.result["implemented_consumers"])

    def test_desk_pro_is_in_implemented_consumers(self):
        self.assertIn("desk_pro__market_metrics", self.result["implemented_consumers"])

    def test_contract_classes_contains_market_metrics(self):
        self.assertIn("market_metrics.v1", self.result["contract_classes"])

    def test_read_at_is_set(self):
        self.assertIsInstance(self.result["read_at"], str)
        self.assertTrue(self.result["read_at"].startswith("2026"))

    def test_producer_runtime_is_list(self):
        self.assertIsInstance(self.result["producer_runtime"], list)
