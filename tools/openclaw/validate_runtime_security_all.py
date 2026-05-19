#!/usr/bin/env python3
"""Warning-only aggregator for OpenClaw runtime/security validations.

Scope:
- reads the OpenClaw skill policy YAML only;
- runs the existing static validator internally;
- validates the generated JSON report against the canonical schema validator;
- writes explicit JSON report artifacts only;
- does not execute runtime actions;
- does not call services or secrets;
- always exits 0 by default to remain warning-only.

GO: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_COMMAND_01
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Literal

DEFAULT_POLICY_PATH = Path("configs/openclaw/security/skill_policy.yaml")
DEFAULT_POLICY_REPORT_PATH = Path("openclaw-skill-policy-report.json")
DEFAULT_SUMMARY_REPORT_PATH = Path("openclaw-runtime-security-validation-summary.json")
STATIC_VALIDATOR_PATH = Path(__file__).with_name("validate_skill_policy_static.py")
SCHEMA_VALIDATOR_PATH = Path(__file__).with_name("validate_policy_json_report_schema.py")
VALIDATOR_NAME = "OPENCLAW_RUNTIME_SECURITY_VALIDATION_AGGREGATOR"
OutputFormat = Literal["text", "json"]


def _load_module(module_name: str, module_path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load validator module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _ensure_parent_dir(path: Path) -> None:
    if path.parent != Path(""):
        path.parent.mkdir(parents=True, exist_ok=True)


def _write_json_artifact(path: Path, payload: dict[str, object]) -> None:
    _ensure_parent_dir(path)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _collect_static_report(static_validator: Any, policy_path: Path) -> dict[str, object]:
    if policy_path.exists():
        policy_text = policy_path.read_text(encoding="utf-8")
        findings = static_validator.validate_policy_text(policy_text, policy_path)
    else:
        findings = [static_validator.Finding("WARN", "POLICY_NOT_FOUND", f"Policy file not found: {policy_path}")]
    return static_validator.build_report(findings, policy_path)


def _collect_schema_report(schema_validator: Any, policy_report: dict[str, object], policy_report_path: Path) -> dict[str, object]:
    validation_result = schema_validator.validate_report_object(policy_report, policy_report_path)
    return schema_validator.build_validation_report(validation_result, policy_report_path)


def _flatten_findings(report: dict[str, object]) -> list[dict[str, str]]:
    validator_name = str(report.get("validator", "UNKNOWN_VALIDATOR"))
    findings = report.get("findings")
    flattened: list[dict[str, str]] = []
    if not isinstance(findings, list):
        return flattened
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        flattened.append(
            {
                "validator": validator_name,
                "level": str(finding.get("level", "WARN")),
                "code": str(finding.get("code", "UNKNOWN_FINDING")),
                "message": str(finding.get("message", "Missing finding message.")),
            }
        )
    return flattened


def build_summary_report(
    policy_path: Path,
    policy_report_path: Path,
    summary_report_path: Path,
    static_report: dict[str, object],
    schema_report: dict[str, object],
) -> dict[str, object]:
    findings = _flatten_findings(static_report) + _flatten_findings(schema_report)
    return {
        "validator": VALIDATOR_NAME,
        "policy_path": str(policy_path),
        "policy_report_path": str(policy_report_path),
        "summary_report_path": str(summary_report_path),
        "mode": "WARNING_ONLY",
        "runtime_execution": "DISABLED",
        "mutation": "DISABLED",
        "validators_count": 2,
        "validators": [
            str(static_report.get("validator", "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR")),
            str(schema_report.get("validator", "OPENCLAW_SKILL_POLICY_JSON_REPORT_SCHEMA_VALIDATOR")),
        ],
        "findings_count": len(findings),
        "findings": findings,
        "reports": {
            "skill_policy_static": static_report,
            "policy_json_report_schema": schema_report,
        },
    }


def render_text_report(summary_report: dict[str, object]) -> str:
    lines = [
        str(summary_report["validator"]),
        f"policy_path: {summary_report['policy_path']}",
        f"policy_report_path: {summary_report['policy_report_path']}",
        f"summary_report_path: {summary_report['summary_report_path']}",
        f"mode: {summary_report['mode']}",
        f"runtime_execution: {summary_report['runtime_execution']}",
        f"mutation: {summary_report['mutation']}",
        f"validators_count: {summary_report['validators_count']}",
        f"findings_count: {summary_report['findings_count']}",
        "",
    ]
    validators = summary_report.get("validators", [])
    if isinstance(validators, list):
        for validator_name in validators:
            lines.append(f"validator: {validator_name}")
    findings = summary_report.get("findings", [])
    if not findings:
        lines.append("PASS_WITH_WARNINGS_0: all configured runtime/security validations passed in warning-only mode")
        return "\n".join(lines)
    for finding in findings:
        lines.append(
            f"{finding['validator']}: {finding['level']}: {finding['code']}: {finding['message']}"
        )
    return "\n".join(lines)


def render_json_report(summary_report: dict[str, object]) -> str:
    return json.dumps(summary_report, indent=2, sort_keys=True)


def run_all_validations(
    policy_path: Path,
    policy_report_path: Path,
    summary_report_path: Path,
) -> dict[str, object]:
    static_validator = _load_module("openclaw_validate_skill_policy_static_for_aggregator", STATIC_VALIDATOR_PATH)
    schema_validator = _load_module("openclaw_validate_policy_json_report_schema_for_aggregator", SCHEMA_VALIDATOR_PATH)

    static_report = _collect_static_report(static_validator, policy_path)
    _write_json_artifact(policy_report_path, static_report)

    schema_report = _collect_schema_report(schema_validator, static_report, policy_report_path)
    summary_report = build_summary_report(policy_path, policy_report_path, summary_report_path, static_report, schema_report)
    _write_json_artifact(summary_report_path, summary_report)
    return summary_report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Warning-only OpenClaw runtime/security validation aggregator.")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH, help=f"Policy YAML path. Default: {DEFAULT_POLICY_PATH}")
    parser.add_argument(
        "--policy-report",
        type=Path,
        default=DEFAULT_POLICY_REPORT_PATH,
        help=f"Generated policy JSON report path. Default: {DEFAULT_POLICY_REPORT_PATH}",
    )
    parser.add_argument(
        "--summary-report",
        type=Path,
        default=DEFAULT_SUMMARY_REPORT_PATH,
        help=f"Consolidated summary JSON report path. Default: {DEFAULT_SUMMARY_REPORT_PATH}",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format. Default: text")
    parser.add_argument("--strict-exit", action="store_true", help="Return 1 when aggregated findings exist.")
    return parser.parse_args(argv)


def _render(summary_report: dict[str, object], output_format: OutputFormat) -> str:
    if output_format == "json":
        return render_json_report(summary_report)
    return render_text_report(summary_report)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(sys.argv[1:] if argv is None else argv))
    summary_report = run_all_validations(args.policy, args.policy_report, args.summary_report)
    print(_render(summary_report, args.format))
    return 1 if args.strict_exit and int(summary_report["findings_count"]) > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
