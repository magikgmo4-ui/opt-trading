#!/usr/bin/env python3
"""Tests for the warning-only OpenClaw runtime/security validation aggregator."""

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
AGGREGATOR_PATH = REPO_ROOT / "tools" / "openclaw" / "validate_runtime_security_all.py"

CLEAN_POLICY_TEXT = """policy_version: \"0.1\"
policy_id: \"OPENCLAW_RUNTIME_SECURITY_POLICY\"
status: \"draft\"
owner_go: \"GO_TEST\"
parent_go: \"GO_PARENT\"
runtime_execution_enabled: false
warning_only_default: true
default_mode: READ_ONLY
validation_mode: WARNING_ONLY
can_fail_ci: false
can_autofix: false
permission_levels:
  L0_READ_ONLY: {}
  L1_ANALYZE: {}
  L2_PLAN: {}
  L3_PROPOSE_PATCH: {}
  L4_WRITE_DOC: {}
  L5_WRITE_CODE: {}
  L6_EXECUTE_SAFE: {}
  L7_EXECUTE_RISKY: {}
  L8_DESTRUCTIVE: {}
surfaces:
  DOCS: {}
  REPO_CODE: {}
  GIT:
    force_operations_blocked_default: true
  SERVICES: {}
  TELEGRAM: {}
  WORKERS: {}
  FILESYSTEM:
    delete_blocked_default: true
  NETWORK: {}
  SECRETS:
    values_read_blocked: true
  MACHINE_OPS: {}
  TRADING_RUNTIME:
    order_execution_blocked_default: true
confirmation: {}
audit: {}
promotion: {}
static_validation: {}
"""


def load_module(module_name: str, module_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RuntimeSecurityValidationAggregatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.aggregator = load_module("validate_runtime_security_all", AGGREGATOR_PATH)

    def run_aggregator(self, policy_path: Path, policy_report_path: Path, summary_report_path: Path, *extra_args: str) -> tuple[int, str]:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = self.aggregator.main(
                [
                    "--policy",
                    str(policy_path),
                    "--policy-report",
                    str(policy_report_path),
                    "--summary-report",
                    str(summary_report_path),
                    *extra_args,
                ]
            )
        return exit_code, output.getvalue()

    def test_aggregator_returns_zero_by_default_and_writes_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            policy_path = temp_root / "skill_policy.yaml"
            policy_report_path = temp_root / "openclaw-skill-policy-report.json"
            summary_report_path = temp_root / "openclaw-runtime-security-validation-summary.json"
            policy_path.write_text(CLEAN_POLICY_TEXT, encoding="utf-8")

            exit_code, raw_output = self.run_aggregator(policy_path, policy_report_path, summary_report_path, "--format", "json")
            report = json.loads(raw_output)

            self.assertEqual(exit_code, 0)
            self.assertEqual(report["mode"], "WARNING_ONLY")
            self.assertEqual(report["runtime_execution"], "DISABLED")
            self.assertEqual(report["mutation"], "DISABLED")
            self.assertEqual(report["validators_count"], 2)
            self.assertEqual(report["findings_count"], len(report["findings"]))
            self.assertEqual(
                report["validators"],
                [
                    "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR",
                    "OPENCLAW_SKILL_POLICY_JSON_REPORT_SCHEMA_VALIDATOR",
                ],
            )
            self.assertTrue(policy_report_path.exists())
            self.assertTrue(summary_report_path.exists())
            self.assertEqual(json.loads(summary_report_path.read_text(encoding="utf-8")), report)

    def test_both_validators_are_represented_in_consolidated_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            policy_path = temp_root / "skill_policy.yaml"
            policy_report_path = temp_root / "openclaw-skill-policy-report.json"
            summary_report_path = temp_root / "openclaw-runtime-security-validation-summary.json"
            policy_path.write_text(CLEAN_POLICY_TEXT, encoding="utf-8")

            exit_code, raw_output = self.run_aggregator(policy_path, policy_report_path, summary_report_path, "--format", "json")
            report = json.loads(raw_output)

            self.assertEqual(exit_code, 0)
            self.assertIn("skill_policy_static", report["reports"])
            self.assertIn("policy_json_report_schema", report["reports"])
            self.assertEqual(report["reports"]["skill_policy_static"]["validator"], "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR")
            self.assertEqual(
                report["reports"]["policy_json_report_schema"]["validator"],
                "OPENCLAW_SKILL_POLICY_JSON_REPORT_SCHEMA_VALIDATOR",
            )
            self.assertEqual(
                report["reports"]["policy_json_report_schema"]["report_path"],
                str(policy_report_path),
            )

    def test_strict_exit_returns_zero_when_no_findings_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            policy_path = temp_root / "skill_policy.yaml"
            policy_report_path = temp_root / "openclaw-skill-policy-report.json"
            summary_report_path = temp_root / "openclaw-runtime-security-validation-summary.json"
            policy_path.write_text(CLEAN_POLICY_TEXT, encoding="utf-8")

            exit_code, raw_output = self.run_aggregator(
                policy_path,
                policy_report_path,
                summary_report_path,
                "--format",
                "json",
                "--strict-exit",
            )
            report = json.loads(raw_output)

            self.assertEqual(exit_code, 0)
            self.assertEqual(report["findings_count"], 0)

    def test_strict_exit_returns_one_only_when_finding_is_simulated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            policy_path = temp_root / "missing_skill_policy.yaml"
            policy_report_path = temp_root / "openclaw-skill-policy-report.json"
            summary_report_path = temp_root / "openclaw-runtime-security-validation-summary.json"

            exit_code, raw_output = self.run_aggregator(
                policy_path,
                policy_report_path,
                summary_report_path,
                "--format",
                "json",
                "--strict-exit",
            )
            report = json.loads(raw_output)

            self.assertEqual(exit_code, 1)
            self.assertEqual(report["mode"], "WARNING_ONLY")
            self.assertEqual(report["runtime_execution"], "DISABLED")
            self.assertEqual(report["mutation"], "DISABLED")
            self.assertEqual(report["findings_count"], len(report["findings"]))
            self.assertGreater(report["findings_count"], 0)
            self.assertEqual(report["findings"][0]["validator"], "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR")
            self.assertEqual(report["findings"][0]["code"], "POLICY_NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
