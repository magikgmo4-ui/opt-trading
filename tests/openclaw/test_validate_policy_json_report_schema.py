#!/usr/bin/env python3
"""Tests for the warning-only OpenClaw policy JSON report schema validator."""

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = REPO_ROOT / "tools" / "openclaw" / "validate_policy_json_report_schema.py"

LEGACY_BASELINE_REPORT = {
    "findings": [],
    "findings_count": 0,
    "mode": "WARNING_ONLY",
    "mutation": "DISABLED",
    "policy_path": "configs/openclaw/security/skill_policy.yaml",
    "runtime_execution": "DISABLED",
    "validator": "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR",
}

VALID_SCHEMA_1_0_REPORT = {
    "schema_version": "1.0",
    "validator": "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR",
    "policy_path": "configs/openclaw/security/skill_policy.yaml",
    "mode": "WARNING_ONLY",
    "runtime_execution": "DISABLED",
    "mutation": "DISABLED",
    "findings_count": 1,
    "findings": [
        {
            "level": "WARNING",
            "code": "SKILL_POLICY_PATH_SCOPE_WARNING",
            "message": "path scope should be narrowed",
        }
    ],
}


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_policy_json_report_schema", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load validator module: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PolicyJsonReportSchemaValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator_module()

    def run_validator(self, payload: dict[str, object], *extra_args: str) -> tuple[int, str]:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump(payload, handle)
            temp_path = Path(handle.name)
        try:
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = self.validator.main(["--report", str(temp_path), *extra_args])
            return exit_code, output.getvalue()
        finally:
            temp_path.unlink(missing_ok=True)

    def test_legacy_baseline_report_is_accepted(self) -> None:
        exit_code, raw_output = self.run_validator(LEGACY_BASELINE_REPORT, "--format", "json")
        report = json.loads(raw_output)
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["report_contract"], "legacy_baseline")
        self.assertIsNone(report["source_schema_version"])
        self.assertEqual(report["findings_count"], 0)

    def test_schema_1_0_report_is_accepted(self) -> None:
        exit_code, raw_output = self.run_validator(VALID_SCHEMA_1_0_REPORT, "--format", "json")
        report = json.loads(raw_output)
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["report_contract"], "schema_1_0")
        self.assertEqual(report["source_schema_version"], "1.0")
        self.assertEqual(report["findings_count"], 0)

    def test_inconsistent_findings_count_is_detected(self) -> None:
        payload = dict(VALID_SCHEMA_1_0_REPORT)
        payload["findings_count"] = 2
        exit_code, raw_output = self.run_validator(payload, "--format", "json")
        report = json.loads(raw_output)
        codes = {finding["code"] for finding in report["findings"]}
        self.assertEqual(exit_code, 0)
        self.assertIn("INCONSISTENT_FINDINGS_COUNT", codes)

    def test_missing_required_field_is_detected(self) -> None:
        payload = dict(LEGACY_BASELINE_REPORT)
        del payload["mode"]
        exit_code, raw_output = self.run_validator(payload, "--format", "json")
        report = json.loads(raw_output)
        codes = {finding["code"] for finding in report["findings"]}
        self.assertEqual(exit_code, 0)
        self.assertIn("MISSING_REQUIRED_FIELD", codes)

    def test_incomplete_finding_is_detected(self) -> None:
        payload = dict(VALID_SCHEMA_1_0_REPORT)
        payload["findings"] = [{"level": "WARNING", "message": "missing stable code"}]
        exit_code, raw_output = self.run_validator(payload, "--format", "json")
        report = json.loads(raw_output)
        codes = {finding["code"] for finding in report["findings"]}
        self.assertEqual(exit_code, 0)
        self.assertIn("FINDING_MISSING_FIELD", codes)

    def test_non_warning_only_mode_is_detected(self) -> None:
        payload = dict(LEGACY_BASELINE_REPORT)
        payload["mode"] = "STRICT"
        exit_code, raw_output = self.run_validator(payload, "--format", "json")
        report = json.loads(raw_output)
        codes = {finding["code"] for finding in report["findings"]}
        self.assertEqual(exit_code, 0)
        self.assertIn("INVALID_MODE", codes)

    def test_default_output_stays_warning_only_with_exit_zero(self) -> None:
        payload = dict(LEGACY_BASELINE_REPORT)
        payload["mode"] = "STRICT"
        exit_code, raw_output = self.run_validator(payload)
        self.assertEqual(exit_code, 0)
        self.assertIn("mode: WARNING_ONLY", raw_output)
        self.assertIn("runtime_execution: DISABLED", raw_output)
        self.assertIn("mutation: DISABLED", raw_output)
        self.assertIn("WARN: INVALID_MODE", raw_output)

    def test_strict_exit_returns_one_when_findings_exist(self) -> None:
        payload = dict(LEGACY_BASELINE_REPORT)
        payload["mode"] = "STRICT"
        exit_code, raw_output = self.run_validator(payload, "--strict-exit")
        self.assertEqual(exit_code, 1)
        self.assertIn("WARN: INVALID_MODE", raw_output)


if __name__ == "__main__":
    unittest.main()
