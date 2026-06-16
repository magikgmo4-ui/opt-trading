"""Schema validation tests for multitf_analysis_input.v1 and multitf_setup_score.v1 DC contracts."""
from __future__ import annotations
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class TestMultiTFAnalysisInputSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema_path = PROJECT_ROOT / "modules" / "data_center" / "contracts" / "multitf_analysis_input.v1.schema.json"
        cls.schema = json.loads(schema_path.read_text())

        sample_path = PROJECT_ROOT / "tests" / "fixtures" / "multitf_analysis_input_sample.json"
        cls.sample = json.loads(sample_path.read_text())

    def test_schema_has_title(self):
        self.assertEqual(self.schema["title"], "multitf_analysis_input.v1")

    def test_schema_required_fields(self):
        required = self.schema.get("required", [])
        self.assertIn("input_class", required)
        self.assertIn("symbol", required)
        self.assertIn("as_of", required)
        self.assertIn("price", required)
        self.assertIn("source", required)
        self.assertIn("freshness_state", required)

    def test_sample_passes_input_class(self):
        self.assertEqual(self.sample["input_class"], "multitf_analysis_input.v1")

    def test_sample_has_required_fields(self):
        for field in ["input_class", "symbol", "as_of", "price", "source", "freshness_state"]:
            self.assertIn(field, self.sample)

    def test_sample_has_timeframes(self):
        self.assertIn("timeframes", self.sample)
        self.assertIn("H4", self.sample["timeframes"])
        self.assertIn("M15", self.sample["timeframes"])

    def test_sample_has_levels(self):
        self.assertIn("levels", self.sample)
        levels = self.sample["levels"]
        self.assertIn("support_levels", levels)
        self.assertIn("resistance_levels", levels)
        self.assertIn("vwap", levels)

    def test_sample_has_signals(self):
        self.assertIn("signals", self.sample)
        self.assertIsInstance(self.sample["signals"], list)
        self.assertGreater(len(self.sample["signals"]), 0)
        sig = self.sample["signals"][0]
        self.assertEqual(sig["event"], "vwap_loss")
        self.assertIn("monitor_only", sig)
        self.assertTrue(sig["monitor_only"])

    def test_sample_has_source_quality(self):
        self.assertIn("source_quality", self.sample)
        sq = self.sample["source_quality"]
        self.assertIn("freshness_state", sq)
        self.assertIn("completeness_score", sq)

    def test_sample_has_missing_array(self):
        self.assertIn("missing", self.sample)
        self.assertIsInstance(self.sample["missing"], list)

    def test_freshness_state_enum(self):
        valid = {"fresh", "stale", "market_closed", "unknown"}
        self.assertIn(self.sample["freshness_state"], valid)

    def test_asset_class_enum(self):
        valid = {"crypto_perp", "forex_cfd", "stock", "ipo", "index", "commodity"}
        self.assertIn(self.sample["asset_class"], valid)

    def test_timeframe_indicators_structure(self):
        h4 = self.sample["timeframes"]["H4"]["indicators"]
        self.assertIn("trend", h4)
        self.assertIn("vwap", h4)
        self.assertIn("rsi", h4)
        self.assertTrue(0 <= h4["rsi"] <= 100)

    def test_no_execution_terms(self):
        """Schema and sample must not contain execution/broker/order terms."""
        schema_str = json.dumps(self.schema)
        sample_str = json.dumps(self.sample)
        forbidden = ["execute", "broker", "order_book_exec", "auto_trade", "market_order", "limit_order"]
        for term in forbidden:
            self.assertNotIn(term, schema_str.lower(), f"Forbidden term '{term}' found in schema")
            self.assertNotIn(term, sample_str.lower(), f"Forbidden term '{term}' found in sample")

    def test_monitor_only_constraints(self):
        """All signals must be monitor_only."""
        for sig in self.sample.get("signals", []):
            self.assertTrue(sig.get("monitor_only", False))


class TestMultiTFSetupScoreSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema_path = PROJECT_ROOT / "modules" / "data_center" / "contracts" / "multitf_setup_score.v1.schema.json"
        cls.schema = json.loads(schema_path.read_text())

        sample_path = PROJECT_ROOT / "tests" / "fixtures" / "multitf_setup_score_sample.json"
        cls.sample = json.loads(sample_path.read_text())

    def test_schema_has_title(self):
        self.assertEqual(self.schema["title"], "multitf_setup_score.v1")

    def test_schema_required_fields(self):
        required = self.schema.get("required", [])
        self.assertIn("output_class", required)
        self.assertIn("symbol", required)
        self.assertIn("as_of", required)
        self.assertIn("bias", required)
        self.assertIn("setups", required)

    def test_sample_passes_output_class(self):
        self.assertEqual(self.sample["output_class"], "multitf_setup_score.v1")

    def test_sample_bias_structure(self):
        bias = self.sample["bias"]
        self.assertIn("htf", bias)
        self.assertIn("ltf", bias)
        self.assertIn("alignment", bias)
        self.assertIn("reason", bias)

    def test_sample_setups_structure(self):
        setups = self.sample["setups"]
        self.assertGreater(len(setups), 0)
        s = setups[0]
        self.assertIn("setup_id", s)
        self.assertIn("direction", s)
        self.assertIn("grade", s)
        self.assertIn("score", s)
        self.assertTrue(0 <= s["score"] <= 100)
        self.assertIn("probability_pct", s)
        self.assertTrue(0 <= s["probability_pct"] <= 100)
        self.assertIn("confidence_pct", s)
        self.assertTrue(0 <= s["confidence_pct"] <= 100)
        self.assertIn("entry_zone", s)
        self.assertIn("invalidation", s)
        self.assertIn("targets", s)
        self.assertIn("risk_reward", s)
        self.assertIn("reason", s)
        self.assertIn("missing", s)

    def test_sample_setup_score_breakdown(self):
        s = self.sample["setups"][0]
        self.assertIn("score_breakdown", s)
        bd = s["score_breakdown"]
        self.assertIn("htf_alignment", bd)
        self.assertIn("vwap_level_quality", bd)
        self.assertIn("volume_orderflow", bd)
        self.assertIn("macro_alignment", bd)

    def test_sample_has_source_quality(self):
        self.assertIn("source_quality", self.sample)
        sq = self.sample["source_quality"]
        self.assertIn("input_freshness", sq)
        self.assertIn("completeness_pct", sq)

    def test_sample_has_missing_array(self):
        self.assertIn("missing", self.sample)
        self.assertIsInstance(self.sample["missing"], list)

    def test_no_execution_terms(self):
        schema_str = json.dumps(self.schema)
        sample_str = json.dumps(self.sample)
        forbidden = ["execute", "broker", "order_book_exec", "auto_trade", "market_order", "limit_order"]
        for term in forbidden:
            self.assertNotIn(term, schema_str.lower(), f"Forbidden term '{term}' found in schema")
            self.assertNotIn(term, sample_str.lower(), f"Forbidden term '{term}' found in sample")

    def test_setup_direction_no_auto(self):
        """Direction must be monitor_only, long, or short — never 'auto'."""
        for s in self.sample.get("setups", []):
            self.assertIn(s["direction"], {"long", "short", "monitor_only"})
            self.assertNotEqual(s["direction"], "auto")

    def test_grade_enum(self):
        valid_grades = {"A+", "A", "A-", "B+", "B", "B-", "C", "REJECT"}
        for s in self.sample.get("setups", []):
            self.assertIn(s["grade"], valid_grades)


class TestRegistryUpdated(unittest.TestCase):
    def test_contracts_json_has_new_contracts(self):
        registry = json.loads(
            (PROJECT_ROOT / "data" / "data_center" / "_registry" / "contracts.json").read_text()
        )
        self.assertIn("multitf_analysis_input.v1", registry["contracts"])
        self.assertIn("multitf_setup_score.v1", registry["contracts"])
        self.assertIn("analysis", registry["domains"])
        self.assertEqual(registry["summary"]["total_contracts"], 30)
        self.assertEqual(registry["summary"]["total_domains"], 8)

    def test_contract_status_is_proven(self):
        registry = json.loads(
            (PROJECT_ROOT / "data" / "data_center" / "_registry" / "contracts.json").read_text()
        )
        self.assertEqual(registry["contracts"]["multitf_analysis_input.v1"]["status"], "PROVEN")
        self.assertEqual(registry["contracts"]["multitf_setup_score.v1"]["status"], "PROVEN")

    def test_contracts_have_score(self):
        registry = json.loads(
            (PROJECT_ROOT / "data" / "data_center" / "_registry" / "contracts.json").read_text()
        )
        self.assertGreater(registry["contracts"]["multitf_analysis_input.v1"]["score"], 0)
        self.assertGreater(registry["contracts"]["multitf_setup_score.v1"]["score"], 0)

    def test_view_directories_exist(self):
        self.assertTrue(
            (PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_analysis_input.v1").is_dir()
        )
        self.assertTrue(
            (PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_analysis_input.v1" / "by_symbol").is_dir()
        )
        self.assertTrue(
            (PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1").is_dir()
        )
        self.assertTrue(
            (PROJECT_ROOT / "data" / "data_center" / "views" / "multitf_setup_score.v1" / "by_symbol").is_dir()
        )

    def test_producer_contract_exists(self):
        self.assertTrue(
            (PROJECT_ROOT / "data" / "data_center" / "_contracts" / "producers" / "multitf_analysis.v1.json").is_file()
        )


class TestMonitorOnlyInvariances(unittest.TestCase):
    """Cross-contract invariants: no execution, no broker, no auto-order."""

    def test_input_schema_no_execution(self):
        schema = json.loads(
            (PROJECT_ROOT / "modules" / "data_center" / "contracts" / "multitf_analysis_input.v1.schema.json").read_text()
        )
        forbidden = ["execute", "broker", "position_open", "entry_order", "stop_order", "limit_order"]
        text = json.dumps(schema).lower()
        for term in forbidden:
            self.assertNotIn(term, text, f"multitf_analysis_input schema contains forbidden term: {term}")

    def test_output_schema_no_execution(self):
        schema = json.loads(
            (PROJECT_ROOT / "modules" / "data_center" / "contracts" / "multitf_setup_score.v1.schema.json").read_text()
        )
        forbidden = ["execute", "broker", "position_open", "entry_order", "stop_order", "limit_order"]
        text = json.dumps(schema).lower()
        for term in forbidden:
            self.assertNotIn(term, text, f"multitf_setup_score schema contains forbidden term: {term}")

    def test_producer_contract_monitor_only(self):
        producer = json.loads(
            (PROJECT_ROOT / "data" / "data_center" / "_contracts" / "producers" / "multitf_analysis.v1.json").read_text()
        )
        guards = producer.get("runtime_guards", {})
        self.assertTrue(guards.get("monitor_only"), "Producer must be monitor_only")
        self.assertTrue(guards.get("no_execution"), "Producer must have no_execution flag")
