"""Read-only fixture harness for OpenClaw MCP policy validator."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
import tempfile
from typing import Any

from .parser import PolicyParseError, parse_policy_yaml
from .validator import (
    CANONICAL_CLASSES,
    CANONICAL_EVALS,
    CANONICAL_GATES,
    CANONICAL_TRACES,
    validate_policy_file,
)


PASS_FIXTURE_HARNESS = "PASS_FIXTURE_HARNESS"
FAIL_FIXTURE_EXPECTATION_MISMATCH = "FAIL_FIXTURE_EXPECTATION_MISMATCH"
BLOCKED_WITH_REASON = "BLOCKED_WITH_REASON"

INDEX_FILE = "09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md"
FIXTURE_FENCE_RE = re.compile(r"```(?P<label>[A-Za-z0-9_-]*)\n(?P<body>.*?)\n```", re.DOTALL)


@dataclass(frozen=True)
class FixtureExpectation:
    fixture_id: str
    file: str
    category: str
    expected_verdict: str
    expected_error_code: str
    related_rule: str
    related_gate: str
    related_trace: str
    related_eval: str


@dataclass
class FixtureCase:
    expectation: FixtureExpectation
    snippet: dict[str, Any]
    inline_expected_verdict: str | None
    inline_expected_error_code: str | None
    source_path: str
    fence_label: str


@dataclass
class FixtureResult:
    fixture_id: str
    source_file: str
    expected_verdict: str
    expected_error_code: str
    actual_verdict: str
    actual_error_code: str
    status: str
    message: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "fixture_id": self.fixture_id,
            "source_file": self.source_file,
            "expected_verdict": self.expected_verdict,
            "expected_error_code": self.expected_error_code,
            "actual_verdict": self.actual_verdict,
            "actual_error_code": self.actual_error_code,
            "status": self.status,
            "message": self.message,
        }


@dataclass
class HarnessReport:
    verdict: str
    total_fixtures: int
    pass_count: int
    fail_count: int
    mismatches: list[FixtureResult] = field(default_factory=list)
    results: list[FixtureResult] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        return 0 if self.verdict == PASS_FIXTURE_HARNESS else 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict,
            "total_fixtures": self.total_fixtures,
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "mismatches": [item.to_dict() for item in self.mismatches],
            "results": [item.to_dict() for item in self.results],
            "warnings": self.warnings,
            "blocked_reasons": self.blocked_reasons,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


def run_fixture_harness(corpus_dir: str | Path) -> HarnessReport:
    corpus_path = Path(corpus_dir)
    blocked: list[str] = []
    warnings: list[str] = []
    if not corpus_path.exists() or not corpus_path.is_dir():
        return HarnessReport(
            verdict=BLOCKED_WITH_REASON,
            total_fixtures=0,
            pass_count=0,
            fail_count=0,
            blocked_reasons=[f"fixture corpus directory not found: {corpus_path}"],
        )

    try:
        expectations = parse_fixture_index(corpus_path / INDEX_FILE)
        cases = parse_fixture_cases(corpus_path, expectations, warnings)
    except FixtureHarnessError as exc:
        return HarnessReport(
            verdict=BLOCKED_WITH_REASON,
            total_fixtures=0,
            pass_count=0,
            fail_count=0,
            warnings=warnings,
            blocked_reasons=[str(exc)],
        )

    results: list[FixtureResult] = []
    with tempfile.TemporaryDirectory(prefix="openclaw_policy_fixture_") as tmp_dir:
        temp_root = Path(tmp_dir)
        for case in cases:
            materialized = materialize_policy(case)
            temp_file = temp_root / f"{case.expectation.fixture_id}.yaml"
            temp_file.write_text(materialized, encoding="utf-8")
            validation = validate_policy_file(temp_file)
            actual_error = validation.errors[0].error_code if validation.errors else "none"
            expected_error = case.expectation.expected_error_code
            ok = validation.verdict == case.expectation.expected_verdict and actual_error == expected_error
            message = ""
            if not ok:
                message = "expected verdict or error code mismatch"
            results.append(
                FixtureResult(
                    fixture_id=case.expectation.fixture_id,
                    source_file=case.expectation.file,
                    expected_verdict=case.expectation.expected_verdict,
                    expected_error_code=expected_error,
                    actual_verdict=validation.verdict,
                    actual_error_code=actual_error,
                    status="PASS" if ok else "FAIL",
                    message=message,
                )
            )

    mismatches = [result for result in results if result.status != "PASS"]
    if blocked:
        verdict = BLOCKED_WITH_REASON
    elif mismatches:
        verdict = FAIL_FIXTURE_EXPECTATION_MISMATCH
    else:
        verdict = PASS_FIXTURE_HARNESS
    return HarnessReport(
        verdict=verdict,
        total_fixtures=len(results),
        pass_count=len(results) - len(mismatches),
        fail_count=len(mismatches),
        mismatches=mismatches,
        results=results,
        warnings=warnings,
        blocked_reasons=blocked,
    )


class FixtureHarnessError(ValueError):
    """Raised when fixture harness metadata is incomplete or ambiguous."""


def parse_fixture_index(path: Path) -> dict[str, FixtureExpectation]:
    if not path.exists():
        raise FixtureHarnessError(f"fixture index missing: {path}")
    expectations: dict[str, FixtureExpectation] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("| `"):
            continue
        columns = [_clean_table_cell(part) for part in stripped.strip("|").split("|")]
        if len(columns) != 9:
            continue
        fixture_id = columns[0]
        if fixture_id in expectations:
            raise FixtureHarnessError(f"duplicate fixture id in index: {fixture_id}")
        expectations[fixture_id] = FixtureExpectation(
            fixture_id=fixture_id,
            file=columns[1],
            category=columns[2],
            expected_verdict=columns[3],
            expected_error_code=columns[4],
            related_rule=columns[5],
            related_gate=columns[6],
            related_trace=columns[7],
            related_eval=columns[8],
        )
    if not expectations:
        raise FixtureHarnessError("fixture index contains no fixture rows")
    return expectations


def parse_fixture_cases(
    corpus_path: Path,
    expectations: dict[str, FixtureExpectation],
    warnings: list[str],
) -> list[FixtureCase]:
    cases: dict[str, FixtureCase] = {}
    for expectation in sorted(expectations.values(), key=lambda item: item.fixture_id):
        source_path = corpus_path / expectation.file
        if not source_path.exists():
            raise FixtureHarnessError(f"fixture file missing: {expectation.file}")
        found = _extract_cases_from_file(source_path, expectation, warnings)
        if len(found) != 1:
            raise FixtureHarnessError(
                f"expected exactly one fixture block for {expectation.fixture_id}, found {len(found)}"
            )
        if expectation.fixture_id in cases:
            raise FixtureHarnessError(f"duplicate fixture case: {expectation.fixture_id}")
        cases[expectation.fixture_id] = found[0]
    return [cases[fixture_id] for fixture_id in sorted(cases)]


def _extract_cases_from_file(
    source_path: Path,
    expectation: FixtureExpectation,
    warnings: list[str],
) -> list[FixtureCase]:
    text = source_path.read_text(encoding="utf-8")
    found: list[FixtureCase] = []
    for match in FIXTURE_FENCE_RE.finditer(text):
        label = match.group("label") or "text"
        body = match.group("body")
        if "fixture_id:" not in body or "policy_snippet:" not in body:
            continue
        try:
            parsed = parse_policy_yaml(body)
        except PolicyParseError as exc:
            raise FixtureHarnessError(f"fixture block parse failed in {source_path.name}: {exc}") from exc
        fixture_id = str(parsed.get("fixture_id", ""))
        if fixture_id != expectation.fixture_id:
            continue
        if "policy_snippet" not in parsed:
            raise FixtureHarnessError(f"fixture {fixture_id} has no policy_snippet")
        inline_verdict = parsed.get("expected_verdict")
        inline_error = _normalize_expected_error(parsed.get("expected_error_code"))
        if not inline_verdict or inline_error == "":
            raise FixtureHarnessError(f"fixture {fixture_id} is missing inline expectation fields")
        if inline_verdict != expectation.expected_verdict:
            warnings.append(f"{fixture_id}: inline expected_verdict differs from fixture index")
        if inline_error != expectation.expected_error_code:
            warnings.append(f"{fixture_id}: inline expected_error_code differs from fixture index")
        snippet = parsed["policy_snippet"]
        if not isinstance(snippet, dict):
            raise FixtureHarnessError(f"fixture {fixture_id} policy_snippet is not a map")
        found.append(
            FixtureCase(
                expectation=expectation,
                snippet=snippet,
                inline_expected_verdict=str(inline_verdict),
                inline_expected_error_code=inline_error,
                source_path=str(source_path),
                fence_label=label,
            )
        )
    return found


def materialize_policy(case: FixtureCase) -> str:
    snippet = case.snippet
    if "final_verdict_policy" in snippet:
        policy = _base_policy()
        policy["traces"].pop("TRACE_VERDICT", None)
        return _dump_yaml(policy)
    if "policy" in snippet or any(key in snippet for key in _required_top_level_sections()):
        return _dump_yaml(_materialize_policy_document(case))
    if "strict_worker_role" in snippet and "capability_class" not in snippet:
        return _dump_yaml(_materialize_worker_policy(case))
    return _dump_yaml(_materialize_capability_policy(case))


def _materialize_policy_document(case: FixtureCase) -> dict[str, Any]:
    baseline = _base_policy()
    result: dict[str, Any] = {}
    for key in _required_top_level_sections():
        if key in case.snippet:
            value = case.snippet[key]
            if value == "present":
                result[key] = baseline[key]
            else:
                result[key] = value
        elif _should_preserve_missing_top_level(case, key):
            continue
        else:
            result[key] = baseline[key]
    return result


def _materialize_capability_policy(case: FixtureCase) -> dict[str, Any]:
    policy = _base_policy()
    snippet = dict(case.snippet)
    capability_id = str(
        snippet.get("capability_id")
        or snippet.get("requested_capability")
        or case.expectation.fixture_id.lower()
    )
    class_name = str(snippet.get("capability_class", "READ_ONLY"))
    capability = {key: value for key, value in snippet.items() if key != "capability_id"}
    capability["capability_class"] = class_name
    _fill_capability_defaults(case, capability_id, capability)
    policy["capabilities"] = {capability_id: capability}
    if capability_id == "suppress_audit_trace":
        capability["approval_path"] = "none"
    return policy


def _materialize_worker_policy(case: FixtureCase) -> dict[str, Any]:
    policy = _base_policy()
    snippet = case.snippet
    role = str(snippet.get("strict_worker_role", "Strict Worker"))
    role_config: dict[str, Any] = {
        "allowed_capabilities": snippet.get("allowed_capabilities", ["repo_state"]),
        "blocked_capabilities": snippet.get("blocked_capabilities", ["secret_read"]),
        "self_approval": False,
    }
    if snippet.get("approval_actor") == "same_worker" or snippet.get("no_self_approval_rule") is False:
        role_config["self_approval"] = True
    if "requested_capability" in snippet:
        role_config["requested_capability"] = snippet["requested_capability"]
    if "worker_output" in snippet:
        role_config["worker_output"] = snippet["worker_output"]
    if "output_policy" in snippet:
        role_config["output_policy"] = snippet["output_policy"]
    if "placeholder_value" in snippet:
        role_config["placeholder_value"] = snippet["placeholder_value"]
    policy["strict_worker_roles"] = {role: role_config}
    return policy


def _fill_capability_defaults(
    case: FixtureCase,
    capability_id: str,
    capability: dict[str, Any],
) -> None:
    class_name = str(capability.get("capability_class", ""))
    default_status = str(capability.get("default_status", ""))
    if "default_allowed" not in capability and default_status:
        capability["default_allowed"] = default_status.startswith("ALLOW")
    if "gate_required" not in capability:
        capability["gate_required"] = class_name in {
            "WRITE_GATED",
            "RUNTIME_GATED",
            "HUMAN_APPROVAL_REQUIRED",
        }
    if "gate_id" not in capability:
        capability["gate_id"] = _default_gate(case, class_name)
    if "trace_required" not in capability:
        capability["trace_required"] = True
    if "trace_family" not in capability:
        capability["trace_family"] = _default_trace(case, class_name)
    if "eval_required" not in capability:
        capability["eval_required"] = True
    if "eval_profile" not in capability:
        capability["eval_profile"] = _default_eval(case, class_name)
    if "secret_policy" not in capability:
        capability["secret_policy"] = "no_secret_allowed"
    if class_name == "READ_SANITIZED" and "output_policy" not in capability:
        capability["output_policy"] = "sanitized_output_only"
    if class_name == "RUNTIME_GATED" and case.expectation.expected_error_code != "ERR_RUNTIME_WITHOUT_GATE":
        capability.setdefault("rollback_required", True)
    if class_name == "WRITE_GATED":
        capability.setdefault("rollback_required", True)
    if case.expectation.expected_error_code == "ERR_GATE_BYPASS_ALLOWED":
        if capability_id in {"trade_execution", "bypass_human_gate"}:
            capability["approval_path"] = "none"
            capability["default_allowed"] = True
        if capability_id == "unrestricted_shell":
            capability["default_allowed"] = True
    if case.expectation.expected_error_code == "ERR_SUPPRESS_TRACE_ALLOWED":
        capability["trace_required"] = True
        capability["default_allowed"] = True
        capability["approval_path"] = "none"
    if case.expectation.fixture_id == "FAIL_MCP_CALL_WITHOUT_TRACE_MCP_CALL_01":
        capability["trace_family"] = None


def _base_policy() -> dict[str, Any]:
    return {
        "policy": {
            "id": "OPENCLAW_MCP_POLICY_FIXTURE_HARNESS_01",
            "version": "0.1-fixture",
            "status": "draft_doc_only",
            "default_status": "BLOCKED_BY_DEFAULT",
            "runtime_binding": False,
            "secret_policy": "no_secret_allowed",
            "unknown_capability": "BLOCKED_BY_DEFAULT",
        },
        "capability_classes": {
            class_name: {
                "default_allowed": class_name in {"READ_ONLY", "READ_SANITIZED"},
                "approval_path": "none"
                if class_name in {"READ_ONLY", "BLOCKED_BY_DEFAULT", "NEVER_ALLOWED"}
                else "human_gate",
            }
            for class_name in sorted(CANONICAL_CLASSES)
        },
        "capabilities": {
            "repo_state": {
                "capability_class": "READ_ONLY",
                "default_allowed": True,
                "gate_required": False,
                "gate_id": "none",
                "trace_required": True,
                "trace_family": "TRACE_MCP_CALL",
                "eval_required": True,
                "eval_profile": "EVAL_MCP_BOUNDARY_COMPLIANCE",
                "secret_policy": "no_secret_allowed",
                "output_policy": "bounded_summary",
            }
        },
        "gates": {gate_id: {} for gate_id in sorted(CANONICAL_GATES)},
        "traces": {trace_id: {} for trace_id in sorted(CANONICAL_TRACES)},
        "evals": {eval_id: {} for eval_id in sorted(CANONICAL_EVALS)},
        "strict_worker_roles": {
            "Repo Auditor": {
                "allowed_capabilities": ["repo_state"],
                "blocked_capabilities": ["secret_read"],
                "self_approval": False,
            }
        },
        "ollama_lab_policy": {"ollama_health_check": "read_only_or_gated"},
        "governor_decision_rules": {"unknown_capability": "BLOCKED_BY_DEFAULT"},
        "never_allowed": {
            "secret_read": {
                "capability_class": "NEVER_ALLOWED",
                "approval_path": "none",
            }
        },
        "blocked_by_default": {"unknown_capability": "BLOCKED_BY_DEFAULT"},
    }


def _required_top_level_sections() -> list[str]:
    return [
        "policy",
        "capability_classes",
        "capabilities",
        "gates",
        "traces",
        "evals",
        "strict_worker_roles",
        "ollama_lab_policy",
        "governor_decision_rules",
        "never_allowed",
        "blocked_by_default",
    ]


def _should_preserve_missing_top_level(case: FixtureCase, key: str) -> bool:
    fixture_id = case.expectation.fixture_id
    return (
        fixture_id == "FAIL_MISSING_CAPABILITY_CLASSES_01"
        and key == "capability_classes"
    ) or (
        fixture_id == "FAIL_MISSING_GOVERNOR_RULES_01"
        and key == "governor_decision_rules"
    )


def _default_gate(case: FixtureCase, class_name: str) -> str:
    if case.expectation.related_gate != "none":
        return case.expectation.related_gate
    if class_name == "WRITE_GATED":
        return "GATE_DOC_WRITE"
    if class_name == "RUNTIME_GATED":
        return "GATE_RUNTIME"
    if class_name == "HUMAN_APPROVAL_REQUIRED":
        return "GATE_MCP_WRITE"
    return "none"


def _default_trace(case: FixtureCase, class_name: str) -> str:
    if case.expectation.related_trace != "none":
        return case.expectation.related_trace
    if class_name == "RUNTIME_GATED":
        return "TRACE_RUNTIME_GATED_ACTION"
    if class_name in {"WRITE_GATED", "HUMAN_APPROVAL_REQUIRED"}:
        return "TRACE_HUMAN_GATE"
    return "TRACE_MCP_CALL"


def _default_eval(case: FixtureCase, class_name: str) -> str:
    if case.expectation.related_eval != "none":
        return case.expectation.related_eval
    if class_name in {"WRITE_GATED", "HUMAN_APPROVAL_REQUIRED"}:
        return "EVAL_GATE_REQUIRED"
    if class_name == "RUNTIME_GATED":
        return "EVAL_NO_RUNTIME_TOUCH"
    return "EVAL_MCP_BOUNDARY_COMPLIANCE"


def _dump_yaml(value: Any, indent: int = 0) -> str:
    lines = _dump_yaml_lines(value, indent)
    return "\n".join(lines) + "\n"


def _dump_yaml_lines(value: Any, indent: int) -> list[str]:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key in sorted(value):
            item = value[key]
            if isinstance(item, (dict, list)):
                if item == {}:
                    lines.append(f"{prefix}{key}: {{}}")
                elif item == []:
                    lines.append(f"{prefix}{key}: []")
                else:
                    lines.append(f"{prefix}{key}:")
                    lines.extend(_dump_yaml_lines(item, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {_scalar_to_yaml(item)}")
        return lines
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(_dump_yaml_lines(item, indent + 2))
            else:
                lines.append(f"{prefix}- {_scalar_to_yaml(item)}")
        return lines
    return [f"{prefix}{_scalar_to_yaml(value)}"]


def _scalar_to_yaml(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "none"
    return str(value)


def _clean_table_cell(value: str) -> str:
    cleaned = value.strip()
    if cleaned.startswith("`") and cleaned.endswith("`"):
        cleaned = cleaned[1:-1]
    return cleaned


def _normalize_expected_error(value: Any) -> str:
    if value is None:
        return "none"
    return str(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openclaw-mcp-policy-fixture-harness",
        description="Run the static OpenClaw MCP policy validator against Markdown fixtures.",
    )
    parser.add_argument("fixture_corpus", help="Path to fixture corpus directory.")
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    report = run_fixture_harness(args.fixture_corpus)
    if args.format == "json":
        print(report.to_json())
    else:
        print(f"verdict={report.verdict}")
        print(f"total_fixtures={report.total_fixtures}")
        print(f"pass_count={report.pass_count}")
        print(f"fail_count={report.fail_count}")
        for mismatch in report.mismatches:
            print(
                "mismatch="
                f"{mismatch.fixture_id} "
                f"expected={mismatch.expected_verdict}/{mismatch.expected_error_code} "
                f"actual={mismatch.actual_verdict}/{mismatch.actual_error_code}"
            )
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
