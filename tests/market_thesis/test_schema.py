"""
Tests for schemas/market_thesis_v1.json — JSON Schema Draft 2020-12 validation.

Covers:
- Schema is valid JSON and conforms to Draft 2020-12
- Canonical BTC example validates against the schema
- Invalid payloads are rejected
- Required fields enforcement
- Probability bounds enforcement
- Readiness locked to monitor_only
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import jsonschema

from modules.market_thesis.models import CANONICAL_BTC_THESIS

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "market_thesis_v1.json"


def load_schema() -> dict:
    with open(SCHEMA_PATH) as f:
        return json.load(f)


class TestJSONSchemaValid(unittest.TestCase):
    """JSON Schema structural validity."""

    def test_schema_is_valid_json(self):
        schema = load_schema()
        self.assertIsInstance(schema, dict)

    def test_schema_has_draft_2020_12(self):
        schema = load_schema()
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_schema_self_validates(self):
        schema = load_schema()
        jsonschema.Draft202012Validator.check_schema(schema)

    def test_canonical_btc_validates(self):
        schema = load_schema()
        payload = CANONICAL_BTC_THESIS.model_dump(by_alias=True, mode="json")
        jsonschema.validate(payload, schema, cls=jsonschema.Draft202012Validator)


class TestJSONSchemaRequiredFields(unittest.TestCase):
    """Required fields enforcement."""

    def setUp(self):
        self.schema = load_schema()
        self.valid = CANONICAL_BTC_THESIS.model_dump(by_alias=True, mode="json")

    def validate(self, payload: dict):
        jsonschema.validate(payload, self.schema, cls=jsonschema.Draft202012Validator)

    def test_missing_metadata_rejected(self):
        payload = dict(self.valid)
        del payload["metadata"]
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_missing_symbol_rejected(self):
        payload = dict(self.valid)
        del payload["symbol"]
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_missing_probabilities_rejected(self):
        payload = dict(self.valid)
        del payload["probabilities"]
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_missing_freshness_rejected(self):
        payload = dict(self.valid)
        del payload["freshness"]
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_missing_confidence_rejected(self):
        payload = dict(self.valid)
        del payload["confidence"]
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_missing_metadata_thesis_id_rejected(self):
        payload = dict(self.valid)
        del payload["metadata"]["thesis_id"]
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)


class TestJSONSchemaBoundedFields(unittest.TestCase):
    """Field boundary enforcement."""

    def setUp(self):
        self.schema = load_schema()

    def validate(self, payload: dict):
        jsonschema.validate(payload, self.schema, cls=jsonschema.Draft202012Validator)

    def _base(self) -> dict:
        return CANONICAL_BTC_THESIS.model_dump(by_alias=True, mode="json")

    def test_confidence_negative_rejected(self):
        payload = self._base()
        payload["confidence"] = -1
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_confidence_101_rejected(self):
        payload = self._base()
        payload["confidence"] = 101
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_probability_bull_negative_rejected(self):
        payload = self._base()
        payload["probabilities"]["bull"] = -1
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_probability_bear_101_rejected(self):
        payload = self._base()
        payload["probabilities"]["bear"] = 101
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_action_not_monitor_only_rejected(self):
        payload = self._base()
        payload["action"]["readiness"] = "ready"
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_ttl_below_minimum_rejected(self):
        payload = self._base()
        payload["metadata"]["ttl_seconds"] = 5
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_sentiment_score_out_of_range_rejected(self):
        payload = self._base()
        payload["news"]["sentiment_score"] = 1.5
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)

    def test_freshness_overall_invalid_rejected(self):
        payload = self._base()
        payload["freshness"]["overall"] = "ancient"
        with self.assertRaises(jsonschema.ValidationError):
            self.validate(payload)


class TestJSONSchemaAllNineSymbols(unittest.TestCase):
    """All 9 target symbols produce valid theses against schema."""

    @classmethod
    def setUpClass(cls):
        cls.schema = load_schema()

    def _make_thesis(self, sym: str) -> dict:
        from modules.market_thesis.models import (
            FreshnessStatus,
            MarketThesis,
            ProbabilitySet,
            ThesisMetadata,
        )
        t = MarketThesis(
            metadata=ThesisMetadata(thesis_id=f"thesis_{sym}_01"),
            symbol=sym,
            probabilities=ProbabilitySet(bull=33, range=34, bear=33),
            freshness=FreshnessStatus(overall="fresh", max_age_minutes=0, source_count=1, fresh_count=1),
            confidence=50,
        )
        return t.model_dump(by_alias=True, mode="json")

    def test_BTC(self):
        jsonschema.validate(self._make_thesis("BTC"), self.schema, cls=jsonschema.Draft202012Validator)

    def test_ETH(self):
        jsonschema.validate(self._make_thesis("ETH"), self.schema, cls=jsonschema.Draft202012Validator)

    def test_SOL(self):
        jsonschema.validate(self._make_thesis("SOL"), self.schema, cls=jsonschema.Draft202012Validator)

    def test_XRP(self):
        jsonschema.validate(self._make_thesis("XRP"), self.schema, cls=jsonschema.Draft202012Validator)

    def test_XAU(self):
        jsonschema.validate(self._make_thesis("XAU"), self.schema, cls=jsonschema.Draft202012Validator)

    def test_SPCX(self):
        jsonschema.validate(self._make_thesis("SPCX"), self.schema, cls=jsonschema.Draft202012Validator)

    def test_NVDA(self):
        jsonschema.validate(self._make_thesis("NVDA"), self.schema, cls=jsonschema.Draft202012Validator)

    def test_AVGO(self):
        jsonschema.validate(self._make_thesis("AVGO"), self.schema, cls=jsonschema.Draft202012Validator)

    def test_MU(self):
        jsonschema.validate(self._make_thesis("MU"), self.schema, cls=jsonschema.Draft202012Validator)


class TestJSONSchemaRiskSeverityEnum(unittest.TestCase):
    """Risk severity enum enforcement."""

    def setUp(self):
        self.schema = load_schema()

    def test_valid_severities(self):
        payload = CANONICAL_BTC_THESIS.model_dump(by_alias=True, mode="json")
        payload["risks"] = [
            {"category": "technical", "severity": "high", "description": "Risque élevé."},
            {"category": "event", "severity": "moderate", "description": "Risque modéré."},
            {"category": "regulatory", "severity": "low", "description": "Risque faible."},
        ]
        jsonschema.validate(payload, self.schema, cls=jsonschema.Draft202012Validator)

    def test_invalid_severity_rejected(self):
        payload = CANONICAL_BTC_THESIS.model_dump(by_alias=True, mode="json")
        payload["risks"] = [
            {"category": "technical", "severity": "critical", "description": "Risque critique."},
        ]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(payload, self.schema, cls=jsonschema.Draft202012Validator)


class TestJSONSchemaSourceRef(unittest.TestCase):
    """SourceRef validation."""

    def setUp(self):
        self.schema = load_schema()

    def test_valid_sources(self):
        payload = CANONICAL_BTC_THESIS.model_dump(by_alias=True, mode="json")
        jsonschema.validate(payload, self.schema, cls=jsonschema.Draft202012Validator)

    def test_invalid_source_status_rejected(self):
        payload = CANONICAL_BTC_THESIS.model_dump(by_alias=True, mode="json")
        payload["sources"][0]["status"] = "unknown"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(payload, self.schema, cls=jsonschema.Draft202012Validator)


if __name__ == "__main__":
    unittest.main()
