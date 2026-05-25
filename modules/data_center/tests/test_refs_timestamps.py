import json
import unittest
from pathlib import Path

from modules.data_center.refs_timestamps import (
    now_utc_z,
    build_refs,
    enrich_produced_at,
    validate_iso_utc,
    is_compatible_legacy,
)


class TestNowUtcZ(unittest.TestCase):
    def test_returns_string(self):
        result = now_utc_z()
        self.assertIsInstance(result, str)

    def test_ends_with_z(self):
        result = now_utc_z()
        self.assertTrue(result.endswith("Z"), f"Expected Z suffix, got {result!r}")

    def test_is_valid_iso(self):
        result = now_utc_z()
        self.assertTrue(validate_iso_utc(result), f"Not valid ISO UTC: {result!r}")


class TestBuildRefs(unittest.TestCase):
    def test_builds_with_primary_output(self):
        refs = build_refs(primary_output="data/dc/spot/latest.json")
        self.assertEqual(refs["primary_output"], "data/dc/spot/latest.json")

    def test_excludes_none_values(self):
        refs = build_refs(primary_output="a.json", latest=None)
        self.assertNotIn("latest", refs)

    def test_includes_extra_kwargs(self):
        refs = build_refs(telegram_message_ref="fixture://tg/ch/001")
        self.assertEqual(refs["telegram_message_ref"], "fixture://tg/ch/001")

    def test_empty_refs(self):
        refs = build_refs()
        self.assertEqual(refs, {})

    def test_all_fields(self):
        refs = build_refs(primary_output="p.json", latest="l.json", status="s.json")
        self.assertIn("primary_output", refs)
        self.assertIn("latest", refs)
        self.assertIn("status", refs)


class TestEnrichProducedAt(unittest.TestCase):
    def test_adds_produced_at_if_absent(self):
        payload = {"entity_type": "pair_market_snapshot"}
        result = enrich_produced_at(payload)
        self.assertIn("produced_at", result)

    def test_does_not_overwrite_existing(self):
        payload = {"produced_at": "2026-01-01T00:00:00Z"}
        result = enrich_produced_at(payload)
        self.assertEqual(result["produced_at"], "2026-01-01T00:00:00Z")

    def test_does_not_modify_original(self):
        payload = {"entity_type": "x"}
        enrich_produced_at(payload)
        self.assertNotIn("produced_at", payload)

    def test_uses_explicit_produced_at(self):
        payload = {"entity_type": "x"}
        result = enrich_produced_at(payload, produced_at="2026-05-25T00:00:00Z")
        self.assertEqual(result["produced_at"], "2026-05-25T00:00:00Z")

    def test_produced_at_is_valid_iso(self):
        result = enrich_produced_at({"x": 1})
        self.assertTrue(validate_iso_utc(result["produced_at"]))


class TestValidateIsoUtc(unittest.TestCase):
    def test_valid_z_suffix(self):
        self.assertTrue(validate_iso_utc("2026-05-25T00:00:00Z"))

    def test_valid_plus_offset(self):
        self.assertTrue(validate_iso_utc("2026-05-25T00:00:00+00:00"))

    def test_invalid_no_utc(self):
        self.assertFalse(validate_iso_utc("2026-05-25T00:00:00"))

    def test_invalid_not_string(self):
        self.assertFalse(validate_iso_utc(1234567890))

    def test_invalid_garbage(self):
        self.assertFalse(validate_iso_utc("not-a-date"))


class TestIsCompatibleLegacy(unittest.TestCase):
    def test_market_metrics_fixture_is_compatible(self):
        fixtures = Path("tests/fixtures/admin_trading_contract_smoke")
        path = fixtures / "market_metrics_v1_minimal.json"
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            ok, warnings = is_compatible_legacy(payload)
            self.assertTrue(ok, f"market_metrics fixture not compatible: {warnings}")

    def test_pair_snapshot_fixture_is_compatible(self):
        payload = {
            "entity_type": "pair_market_snapshot",
            "generated_at": "2026-05-25T00:00:00Z",
            "records": [],
        }
        ok, warnings = is_compatible_legacy(payload)
        self.assertTrue(ok)

    def test_vision_analysis_fixture_is_compatible(self):
        payload = {
            "input_class": "vision_analysis.v1",
            "analysis_ts": "2026-05-25T00:00:00Z",
        }
        ok, warnings = is_compatible_legacy(payload)
        self.assertTrue(ok)

    def test_telegram_claim_fixture_is_compatible(self):
        payload = {"input_class": "telegram_claim.v1", "claim_ts": "2026-05-25T00:00:00Z"}
        ok, warnings = is_compatible_legacy(payload)
        self.assertTrue(ok)

    def test_payload_with_no_ts_fields_warns(self):
        payload = {"input_class": "future.v1", "data": "no timestamps here"}
        ok, warnings = is_compatible_legacy(payload)
        self.assertFalse(ok)
        self.assertTrue(len(warnings) > 0)


if __name__ == "__main__":
    unittest.main()
