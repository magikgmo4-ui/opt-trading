#!/usr/bin/env python3
"""Warning-only schema validator for OpenClaw policy JSON reports.

Scope:
- reads a JSON report file only;
- validates the report against the documented canonical contract;
- explicitly accepts the observed unversioned legacy baseline;
- validates future reports with schema_version "1.0";
- does not execute runtime actions;
- does not mutate files;
- always exits 0 by default to remain warning-only.

GO: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

DEFAULT_REPORT_PATH = Path("openclaw-skill-policy-report.json")
CANONICAL_SCHEMA_VERSION = "1.0"
EXPECTED_REPORT_VALIDATOR = "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR"
VALIDATOR_NAME = "OPENCLAW_SKILL_POLICY_JSON_REPORT_SCHEMA_VALIDATOR"
REQUIRED_TOP_LEVEL_FIELDS = (
    "validator",
    "policy_path",
    "mode",
    "runtime_execution",
    "mutation",
    "findings_count",
    "findings",
)
REQUIRED_FINDING_FIELDS = ("level", "code", "message")
OutputFormat = Literal["text", "json"]


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    report_contract: str
    source_schema_version: str | None
    findings: list[Finding]


def _warn(findings: list[Finding], code: str, message: str) -> None:
    findings.append(Finding("WARN", code, message))


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_report_object(report: Any, report_path: Path) -> ValidationResult:
    findings: list[Finding] = []

    if not isinstance(report, dict):
        _warn(findings, "INVALID_REPORT_TYPE", "Report root must be a JSON object.")
        return ValidationResult("invalid_document", None, findings)

    source_schema_version = report.get("schema_version")
    if source_schema_version is None:
        report_contract = "legacy_baseline"
    elif source_schema_version == CANONICAL_SCHEMA_VERSION:
        report_contract = "schema_1_0"
    elif isinstance(source_schema_version, str):
        report_contract = "unsupported_schema_version"
        _warn(
            findings,
            "UNSUPPORTED_SCHEMA_VERSION",
            f"Unsupported schema_version {source_schema_version!r}; expected {CANONICAL_SCHEMA_VERSION!r} or no schema_version for legacy baseline.",
        )
    else:
        report_contract = "unsupported_schema_version"
        _warn(findings, "INVALID_SCHEMA_VERSION_TYPE", "schema_version must be a string when provided.")

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in report:
            _warn(findings, "MISSING_REQUIRED_FIELD", f"Missing required top-level field: {field}")

    validator_name = report.get("validator")
    if validator_name is not None and validator_name != EXPECTED_REPORT_VALIDATOR:
        _warn(
            findings,
            "UNEXPECTED_VALIDATOR",
            f"validator must be {EXPECTED_REPORT_VALIDATOR!r}; got {validator_name!r}.",
        )

    policy_path = report.get("policy_path")
    if policy_path is not None and not _is_non_empty_string(policy_path):
        _warn(findings, "INVALID_POLICY_PATH", "policy_path must be a non-empty string.")

    expected_scalars = {
        "mode": "WARNING_ONLY",
        "runtime_execution": "DISABLED",
        "mutation": "DISABLED",
    }
    for field, expected_value in expected_scalars.items():
        actual_value = report.get(field)
        if actual_value is not None and actual_value != expected_value:
            _warn(findings, f"INVALID_{field.upper()}", f"{field} must be {expected_value!r}; got {actual_value!r}.")

    findings_value = report.get("findings")
    if findings_value is not None and not isinstance(findings_value, list):
        _warn(findings, "INVALID_FINDINGS_TYPE", "findings must be a list.")
        findings_value = None

    findings_count = report.get("findings_count")
    if findings_count is not None:
        if not isinstance(findings_count, int) or findings_count < 0:
            _warn(findings, "INVALID_FINDINGS_COUNT", "findings_count must be an integer >= 0.")
        elif isinstance(findings_value, list) and findings_count != len(findings_value):
            _warn(
                findings,
                "INCONSISTENT_FINDINGS_COUNT",
                f"findings_count must match len(findings); got {findings_count} and {len(findings_value)}.",
            )

    if isinstance(findings_value, list):
        for index, finding in enumerate(findings_value):
            if not isinstance(finding, dict):
                _warn(findings, "FINDING_NOT_OBJECT", f"finding[{index}] must be an object.")
                continue
            for field in REQUIRED_FINDING_FIELDS:
                if field not in finding:
                    _warn(findings, "FINDING_MISSING_FIELD", f"finding[{index}] missing required field: {field}")
                    continue
                if not _is_non_empty_string(finding[field]):
                    _warn(
                        findings,
                        "FINDING_INVALID_FIELD",
                        f"finding[{index}].{field} must be a non-empty string.",
                    )

    return ValidationResult(report_contract, source_schema_version if isinstance(source_schema_version, str) else None, findings)


def build_validation_report(result: ValidationResult, report_path: Path) -> dict[str, object]:
    return {
        "validator": VALIDATOR_NAME,
        "report_path": str(report_path),
        "schema_target": CANONICAL_SCHEMA_VERSION,
        "report_contract": result.report_contract,
        "source_schema_version": result.source_schema_version,
        "mode": "WARNING_ONLY",
        "runtime_execution": "DISABLED",
        "mutation": "DISABLED",
        "findings_count": len(result.findings),
        "findings": [asdict(item) for item in result.findings],
    }


def render_text_report(result: ValidationResult, report_path: Path) -> str:
    report = build_validation_report(result, report_path)
    lines = [
        str(report["validator"]),
        f"report_path: {report['report_path']}",
        f"schema_target: {report['schema_target']}",
        f"report_contract: {report['report_contract']}",
        f"source_schema_version: {report['source_schema_version']}",
        f"mode: {report['mode']}",
        f"runtime_execution: {report['runtime_execution']}",
        f"mutation: {report['mutation']}",
        f"findings_count: {report['findings_count']}",
        "",
    ]
    if not result.findings:
        lines.append("PASS_WITH_WARNINGS_0: report matches the accepted warning-only schema contract")
        return "\n".join(lines)
    lines.extend(f"{item.level}: {item.code}: {item.message}" for item in result.findings)
    return "\n".join(lines)


def render_json_report(result: ValidationResult, report_path: Path) -> str:
    return json.dumps(build_validation_report(result, report_path), indent=2, sort_keys=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Warning-only OpenClaw policy JSON report schema validator.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT_PATH, help=f"JSON report path. Default: {DEFAULT_REPORT_PATH}")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format. Default: text")
    parser.add_argument("--strict-exit", action="store_true", help="Return 1 when validation findings exist.")
    return parser.parse_args(argv)


def _render(result: ValidationResult, report_path: Path, output_format: OutputFormat) -> str:
    if output_format == "json":
        return render_json_report(result, report_path)
    return render_text_report(result, report_path)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(sys.argv[1:] if argv is None else argv))
    report_path: Path = args.report
    output_format: OutputFormat = args.format

    if not report_path.exists():
        result = ValidationResult(
            report_contract="missing_report",
            source_schema_version=None,
            findings=[Finding("WARN", "REPORT_NOT_FOUND", f"Report file not found: {report_path}")],
        )
        print(_render(result, report_path, output_format))
        return 1 if args.strict_exit else 0

    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result = ValidationResult(
            report_contract="invalid_json",
            source_schema_version=None,
            findings=[Finding("WARN", "INVALID_JSON", f"Invalid JSON in report file: {exc}")],
        )
        print(_render(result, report_path, output_format))
        return 1 if args.strict_exit else 0

    result = validate_report_object(report, report_path)
    print(_render(result, report_path, output_format))
    return 1 if args.strict_exit and result.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
