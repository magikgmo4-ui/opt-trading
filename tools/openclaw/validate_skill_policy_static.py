#!/usr/bin/env python3
"""Warning-only static validator for OpenClaw skill policy drafts.

Scope:
- reads configs/openclaw/security/skill_policy.yaml by default;
- performs conservative text-level checks only;
- does not execute runtime actions;
- does not mutate files;
- does not require PyYAML or external dependencies;
- always exits 0 by default to remain warning-only;
- can render a machine-readable JSON report with --format json.

GO: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_STATIC_VALIDATOR_01
JSON report child: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_REPORT_01
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

DEFAULT_POLICY_PATH = Path("configs/openclaw/security/skill_policy.yaml")
OutputFormat = Literal["text", "json"]


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str


REQUIRED_TOP_LEVEL_KEYS = [
    "policy_version",
    "policy_id",
    "status",
    "owner_go",
    "parent_go",
    "runtime_execution_enabled",
    "warning_only_default",
    "default_mode",
    "validation_mode",
    "can_fail_ci",
    "can_autofix",
    "permission_levels",
    "surfaces",
    "confirmation",
    "audit",
    "promotion",
    "static_validation",
]

REQUIRED_LEVELS = [
    "L0_READ_ONLY",
    "L1_ANALYZE",
    "L2_PLAN",
    "L3_PROPOSE_PATCH",
    "L4_WRITE_DOC",
    "L5_WRITE_CODE",
    "L6_EXECUTE_SAFE",
    "L7_EXECUTE_RISKY",
    "L8_DESTRUCTIVE",
]

REQUIRED_SURFACES = [
    "DOCS",
    "REPO_CODE",
    "GIT",
    "SERVICES",
    "TELEGRAM",
    "WORKERS",
    "FILESYSTEM",
    "NETWORK",
    "SECRETS",
    "MACHINE_OPS",
    "TRADING_RUNTIME",
]

SECURE_DEFAULTS = {
    "runtime_execution_enabled": "false",
    "warning_only_default": "true",
    "default_mode": "READ_ONLY",
    "validation_mode": "WARNING_ONLY",
    "can_fail_ci": "false",
    "can_autofix": "false",
}


def _extract_scalar(text: str, key: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*:\s*['\"]?([^'\"#\n]+)['\"]?\s*(?:#.*)?$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def _contains_key(text: str, key: str) -> bool:
    return re.search(rf"^\s*{re.escape(key)}\s*:", text, re.MULTILINE) is not None


def validate_policy_text(text: str, policy_path: Path) -> list[Finding]:
    findings: list[Finding] = []

    for key in REQUIRED_TOP_LEVEL_KEYS:
        if not _contains_key(text, key):
            findings.append(Finding("WARN", "MISSING_TOP_LEVEL_KEY", f"Missing top-level key: {key}"))

    for level in REQUIRED_LEVELS:
        if not _contains_key(text, level):
            findings.append(Finding("WARN", "MISSING_PERMISSION_LEVEL", f"Missing permission level: {level}"))

    for surface in REQUIRED_SURFACES:
        if not _contains_key(text, surface):
            findings.append(Finding("WARN", "MISSING_SURFACE", f"Missing runtime surface: {surface}"))

    for key, expected in SECURE_DEFAULTS.items():
        actual = _extract_scalar(text, key)
        if actual is None:
            findings.append(Finding("WARN", "MISSING_SECURE_DEFAULT", f"Missing secure default: {key}: {expected}"))
        elif actual.strip('"\'').lower() != expected.lower():
            findings.append(Finding("WARN", "UNSAFE_DEFAULT", f"Unexpected default for {key}: got {actual!r}, expected {expected!r}"))

    fixed_checks = [
        ("values_read_blocked: true", "SECRETS_VALUES_NOT_BLOCKED", "Secrets surface should block value reads."),
        ("order_execution_blocked_default: true", "TRADING_EXECUTION_NOT_BLOCKED", "Trading runtime should block order execution by default."),
        ("force_operations_blocked_default: true", "GIT_FORCE_NOT_BLOCKED", "Git force operations should be blocked by default."),
        ("delete_blocked_default: true", "DELETE_NOT_BLOCKED", "Filesystem delete should be blocked by default."),
    ]
    for needle, code, message in fixed_checks:
        if needle not in text:
            findings.append(Finding("WARN", code, message))

    unsafe_needles = [
        ("runtime_execution_enabled: true", "RUNTIME_EXECUTION_ENABLED", "Policy draft must not enable runtime execution."),
        ("can_fail_ci: true", "BLOCKING_CI_ENABLED", "Static validation must not fail CI in this phase."),
        ("can_autofix: true", "AUTOFIX_ENABLED", "Autofix must remain disabled in this phase."),
    ]
    for needle, code, message in unsafe_needles:
        if needle in text:
            findings.append(Finding("WARN", code, message))

    if not policy_path.name.endswith((".yaml", ".yml")):
        findings.append(Finding("WARN", "UNEXPECTED_EXTENSION", "Policy path should use .yaml or .yml."))

    return findings


def build_report(findings: list[Finding], policy_path: Path) -> dict[str, object]:
    return {
        "validator": "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR",
        "policy_path": str(policy_path),
        "mode": "WARNING_ONLY",
        "runtime_execution": "DISABLED",
        "mutation": "DISABLED",
        "findings_count": len(findings),
        "findings": [asdict(item) for item in findings],
    }


def render_findings(findings: list[Finding], policy_path: Path) -> str:
    report = build_report(findings, policy_path)
    lines = [
        str(report["validator"]),
        f"policy_path: {report['policy_path']}",
        f"mode: {report['mode']}",
        f"runtime_execution: {report['runtime_execution']}",
        f"mutation: {report['mutation']}",
        f"findings_count: {report['findings_count']}",
        "",
    ]
    if not findings:
        lines.append("PASS_WITH_WARNINGS_0: no warning-only findings detected")
        return "\n".join(lines)
    lines.extend(f"{item.level}: {item.code}: {item.message}" for item in findings)
    return "\n".join(lines)


def render_json_report(findings: list[Finding], policy_path: Path) -> str:
    return json.dumps(build_report(findings, policy_path), indent=2, sort_keys=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Warning-only OpenClaw skill policy static validator.")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH, help=f"Policy YAML path. Default: {DEFAULT_POLICY_PATH}")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Report output format. Default: text")
    parser.add_argument("--strict-exit", action="store_true", help="Return 1 when findings exist. Not recommended for the current GO.")
    return parser.parse_args(argv)


def _render(findings: list[Finding], policy_path: Path, output_format: OutputFormat) -> str:
    if output_format == "json":
        return render_json_report(findings, policy_path)
    return render_findings(findings, policy_path)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(sys.argv[1:] if argv is None else argv))
    policy_path: Path = args.policy
    output_format: OutputFormat = args.format

    if not policy_path.exists():
        findings = [Finding("WARN", "POLICY_NOT_FOUND", f"Policy file not found: {policy_path}")]
        print(_render(findings, policy_path, output_format))
        return 1 if args.strict_exit else 0

    text = policy_path.read_text(encoding="utf-8")
    findings = validate_policy_text(text, policy_path)
    print(_render(findings, policy_path, output_format))
    return 1 if args.strict_exit and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
