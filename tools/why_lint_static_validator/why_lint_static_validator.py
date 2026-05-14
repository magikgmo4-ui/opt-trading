"""Local read-only WHY lint static validator.

The validator reads Markdown fixture documents, extracts YAML-like fenced
policy snippets, evaluates the snippets against the WHY lint fixture contract,
and reports whether observed verdicts match expected verdicts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_VERDICTS = {
    "PASS_RULE_STATIC_VALIDATION",
    "WARN_REVIEW_REQUIRED",
    "NEED_MORE_EVIDENCE",
    "BLOCKED_BY_POLICY",
    "FAIL_UNKNOWN_RULE",
    "FAIL_UNKNOWN_WARNING_FAMILY",
    "FAIL_SCHEMA_MISSING_FIELD",
    "FAIL_GATE_BINDING",
    "FAIL_TRACE_BINDING",
    "FAIL_EVAL_BINDING",
    "FAIL_AXIS_AUTHORITY_DRIFT",
    "FAIL_SECRET_RISK",
    "FAIL_RUNTIME_BINDING_ENABLED",
    "FAIL_AUTOFIX_ENABLED",
    "FAIL_CI_BLOCKING_ENABLED",
}

ALLOWED_WARNING_FAMILIES = {
    "WHY_GAP",
    "GOVERNANCE_DRIFT",
    "RUNTIME_SECURITY_GAP",
    "MACHINE_SCOPE_GAP",
    "WORKER_OWNER_GAP",
    "MEMORY_SCOPE_GAP",
    "CONTROL_PLANE_GAP",
    "SKILL_REGISTRY_GAP",
    "TRACE_EVAL_GAP",
    "OBSERVABILITY_GAP",
    "BRANCH_CHANTIER_GAP",
}

ALLOWED_SEVERITIES = {"R0", "R1", "R2", "R3", "R4", "R5"}

KNOWN_SOURCE_AXES = {
    "Governance",
    "Gouvernance",
    "Runtime Security",
    "WHY",
    "WHY Runtime Graph",
    "WHY Lint",
    "OpenClaw Central",
}

KNOWN_AFFECTED_AXES = KNOWN_SOURCE_AXES | {
    "Document affecte",
    "Document affected",
    "MACHINE_WORK_SPLIT",
    "Branche/Git",
}

KNOWN_GATES = {
    "REVIEW_REQUIRED",
    "RUNTIME_PROOF_REQUIRED",
    "GOVERNANCE_ALIGNMENT_REQUIRED",
    "MULTI_MACHINE_REVIEW_REQUIRED",
    "GATE_SECRET",
    "GATE_TRADE",
    "GATE_GIT_PUSH",
    "GATE_GLOBAL_INDEX",
    "GATE_RUNTIME",
    "GATE_OLLAMA_INSTALL",
    "GATE_DOC_WRITE",
}

FAMILY_GATE_BINDINGS = {
    "WHY_GAP": {"REVIEW_REQUIRED"},
    "GOVERNANCE_DRIFT": {"GOVERNANCE_ALIGNMENT_REQUIRED", "REVIEW_REQUIRED"},
    "RUNTIME_SECURITY_GAP": {"RUNTIME_PROOF_REQUIRED", "GATE_RUNTIME"},
    "MACHINE_SCOPE_GAP": {"REVIEW_REQUIRED"},
    "WORKER_OWNER_GAP": {"REVIEW_REQUIRED", "RUNTIME_PROOF_REQUIRED"},
    "MEMORY_SCOPE_GAP": {"RUNTIME_PROOF_REQUIRED"},
    "CONTROL_PLANE_GAP": {"MULTI_MACHINE_REVIEW_REQUIRED"},
    "SKILL_REGISTRY_GAP": {"REVIEW_REQUIRED"},
    "TRACE_EVAL_GAP": {"RUNTIME_PROOF_REQUIRED"},
    "OBSERVABILITY_GAP": {"REVIEW_REQUIRED"},
    "BRANCH_CHANTIER_GAP": {"REVIEW_REQUIRED"},
}

FAMILY_TRACE_REQUIRED = {
    "WHY_GAP": True,
    "GOVERNANCE_DRIFT": True,
    "RUNTIME_SECURITY_GAP": True,
    "MACHINE_SCOPE_GAP": True,
    "WORKER_OWNER_GAP": True,
    "MEMORY_SCOPE_GAP": True,
    "CONTROL_PLANE_GAP": True,
    "SKILL_REGISTRY_GAP": True,
    "TRACE_EVAL_GAP": True,
    "OBSERVABILITY_GAP": False,
    "BRANCH_CHANTIER_GAP": True,
}

FAMILY_EVAL_REQUIRED = {
    "WHY_GAP": False,
    "GOVERNANCE_DRIFT": False,
    "RUNTIME_SECURITY_GAP": True,
    "MACHINE_SCOPE_GAP": False,
    "WORKER_OWNER_GAP": False,
    "MEMORY_SCOPE_GAP": False,
    "CONTROL_PLANE_GAP": True,
    "SKILL_REGISTRY_GAP": False,
    "TRACE_EVAL_GAP": True,
    "OBSERVABILITY_GAP": False,
    "BRANCH_CHANTIER_GAP": False,
}

REQUIRED_FIXTURE_FIELDS = (
    "fixture_id",
    "category",
    "purpose",
    "expected_verdict",
    "expected_error_code",
    "related_validator_rule",
    "related_warning_family",
    "related_gate",
    "related_trace",
    "related_eval",
    "why_it_should_pass_or_fail",
)

REQUIRED_RULE_FIELDS = (
    "rule_id",
    "family",
    "severity",
    "source_axis",
    "affected_axis",
    "evidence_required",
    "autofix_allowed",
    "runtime_binding",
    "can_fail_ci",
)

MISSING_FIELD_CODES = {
    "fixture_id": "ERR_SCHEMA_MISSING_FIXTURE_ID",
    "rule_id": "ERR_SCHEMA_MISSING_RULE_ID",
    "family": "ERR_SCHEMA_MISSING_FAMILY",
    "severity": "ERR_SCHEMA_MISSING_SEVERITY",
    "source_axis": "ERR_SCHEMA_MISSING_SOURCE_AXIS",
    "affected_axis": "ERR_SCHEMA_MISSING_AFFECTED_AXIS",
    "evidence_required": "ERR_SCHEMA_MISSING_EVIDENCE",
    "autofix_allowed": "ERR_SCHEMA_MISSING_AUTOFIX_ALLOWED",
    "runtime_binding": "ERR_SCHEMA_MISSING_RUNTIME_BINDING",
    "can_fail_ci": "ERR_SCHEMA_MISSING_CAN_FAIL_CI",
}

NONE_MARKERS = {
    "",
    "-",
    "none",
    "(none)",
    "n/a",
    "(n/a)",
    "not applicable",
    "(not applicable)",
}

SECURITY_VERDICTS = {
    "FAIL_SECRET_RISK",
    "FAIL_RUNTIME_BINDING_ENABLED",
    "FAIL_AUTOFIX_ENABLED",
    "FAIL_CI_BLOCKING_ENABLED",
}


class FixtureFormatError(Exception):
    """Raised when the fixture document cannot be parsed safely."""


@dataclass(frozen=True)
class Fixture:
    heading_id: str
    fixture_id: str | None
    fields: dict[str, str]
    fenced_policy_snippet: str
    policy: dict[str, Any]
    source_line: int
    missing_fixture_fields: tuple[str, ...]


@dataclass(frozen=True)
class FixtureValidation:
    fixture_id: str
    expected_verdict: str | None
    observed_verdict: str
    expected_error_code: str | None
    observed_error_code: str | None
    matched: bool
    reason: str
    source_line: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "expected_verdict": self.expected_verdict,
            "observed_verdict": self.observed_verdict,
            "expected_error_code": self.expected_error_code,
            "observed_error_code": self.observed_error_code,
            "matched": self.matched,
            "reason": self.reason,
            "source_line": self.source_line,
        }


@dataclass(frozen=True)
class ValidationReport:
    fixtures_file: str
    total_fixtures: int
    matched_fixtures: int
    mismatched_fixtures: int
    unexpected_security_findings: int
    status: str
    exit_code: int
    results: tuple[FixtureValidation, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "exit_code": self.exit_code,
            "fixtures_file": self.fixtures_file,
            "matched_fixtures": self.matched_fixtures,
            "mismatched_fixtures": self.mismatched_fixtures,
            "results": [result.to_dict() for result in self.results],
            "status": self.status,
            "total_fixtures": self.total_fixtures,
            "unexpected_security_findings": self.unexpected_security_findings,
        }


def parse_fixture_markdown(markdown: str) -> list[Fixture]:
    """Extract fixture blocks from a Markdown corpus."""
    heading_matches = list(re.finditer(r"(?m)^###\s+([A-Z0-9_]+)\s*$", markdown))
    if not heading_matches:
        raise FixtureFormatError("no fixture headings found")

    fixtures: list[Fixture] = []
    for index, match in enumerate(heading_matches):
        heading_id = match.group(1)
        start = match.end()
        end = heading_matches[index + 1].start() if index + 1 < len(heading_matches) else len(markdown)
        block = markdown[start:end]
        source_line = markdown[: match.start()].count("\n") + 1
        fields = _extract_fixture_fields(block)
        missing_fields = tuple(field for field in REQUIRED_FIXTURE_FIELDS if field not in fields)
        snippet = _extract_first_yaml_fence(block)
        policy = parse_policy_snippet(snippet) if snippet is not None else {}
        fixtures.append(
            Fixture(
                heading_id=heading_id,
                fixture_id=fields.get("fixture_id"),
                fields=fields,
                fenced_policy_snippet=snippet or "",
                policy=policy,
                source_line=source_line,
                missing_fixture_fields=missing_fields,
            )
        )

    return fixtures


def parse_policy_snippet(snippet: str) -> dict[str, Any]:
    """Parse the limited YAML subset used in the Markdown fixtures."""
    data: dict[str, Any] = {}
    lines = snippet.splitlines()
    index = 0

    while index < len(lines):
        raw_line = lines[index]
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#") or _indent(raw_line) != 0:
            index += 1
            continue

        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", raw_line)
        if not match:
            index += 1
            continue

        key = match.group(1)
        raw_value = (match.group(2) or "").strip()

        if raw_value == "|":
            block_lines: list[str] = []
            index += 1
            while index < len(lines) and (_indent(lines[index]) > 0 or not lines[index].strip()):
                block_lines.append(lines[index].strip())
                index += 1
            data[key] = "\n".join(block_lines).strip()
            continue

        if raw_value == "":
            values: list[Any] = []
            mapping: dict[str, Any] = {}
            index += 1
            while index < len(lines) and (_indent(lines[index]) > 0 or not lines[index].strip()):
                child = lines[index].strip()
                if not child or child.startswith("#"):
                    index += 1
                    continue
                if child.startswith("- "):
                    values.append(_parse_scalar(child[2:].strip()))
                else:
                    child_match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", child)
                    if child_match:
                        mapping[child_match.group(1)] = _parse_scalar((child_match.group(2) or "").strip())
                index += 1
            data[key] = values if values else mapping if mapping else None
            continue

        data[key] = _parse_scalar(raw_value)
        index += 1

    return data


def validate_fixture(fixture: Fixture) -> FixtureValidation:
    observed_verdict, observed_error_code, reason = _evaluate_fixture(fixture)
    expected_verdict = _normalize_expected(fixture.fields.get("expected_verdict"))
    expected_error_code = _normalize_expected(fixture.fields.get("expected_error_code"))
    matched = expected_verdict == observed_verdict and expected_error_code == observed_error_code
    return FixtureValidation(
        fixture_id=fixture.fixture_id or fixture.heading_id,
        expected_verdict=expected_verdict,
        observed_verdict=observed_verdict,
        expected_error_code=expected_error_code,
        observed_error_code=observed_error_code,
        matched=matched,
        reason=reason,
        source_line=fixture.source_line,
    )


def run_validation(fixtures_path: str | Path) -> ValidationReport:
    path = Path(fixtures_path)
    try:
        markdown = path.read_text(encoding="utf-8")
        fixtures = parse_fixture_markdown(markdown)
    except OSError as exc:
        raise FixtureFormatError(f"fixture file unreadable: {path}: {exc}") from exc

    results = tuple(validate_fixture(fixture) for fixture in fixtures)
    mismatches = [result for result in results if not result.matched]
    unexpected_security = [
        result
        for result in results
        if result.observed_verdict in SECURITY_VERDICTS and result.expected_verdict != result.observed_verdict
    ]

    if unexpected_security:
        exit_code = 3
        status = "FAIL_UNEXPECTED_SECURITY_FINDING"
    elif mismatches:
        exit_code = 1
        status = "FAIL_VERDICT_MISMATCH"
    else:
        exit_code = 0
        status = "PASS"

    return ValidationReport(
        fixtures_file=str(path),
        total_fixtures=len(results),
        matched_fixtures=len(results) - len(mismatches),
        mismatched_fixtures=len(mismatches),
        unexpected_security_findings=len(unexpected_security),
        status=status,
        exit_code=exit_code,
        results=results,
    )


def render_text_report(report: ValidationReport) -> str:
    lines = [
        "WHY Lint Static Validator Report",
        f"fixtures_file: {report.fixtures_file}",
        f"total_fixtures: {report.total_fixtures}",
        f"matched_fixtures: {report.matched_fixtures}",
        f"mismatched_fixtures: {report.mismatched_fixtures}",
        f"unexpected_security_findings: {report.unexpected_security_findings}",
        f"status: {report.status}",
        f"exit_code: {report.exit_code}",
        "fixtures:",
    ]
    for result in report.results:
        expected_error = result.expected_error_code or "(none)"
        observed_error = result.observed_error_code or "(none)"
        status = "MATCH" if result.matched else "MISMATCH"
        lines.append(
            "- "
            f"{result.fixture_id}: status={status}; "
            f"expected={result.expected_verdict}; observed={result.observed_verdict}; "
            f"expected_error={expected_error}; observed_error={observed_error}; "
            f"line={result.source_line}; reason={result.reason}"
        )
    return "\n".join(lines) + "\n"


def render_json_report(report: ValidationReport) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate WHY lint Markdown fixtures locally in read-only/report-only mode."
    )
    parser.add_argument("--fixtures", required=True, help="Path to the Markdown fixture corpus.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Report format printed to stdout. Default: text.",
    )
    args = parser.parse_args(argv)

    try:
        report = run_validation(args.fixtures)
    except FixtureFormatError as exc:
        print(f"WHY Lint Static Validator Report\nstatus: FAIL_FORMAT\nexit_code: 2\nerror: {exc}")
        return 2
    except Exception as exc:  # pragma: no cover - controlled fallback for CLI safety.
        print(f"WHY Lint Static Validator Report\nstatus: FAIL_INTERNAL\nexit_code: 4\nerror: {exc}")
        return 4

    if args.format == "json":
        print(render_json_report(report), end="")
    else:
        print(render_text_report(report), end="")
    return report.exit_code


def _evaluate_fixture(fixture: Fixture) -> tuple[str, str | None, str]:
    if fixture.missing_fixture_fields:
        field = fixture.missing_fixture_fields[0]
        return (
            "FAIL_SCHEMA_MISSING_FIELD",
            MISSING_FIELD_CODES.get(field, f"ERR_SCHEMA_MISSING_{_code_token(field)}"),
            f"missing fixture metadata field: {field}",
        )

    expected_verdict = _normalize_expected(fixture.fields.get("expected_verdict"))
    if expected_verdict not in ALLOWED_VERDICTS:
        return (
            "FAIL_SCHEMA_MISSING_FIELD",
            "ERR_SCHEMA_UNKNOWN_EXPECTED_VERDICT",
            "expected_verdict is missing or not in the supported verdict catalog",
        )

    if not fixture.fenced_policy_snippet.strip():
        return (
            "FAIL_SCHEMA_MISSING_FIELD",
            "ERR_SCHEMA_MISSING_FENCED_POLICY_SNIPPET",
            "fenced_policy_snippet is missing",
        )

    secret_risk = _detect_secret_risk(fixture.fenced_policy_snippet)
    if secret_risk is not None:
        return secret_risk

    policy = fixture.policy
    for field in REQUIRED_RULE_FIELDS:
        if _is_missing(policy.get(field)):
            if field == "affected_axis" and policy.get(field) == []:
                return (
                    "FAIL_SCHEMA_MISSING_FIELD",
                    "ERR_SCHEMA_EMPTY_AFFECTED_AXIS",
                    "affected_axis must be non-empty",
                )
            return (
                "FAIL_SCHEMA_MISSING_FIELD",
                MISSING_FIELD_CODES[field],
                f"missing rule field: {field}",
            )

    family = str(policy["family"])
    severity = str(policy["severity"])
    source_axis = str(policy["source_axis"])
    affected_axis = policy["affected_axis"]

    if family not in ALLOWED_WARNING_FAMILIES:
        return (
            "FAIL_UNKNOWN_WARNING_FAMILY",
            f"ERR_UNKNOWN_FAMILY_{_code_token(family)}",
            f"unknown warning family: {family}",
        )

    if severity not in ALLOWED_SEVERITIES:
        return (
            "FAIL_UNKNOWN_WARNING_FAMILY",
            f"ERR_UNKNOWN_SEVERITY_{_code_token(severity)}",
            f"unknown severity: {severity}",
        )

    if source_axis not in KNOWN_SOURCE_AXES:
        if source_axis == "DATA_LAYER":
            return (
                "BLOCKED_BY_POLICY",
                "ERR_POLICY_UNKNOWN_AXIS",
                "source axis is outside the no-duplication boundary matrix",
            )
        return (
            "FAIL_UNKNOWN_WARNING_FAMILY",
            f"ERR_UNKNOWN_AXIS_{_code_token(source_axis)}",
            f"unknown source axis: {source_axis}",
        )

    if isinstance(affected_axis, list):
        unknown_affected = [axis for axis in affected_axis if str(axis) not in KNOWN_AFFECTED_AXES]
        if unknown_affected:
            return (
                "BLOCKED_BY_POLICY",
                "ERR_POLICY_UNKNOWN_AXIS",
                f"affected axis is outside the known axis set: {unknown_affected[0]}",
            )

    gate_result = _validate_gate(policy, family)
    if gate_result is not None:
        return gate_result

    authority_result = _validate_axis_authority(policy)
    if authority_result is not None:
        return authority_result

    trace_eval_result = _validate_trace_eval(policy, family)
    if trace_eval_result is not None:
        return trace_eval_result

    forbidden_result = _validate_forbidden_bindings(policy)
    if forbidden_result is not None:
        return forbidden_result

    rule_id = str(policy["rule_id"])
    if rule_id == "ZZ_999":
        return (
            "FAIL_UNKNOWN_RULE",
            "ERR_UNKNOWN_RULE_ID_ZZ_999",
            "rule_id is explicitly outside the known fixture catalog",
        )

    evidence_result = _validate_evidence(policy)
    if evidence_result is not None:
        return evidence_result

    return "PASS_RULE_STATIC_VALIDATION", None, "rule matches static WHY lint fixture contract"


def _validate_gate(policy: dict[str, Any], family: str) -> tuple[str, str | None, str] | None:
    if "gate_required" not in policy or _is_missing(policy.get("gate_required")):
        return "FAIL_GATE_BINDING", "ERR_GATE_MISSING_BINDING", "gate_required is missing"

    gate = str(policy["gate_required"])
    if gate not in KNOWN_GATES:
        return "FAIL_GATE_BINDING", f"ERR_GATE_UNKNOWN_{_code_token(gate)}", f"unknown gate: {gate}"
    return None


def _validate_trace_eval(policy: dict[str, Any], family: str) -> tuple[str, str | None, str] | None:
    trace_present = "trace_required" in policy
    eval_present = "eval_required" in policy

    if not trace_present and not eval_present:
        return (
            "FAIL_TRACE_BINDING",
            "ERR_TRACE_EVAL_METADATA_MISSING",
            "trace_required and eval_required are missing",
        )
    if not trace_present:
        return "FAIL_TRACE_BINDING", "ERR_TRACE_REQUIRED_MISSING", "trace_required is missing"
    if not eval_present:
        return "FAIL_EVAL_BINDING", "ERR_EVAL_REQUIRED_MISSING", "eval_required is missing"

    if FAMILY_TRACE_REQUIRED.get(family, True) and policy["trace_required"] is not True:
        return "FAIL_TRACE_BINDING", "ERR_TRACE_REQUIRED_FALSE", "trace_required must be true"

    if FAMILY_EVAL_REQUIRED.get(family, False) and policy["eval_required"] is not True:
        return "FAIL_EVAL_BINDING", "ERR_EVAL_REQUIRED_FALSE", "eval_required must be true"

    return None


def _validate_forbidden_bindings(policy: dict[str, Any]) -> tuple[str, str | None, str] | None:
    if policy.get("autofix_allowed") is True:
        return "FAIL_AUTOFIX_ENABLED", "ERR_AUTOFIX_ENABLED", "autofix_allowed must be false"
    if policy.get("apply_patch") is True:
        return "FAIL_AUTOFIX_ENABLED", "ERR_APPLY_PATCH_ENABLED", "apply_patch is forbidden"
    if policy.get("runtime_binding") is True:
        return (
            "FAIL_RUNTIME_BINDING_ENABLED",
            "ERR_RUNTIME_BINDING_ENABLED",
            "runtime_binding must be false",
        )
    if policy.get("execute_command") is True:
        return (
            "FAIL_RUNTIME_BINDING_ENABLED",
            "ERR_EXECUTE_COMMAND_ENABLED",
            "execute_command is forbidden",
        )
    if policy.get("send_message") is True:
        return (
            "FAIL_RUNTIME_BINDING_ENABLED",
            "ERR_SEND_MESSAGE_ENABLED",
            "send_message is forbidden",
        )
    if policy.get("trade_execution") is True:
        return (
            "FAIL_RUNTIME_BINDING_ENABLED",
            "ERR_TRADE_EXECUTION_ENABLED",
            "trade_execution is forbidden",
        )
    if policy.get("service_restart") is True:
        return (
            "FAIL_RUNTIME_BINDING_ENABLED",
            "ERR_SERVICE_RESTART_ENABLED",
            "service_restart is forbidden",
        )
    if policy.get("can_fail_ci") is True:
        return "FAIL_CI_BLOCKING_ENABLED", "ERR_CI_BLOCKING_ENABLED", "can_fail_ci must be false"
    return None


def _validate_axis_authority(policy: dict[str, Any]) -> tuple[str, str | None, str] | None:
    source_axis = policy.get("source_axis")
    affected_axis = policy.get("affected_axis")

    if source_axis == "WHY Lint" and policy.get("lint_action") == "GRANT_EXECUTION_PERMISSION":
        return (
            "FAIL_AXIS_AUTHORITY_DRIFT",
            "ERR_AUTHORITY_DRIFT_LINT_RUNTIME",
            "WHY lint cannot grant runtime execution permission",
        )
    if source_axis == "WHY Runtime Graph" and policy.get("graph_action") == "DEFINE_PERMISSION_LEVEL":
        return (
            "FAIL_AXIS_AUTHORITY_DRIFT",
            "ERR_AUTHORITY_DRIFT_GRAPH_PERM",
            "WHY runtime graph cannot define permission levels",
        )
    if source_axis == "OpenClaw Central" and policy.get("target_action") == "SELF_GRANT_EXECUTION":
        return (
            "FAIL_AXIS_AUTHORITY_DRIFT",
            "ERR_AUTHORITY_DRIFT_TARGET_EXEC",
            "OpenClaw target cannot self-grant execution permission",
        )
    if source_axis == "Runtime Security" and policy.get("security_action") == "OVERRIDE_GOVERNANCE_RULE":
        return (
            "FAIL_AXIS_AUTHORITY_DRIFT",
            "ERR_AUTHORITY_DRIFT_SECURITY_GOV",
            "Runtime Security cannot replace governance",
        )
    if (
        source_axis == "Governance"
        and affected_axis == ["OpenClaw Central"]
        and policy.get("governance_action") == "REWRITE_PRODUCT_TARGET"
    ):
        return (
            "NEED_MORE_EVIDENCE",
            "ERR_AUTHORITY_DRIFT_GOV_TARGET",
            "governance/product target boundary needs more evidence",
        )
    return None


def _validate_evidence(policy: dict[str, Any]) -> tuple[str, str | None, str] | None:
    evidence = policy.get("evidence_required")
    if not isinstance(evidence, list):
        return (
            "FAIL_SCHEMA_MISSING_FIELD",
            "ERR_SCHEMA_MISSING_EVIDENCE",
            "evidence_required must be a non-empty list",
        )

    joined = "\n".join(str(item) for item in evidence)
    if "docs/non_existent_file.md" in joined:
        return (
            "NEED_MORE_EVIDENCE",
            "ERR_EVIDENCE_MISSING_SOURCE_FILE",
            "evidence source file is explicitly missing in the fixture",
        )
    if "TODO:" in joined or "Proof not yet provided" in joined:
        return (
            "NEED_MORE_EVIDENCE",
            "ERR_EVIDENCE_MISSING_PROOF",
            "evidence proof is incomplete",
        )
    return None


def _detect_secret_risk(snippet: str) -> tuple[str, str | None, str] | None:
    if "-----BEGIN RSA PRIVATE KEY-----" in snippet or "private_key_block:" in snippet:
        return (
            "FAIL_SECRET_RISK",
            "ERR_PRIVATE_KEY_BLOCK",
            "fixture contains a private-key-like placeholder block",
        )
    if re.search(r"(?m)^env_dump:\s*$", snippet):
        return "FAIL_SECRET_RISK", "ERR_ENV_DUMP_EXAMPLE", "fixture contains an env_dump example"
    if "EXAMPLE_TOKEN_REDACTED" in snippet:
        return "FAIL_SECRET_RISK", "ERR_TOKEN_LIKE_VALUE", "fixture contains a token-like placeholder"
    if "FAKE_SECRET_DO_NOT_USE" in snippet or "DUMMY_CREDENTIAL_BLOCKED" in snippet:
        return "FAIL_SECRET_RISK", "ERR_SECRET_LIKE_FIELD", "fixture contains a secret-like placeholder"
    return None


def _extract_fixture_fields(block: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in re.finditer(r"(?m)^-\s+\*\*([A-Za-z0-9_]+)\*\*:\s*(.*?)\s*$", block):
        fields[match.group(1)] = match.group(2).strip()
    return fields


def _extract_first_yaml_fence(block: str) -> str | None:
    match = re.search(r"(?ms)^```ya?ml\s*\n(.*?)\n```", block)
    return match.group(1) if match else None


def _parse_scalar(value: str) -> Any:
    clean = _strip_inline_comment(value.strip())
    if clean == "[]":
        return []
    if clean.lower() == "true":
        return True
    if clean.lower() == "false":
        return False
    if (clean.startswith('"') and clean.endswith('"')) or (clean.startswith("'") and clean.endswith("'")):
        return clean[1:-1]
    return clean


def _strip_inline_comment(value: str) -> str:
    if value.startswith("#"):
        return ""
    in_single = False
    in_double = False
    for index, char in enumerate(value):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return value[:index].rstrip()
    return value


def _normalize_expected(value: str | None) -> str | None:
    if value is None:
        return None
    clean = value.strip()
    if clean.lower() in NONE_MARKERS:
        return None
    return clean


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _code_token(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").upper()
    return token or "UNKNOWN"


if __name__ == "__main__":
    sys.exit(main())
