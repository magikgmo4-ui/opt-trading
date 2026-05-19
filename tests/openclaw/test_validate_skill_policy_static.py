#!/usr/bin/env python3
"""Tests for the warning-only OpenClaw skill policy static validator.

These tests intentionally use only the Python standard library.
They do not execute OpenClaw runtime actions and do not mutate project files.
"""

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
VALIDATOR_PATH = REPO_ROOT / "tools" / "openclaw" / "validate_skill_policy_static.py"
POLICY_PATH = REPO_ROOT / "configs" / "openclaw" / "security" / "skill_policy.yaml"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_skill_policy_static", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load validator module: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SkillPolicyStaticValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator_module()

    def test_real_policy_warning_only_exit_zero(self) -> None:
        self.assertTrue(POLICY_PATH.exists(), f"Missing policy fixture: {POLICY_PATH}")
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = self.validator.main(["--policy", str(POLICY_PATH)])
        report = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("mode: WARNING_ONLY", report)
        self.assertIn("runtime_execution: DISABLED", report)
        self.assertIn("mutation: DISABLED", report)

    def test_real_policy_json_report_exit_zero(self) -> None:
        self.assertTrue(POLICY_PATH.exists(), f"Missing policy fixture: {POLICY_PATH}")
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = self.validator.main(["--policy", str(POLICY_PATH), "--format", "json"])
        self.assertEqual(exit_code, 0)
        report = json.loads(output.getvalue())
        self.assertEqual(report["validator"], "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR")
        self.assertEqual(report["mode"], "WARNING_ONLY")
        self.assertEqual(report["runtime_execution"], "DISABLED")
        self.assertEqual(report["mutation"], "DISABLED")
        self.assertIn("findings_count", report)
        self.assertIsInstance(report["findings"], list)

    def test_missing_policy_still_exit_zero_by_default(self) -> None:
        missing_path = Path(tempfile.gettempdir()) / "missing_openclaw_skill_policy.yaml"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = self.validator.main(["--policy", str(missing_path)])
        report = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("WARN: POLICY_NOT_FOUND", report)

    def test_missing_policy_json_report_still_exit_zero_by_default(self) -> None:
        missing_path = Path(tempfile.gettempdir()) / "missing_openclaw_skill_policy.yaml"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = self.validator.main(["--policy", str(missing_path), "--format", "json"])
        self.assertEqual(exit_code, 0)
        report = json.loads(output.getvalue())
        self.assertEqual(report["findings_count"], 1)
        self.assertEqual(report["findings"][0]["code"], "POLICY_NOT_FOUND")

    def test_missing_policy_strict_exit_returns_one(self) -> None:
        missing_path = Path(tempfile.gettempdir()) / "missing_openclaw_skill_policy.yaml"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = self.validator.main(["--policy", str(missing_path), "--strict-exit"])
        report = output.getvalue()
        self.assertEqual(exit_code, 1)
        self.assertIn("WARN: POLICY_NOT_FOUND", report)

    def test_detects_unsafe_defaults_without_mutation(self) -> None:
        unsafe_policy = """
policy_version: "0.1"
policy_id: "UNSAFE_TEST_POLICY"
status: "draft"
owner_go: "GO_TEST"
parent_go: "GO_PARENT"
runtime_execution_enabled: true
warning_only_default: false
default_mode: "EXECUTE"
validation_mode: "RUNTIME_GATED"
can_fail_ci: true
can_autofix: true
permission_levels:
  L0_READ_ONLY: {}
surfaces:
  DOCS: {}
confirmation: {}
audit: {}
promotion: {}
static_validation: {}
"""
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as handle:
            handle.write(unsafe_policy)
            temp_path = Path(handle.name)
        try:
            findings = self.validator.validate_policy_text(temp_path.read_text(encoding="utf-8"), temp_path)
            codes = {finding.code for finding in findings}
            self.assertIn("RUNTIME_EXECUTION_ENABLED", codes)
            self.assertIn("BLOCKING_CI_ENABLED", codes)
            self.assertIn("AUTOFIX_ENABLED", codes)
            self.assertIn("UNSAFE_DEFAULT", codes)
            self.assertTrue(temp_path.exists(), "Validator must not delete or mutate fixture files")
        finally:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
