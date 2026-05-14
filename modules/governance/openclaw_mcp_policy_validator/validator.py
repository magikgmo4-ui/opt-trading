"""Static read-only OpenClaw MCP policy validator."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import re
from typing import Any

from .parser import PolicyParseError, parse_policy_yaml


PASS_VERDICT = "PASS_POLICY_STATIC_VALIDATION"

ERROR_VERDICTS = {
    "ERR_SCHEMA_MISSING_FIELD": "FAIL_SCHEMA_MISSING_FIELD",
    "ERR_POLICY_VERSION_CONFLICT": "FAIL_POLICY",
    "ERR_RUNTIME_BINDING_ENABLED": "FAIL_RUNTIME_BINDING_ENABLED",
    "ERR_SECRET_POLICY_MISSING": "FAIL_SCHEMA_MISSING_FIELD",
    "ERR_SECRET_RISK": "FAIL_SECRET_RISK",
    "ERR_UNKNOWN_CLASS": "FAIL_UNKNOWN_CLASS",
    "ERR_UNKNOWN_CAPABILITY": "BLOCKED_WITH_REASON",
    "ERR_DEFAULT_ALLOW_BLOCKED_CLASS": "FAIL_POLICY",
    "ERR_READ_SANITIZED_OUTPUT": "FAIL_POLICY",
    "ERR_WRITE_WITHOUT_GATE": "FAIL_GATE_BINDING",
    "ERR_RUNTIME_WITHOUT_GATE": "FAIL_GATE_BINDING",
    "ERR_MISSING_ROLLBACK": "FAIL_POLICY",
    "ERR_TRACE_REQUIRED_MISSING": "FAIL_TRACE_BINDING",
    "ERR_TRACE_FAMILY_UNKNOWN": "FAIL_TRACE_BINDING",
    "ERR_EVAL_REQUIRED_MISSING": "FAIL_EVAL_BINDING",
    "ERR_EVAL_PROFILE_UNKNOWN": "FAIL_EVAL_BINDING",
    "ERR_NEVER_ALLOWED_APPROVAL_PATH": "FAIL_NEVER_ALLOWED_APPROVAL_PATH",
    "ERR_GATE_BYPASS_ALLOWED": "FAIL_POLICY",
    "ERR_SUPPRESS_TRACE_ALLOWED": "FAIL_POLICY",
    "ERR_SELF_APPROVAL": "FAIL_POLICY",
    "ERR_OLLAMA_UNBOUNDED_ACTION": "FAIL_POLICY",
    "ERR_NEED_MORE_EVIDENCE": "NEED_MORE_EVIDENCE",
    "ERR_POLICY_PARSE": "FAIL_POLICY",
}

VERDICT_PRIORITY = {
    "FAIL_SECRET_RISK": 0,
    "FAIL_RUNTIME_BINDING_ENABLED": 1,
    "FAIL_NEVER_ALLOWED_APPROVAL_PATH": 2,
    "FAIL_SCHEMA_MISSING_FIELD": 3,
    "FAIL_UNKNOWN_CLASS": 4,
    "FAIL_GATE_BINDING": 5,
    "FAIL_TRACE_BINDING": 6,
    "FAIL_EVAL_BINDING": 7,
    "FAIL_POLICY": 8,
    "BLOCKED_WITH_REASON": 9,
    "NEED_MORE_EVIDENCE": 10,
}

SEVERITY_PRIORITY = {"critical": 0, "high": 1, "medium": 2, "low": 3}

CANONICAL_CLASSES = {
    "READ_ONLY",
    "READ_SANITIZED",
    "WRITE_GATED",
    "RUNTIME_GATED",
    "HUMAN_APPROVAL_REQUIRED",
    "BLOCKED_BY_DEFAULT",
    "NEVER_ALLOWED",
}

CANONICAL_GATES = {
    "GATE_DOC_WRITE",
    "GATE_GLOBAL_INDEX",
    "GATE_GIT_PUSH",
    "GATE_BRANCH_DELETE",
    "GATE_MERGE",
    "GATE_RUNTIME",
    "GATE_OLLAMA_INSTALL",
    "GATE_MODEL_PULL",
    "GATE_SERVICE_RESTART",
    "GATE_SECRET",
    "GATE_TRADE",
    "GATE_MCP_WRITE",
    "GATE_REMOTE_EXEC",
    "GATE_DATABASE_MUTATION",
}

CANONICAL_TRACES = {
    "TRACE_SESSION",
    "TRACE_GO",
    "TRACE_WORKER",
    "TRACE_TOOL_CALL",
    "TRACE_MCP_CALL",
    "TRACE_CODEX_PATCH",
    "TRACE_GIT_ACTION",
    "TRACE_HUMAN_GATE",
    "TRACE_RUNTIME_READ",
    "TRACE_RUNTIME_GATED_ACTION",
    "TRACE_SECRET_BLOCK",
    "TRACE_TRADE_BLOCK",
    "TRACE_EVAL_RUN",
    "TRACE_VERDICT",
}

CANONICAL_EVALS = {
    "EVAL_DOC_ONLY_COMPLIANCE",
    "EVAL_NO_SECRET_LEAK",
    "EVAL_NO_RUNTIME_TOUCH",
    "EVAL_GATE_REQUIRED",
    "EVAL_GATE_APPROVAL_VALID",
    "EVAL_WORKER_SCOPE_COMPLIANCE",
    "EVAL_MCP_BOUNDARY_COMPLIANCE",
    "EVAL_TRACE_COMPLETENESS",
    "EVAL_ROLLBACK_READY",
    "EVAL_FINAL_VERDICT_VALIDITY",
}

REQUIRED_TOP_LEVEL = [
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

REQUIRED_POLICY_FIELDS = ["id", "status", "default_status", "runtime_binding", "secret_policy"]

ALLOWED_POLICY_STATUS = {
    "draft_doc_only",
    "review_only",
    "blocked",
    "approved_for_static_review",
}

NO_SECRET_POLICY_VALUES = {"no_secret_allowed", "NO_SECRET_VALUES", "NEVER_READ"}

FORBIDDEN_FIELD_NAMES = {
    "secret_value",
    "token_value",
    "password",
    "api_key_value",
    "private_key",
    "credential_blob",
    "raw_env",
    "raw_runtime_log",
    "sudo_password",
    "broker_order_payload",
}

FORBIDDEN_ACTION_IDS = {
    "secret_read": "ERR_SECRET_RISK",
    "credential_export": "ERR_SECRET_RISK",
    "trade_execution": "ERR_GATE_BYPASS_ALLOWED",
    "bypass_human_gate": "ERR_GATE_BYPASS_ALLOWED",
    "suppress_audit_trace": "ERR_SUPPRESS_TRACE_ALLOWED",
}

BLOCKED_OR_NEVER_IDS = {"unrestricted_shell", "sudo"}

_AWS_KEY_PREFIX = "AK" + "IA"
_KEY_MATERIAL_MARKER = "PRI" + "VATE" + " KEY"
_GITHUB_TOKEN_PREFIX = "gh" + "p_"
_SLACK_TOKEN_PREFIX = "xox" + "[baprs]-"
_OPENAI_TOKEN_PREFIX = "sk" + "-"

SECRET_VALUE_PATTERNS = [
    (re.compile(r"\bFAKE_SECRET_DO_NOT_USE\b"), "secret-like placeholder"),
    (re.compile(r"\bEXAMPLE_TOKEN_REDACTED\b"), "token-like placeholder"),
    (re.compile(r"\bDUMMY_CREDENTIAL_BLOCKED\b"), "credential-like placeholder"),
    (re.compile(r"\b" + _AWS_KEY_PREFIX + r"[0-9A-Z]{16}\b"), "aws access key pattern"),
    (re.compile(r"-----" + "BEGIN " + r"[A-Z ]*" + _KEY_MATERIAL_MARKER + "-----"), "private key marker"),
    (re.compile(r"\b" + _GITHUB_TOKEN_PREFIX + r"[A-Za-z0-9_]{20,}\b"), "github token pattern"),
    (re.compile(r"\b" + _SLACK_TOKEN_PREFIX + r"[A-Za-z0-9-]{10,}\b"), "slack token pattern"),
    (re.compile(r"\b" + _OPENAI_TOKEN_PREFIX + r"[A-Za-z0-9]{20,}\b"), "api token pattern"),
]


@dataclass(frozen=True)
class ValidationFinding:
    error_code: str
    verdict: str
    severity: str
    path: str
    message: str
    blocked_action: str = "policy_promotion"

    def to_dict(self) -> dict[str, str]:
        return {
            "error_code": self.error_code,
            "verdict": self.verdict,
            "severity": self.severity,
            "path": self.path,
            "message": self.message,
            "blocked_action": self.blocked_action,
        }


@dataclass
class ValidationReport:
    verdict: str
    errors: list[ValidationFinding] = field(default_factory=list)
    warnings: list[dict[str, str]] = field(default_factory=list)
    evidence_summary: list[str] = field(default_factory=list)
    blocked_capabilities: list[str] = field(default_factory=list)
    missing_gates: list[str] = field(default_factory=list)
    missing_traces: list[str] = field(default_factory=list)
    missing_evals: list[str] = field(default_factory=list)
    secret_risk_status: str = "not_detected"
    next_action: str = "eligible_for_human_review"

    @property
    def passed(self) -> bool:
        return self.verdict == PASS_VERDICT

    @property
    def exit_code(self) -> int:
        return 0 if self.passed else 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict,
            "passed": self.passed,
            "errors": [error.to_dict() for error in self.errors],
            "warnings": self.warnings,
            "evidence_summary": self.evidence_summary,
            "blocked_capabilities": sorted(set(self.blocked_capabilities)),
            "missing_gates": sorted(set(self.missing_gates)),
            "missing_traces": sorted(set(self.missing_traces)),
            "missing_evals": sorted(set(self.missing_evals)),
            "secret_risk_status": self.secret_risk_status,
            "next_action": self.next_action,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


class _ValidationContext:
    def __init__(self, source: str) -> None:
        self.source = source
        self.errors: list[ValidationFinding] = []
        self.warnings: list[dict[str, str]] = []
        self.blocked_capabilities: list[str] = []
        self.missing_gates: list[str] = []
        self.missing_traces: list[str] = []
        self.missing_evals: list[str] = []

    def add(
        self,
        error_code: str,
        path: str,
        message: str,
        *,
        severity: str = "high",
        blocked_action: str = "policy_promotion",
    ) -> None:
        self.errors.append(
            ValidationFinding(
                error_code=error_code,
                verdict=ERROR_VERDICTS[error_code],
                severity=severity,
                path=path,
                message=message,
                blocked_action=blocked_action,
            )
        )


def validate_policy_file(path: str | Path, *, requested_capability: str | None = None) -> ValidationReport:
    policy_path = Path(path)
    text = policy_path.read_text(encoding="utf-8")
    return validate_policy_text(text, source=str(policy_path), requested_capability=requested_capability)


def validate_policy_text(
    text: str,
    *,
    source: str = "<memory>",
    requested_capability: str | None = None,
) -> ValidationReport:
    ctx = _ValidationContext(source)
    _scan_raw_text_for_secret_risk(text, ctx)
    if ctx.errors:
        return _build_report(ctx, parsed=False)

    try:
        policy_data = parse_policy_yaml(text)
    except PolicyParseError:
        ctx.add(
            "ERR_POLICY_PARSE",
            source,
            "policy input could not be parsed by the static YAML subset parser",
            severity="high",
        )
        return _build_report(ctx, parsed=False)

    _scan_parsed_value_for_secret_risk(policy_data, ctx)
    if ctx.errors:
        return _build_report(ctx, parsed=True)

    _validate_schema(policy_data, ctx)
    if not _has_top_level_schema(policy_data):
        return _build_report(ctx, parsed=True)

    _validate_class_catalog(policy_data, ctx)
    gates = _ids_from_section(policy_data.get("gates"))
    traces = _ids_from_section(policy_data.get("traces"))
    evals = _ids_from_section(policy_data.get("evals"))
    _validate_id_catalog(gates, CANONICAL_GATES, "gates", "ERR_WRITE_WITHOUT_GATE", ctx)
    _validate_id_catalog(traces, CANONICAL_TRACES, "traces", "ERR_TRACE_FAMILY_UNKNOWN", ctx)
    _validate_id_catalog(evals, CANONICAL_EVALS, "evals", "ERR_EVAL_PROFILE_UNKNOWN", ctx)
    _validate_capabilities(policy_data, gates, traces, evals, ctx)
    _validate_never_allowed(policy_data.get("never_allowed"), ctx)
    _validate_blocked_by_default(policy_data, ctx)
    _validate_strict_workers(policy_data.get("strict_worker_roles"), ctx)
    _validate_ollama_lab(policy_data.get("ollama_lab_policy"), ctx)

    if requested_capability:
        _validate_requested_capability(requested_capability, policy_data, ctx)

    return _build_report(ctx, parsed=True)


def _scan_raw_text_for_secret_risk(text: str, ctx: _ValidationContext) -> None:
    for pattern, reason in SECRET_VALUE_PATTERNS:
        if pattern.search(text):
            ctx.add(
                "ERR_SECRET_RISK",
                ctx.source,
                f"secret risk detected in raw policy input: {reason}; value suppressed",
                severity="critical",
            )
            return


def _scan_parsed_value_for_secret_risk(value: Any, ctx: _ValidationContext, path: str = "policy_root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            lowered = key_text.lower()
            item_path = f"{path}.{key_text}"
            if lowered in FORBIDDEN_FIELD_NAMES and not path.endswith(".forbidden_fields"):
                ctx.add(
                    "ERR_SECRET_RISK",
                    item_path,
                    "forbidden secret-like field name detected; value suppressed",
                    severity="critical",
                )
                continue
            if lowered in {"credential_display", "credential_display_policy", "secret_display"}:
                if _value_implies_allow(item):
                    ctx.add(
                        "ERR_SECRET_RISK",
                        item_path,
                        "credential display policy is forbidden; value suppressed",
                        severity="critical",
                    )
                    continue
            _scan_parsed_value_for_secret_risk(item, ctx, item_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_parsed_value_for_secret_risk(item, ctx, f"{path}[{index}]")
    elif isinstance(value, str):
        for pattern, reason in SECRET_VALUE_PATTERNS:
            if pattern.search(value):
                ctx.add(
                    "ERR_SECRET_RISK",
                    path,
                    f"secret risk detected in field value: {reason}; value suppressed",
                    severity="critical",
                )
                return


def _validate_schema(policy_data: dict[str, Any], ctx: _ValidationContext) -> None:
    for field_name in REQUIRED_TOP_LEVEL:
        if field_name not in policy_data:
            ctx.add(
                "ERR_SCHEMA_MISSING_FIELD",
                field_name,
                "required top-level policy section is missing",
                severity="high",
            )

    policy = policy_data.get("policy")
    if not isinstance(policy, dict):
        ctx.add("ERR_SCHEMA_MISSING_FIELD", "policy", "policy section must be a map", severity="high")
        return

    for field_name in REQUIRED_POLICY_FIELDS:
        if field_name not in policy or policy[field_name] in {None, ""}:
            error_code = "ERR_SECRET_POLICY_MISSING" if field_name == "secret_policy" else "ERR_SCHEMA_MISSING_FIELD"
            ctx.add(error_code, f"policy.{field_name}", "required policy field is missing", severity="high")

    version = policy.get("version")
    policy_version = policy.get("policy_version")
    if not version and not policy_version:
        ctx.add("ERR_SCHEMA_MISSING_FIELD", "policy.version", "policy version is missing", severity="high")
    if version and policy_version and str(version) != str(policy_version):
        ctx.add(
            "ERR_POLICY_VERSION_CONFLICT",
            "policy.version",
            "policy.version and policy.policy_version conflict",
            severity="high",
        )

    status = policy.get("status")
    if status and status not in ALLOWED_POLICY_STATUS:
        ctx.add("ERR_POLICY_PARSE", "policy.status", "policy status is not static-review safe", severity="high")

    if policy.get("default_status") and policy.get("default_status") != "BLOCKED_BY_DEFAULT":
        ctx.add(
            "ERR_DEFAULT_ALLOW_BLOCKED_CLASS",
            "policy.default_status",
            "policy default_status must be BLOCKED_BY_DEFAULT",
            severity="high",
        )

    if "runtime_binding" in policy and policy.get("runtime_binding") is not False:
        ctx.add(
            "ERR_RUNTIME_BINDING_ENABLED",
            "policy.runtime_binding",
            "runtime binding must remain false",
            severity="critical",
            blocked_action="runtime_use",
        )

    secret_policy = policy.get("secret_policy")
    if secret_policy and secret_policy not in NO_SECRET_POLICY_VALUES:
        ctx.add(
            "ERR_SECRET_RISK",
            "policy.secret_policy",
            "secret policy must explicitly forbid secrets",
            severity="critical",
        )

    unknown_capability = policy.get("unknown_capability")
    if unknown_capability and unknown_capability != "BLOCKED_BY_DEFAULT":
        ctx.add(
            "ERR_UNKNOWN_CAPABILITY",
            "policy.unknown_capability",
            "unknown capability must resolve to BLOCKED_BY_DEFAULT",
            severity="high",
        )


def _has_top_level_schema(policy_data: dict[str, Any]) -> bool:
    if any(field_name not in policy_data for field_name in REQUIRED_TOP_LEVEL):
        return False
    policy = policy_data.get("policy")
    if not isinstance(policy, dict):
        return False
    if any(field_name not in policy for field_name in REQUIRED_POLICY_FIELDS):
        return False
    if not (policy.get("version") or policy.get("policy_version")):
        return False
    return True


def _validate_class_catalog(policy_data: dict[str, Any], ctx: _ValidationContext) -> None:
    capability_classes = policy_data.get("capability_classes")
    if not isinstance(capability_classes, dict):
        ctx.add(
            "ERR_SCHEMA_MISSING_FIELD",
            "capability_classes",
            "capability_classes must be a map",
            severity="high",
        )
        return

    for class_name, config in capability_classes.items():
        if class_name not in CANONICAL_CLASSES:
            ctx.add(
                "ERR_UNKNOWN_CLASS",
                f"capability_classes.{class_name}",
                "capability class is not canonical",
                severity="high",
            )
            continue
        if not isinstance(config, dict):
            continue
        default_allowed = config.get("default_allowed")
        approval_path = config.get("approval_path")
        if class_name in {"WRITE_GATED", "RUNTIME_GATED", "HUMAN_APPROVAL_REQUIRED", "BLOCKED_BY_DEFAULT", "NEVER_ALLOWED"}:
            if default_allowed is True:
                ctx.add(
                    "ERR_DEFAULT_ALLOW_BLOCKED_CLASS",
                    f"capability_classes.{class_name}.default_allowed",
                    "blocked or gated capability class cannot be default allowed",
                    severity="high",
                )
        if class_name == "NEVER_ALLOWED" and not _is_none_value(approval_path):
            ctx.add(
                "ERR_NEVER_ALLOWED_APPROVAL_PATH",
                f"capability_classes.{class_name}.approval_path",
                "NEVER_ALLOWED class cannot have an approval path",
                severity="critical",
            )


def _validate_id_catalog(
    ids: set[str],
    canonical: set[str],
    section: str,
    error_code: str,
    ctx: _ValidationContext,
) -> None:
    for item_id in ids:
        if item_id not in canonical:
            ctx.add(
                error_code,
                f"{section}.{item_id}",
                f"{section} id is not canonical",
                severity="high",
            )


def _validate_capabilities(
    policy_data: dict[str, Any],
    gates: set[str],
    traces: set[str],
    evals: set[str],
    ctx: _ValidationContext,
) -> None:
    capabilities = _normalize_capabilities(policy_data.get("capabilities"), ctx)
    for capability in capabilities:
        capability_id = str(capability.get("capability_id") or capability.get("id") or "<unknown>")
        path = f"capabilities.{capability_id}"
        class_name = capability.get("capability_class", capability.get("class"))
        if not class_name:
            ctx.add(
                "ERR_SCHEMA_MISSING_FIELD",
                f"{path}.capability_class",
                "capability_class is required",
                severity="high",
            )
            continue
        if class_name not in CANONICAL_CLASSES:
            ctx.add(
                "ERR_UNKNOWN_CLASS",
                f"{path}.capability_class",
                "capability class is not canonical",
                severity="high",
            )
            continue

        _validate_capability_deny_rules(capability_id, class_name, capability, path, ctx)
        _validate_capability_class_rules(capability_id, class_name, capability, path, ctx)
        _validate_capability_gate(class_name, capability, path, gates, ctx)
        _validate_capability_trace(class_name, capability, path, traces, ctx)
        _validate_capability_eval(class_name, capability, path, evals, ctx)


def _normalize_capabilities(value: Any, ctx: _ValidationContext) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        normalized = []
        for capability_id, config in value.items():
            if not isinstance(config, dict):
                ctx.add(
                    "ERR_POLICY_PARSE",
                    f"capabilities.{capability_id}",
                    "capability entry must be a map",
                    severity="high",
                )
                continue
            entry = dict(config)
            entry.setdefault("capability_id", capability_id)
            normalized.append(entry)
        return normalized
    if isinstance(value, list):
        normalized = []
        for index, config in enumerate(value):
            if not isinstance(config, dict):
                ctx.add(
                    "ERR_POLICY_PARSE",
                    f"capabilities[{index}]",
                    "capability list entry must be a map",
                    severity="high",
                )
                continue
            normalized.append(config)
        return normalized
    ctx.add("ERR_SCHEMA_MISSING_FIELD", "capabilities", "capabilities must be a map or list", severity="high")
    return []


def _validate_capability_deny_rules(
    capability_id: str,
    class_name: str,
    capability: dict[str, Any],
    path: str,
    ctx: _ValidationContext,
) -> None:
    if capability_id in FORBIDDEN_ACTION_IDS and class_name != "NEVER_ALLOWED":
        error_code = FORBIDDEN_ACTION_IDS[capability_id]
        ctx.add(
            error_code,
            f"{path}.capability_class",
            "forbidden capability must be NEVER_ALLOWED",
            severity="critical",
            blocked_action=capability_id,
        )
    if capability_id in BLOCKED_OR_NEVER_IDS and class_name not in {"BLOCKED_BY_DEFAULT", "NEVER_ALLOWED"}:
        ctx.add(
            "ERR_GATE_BYPASS_ALLOWED",
            f"{path}.capability_class",
            "blocked capability cannot be allowed implicitly",
            severity="critical",
            blocked_action=capability_id,
        )
    if capability_id == "trade_execution" and _value_implies_allow(capability):
        ctx.add(
            "ERR_GATE_BYPASS_ALLOWED",
            path,
            "trade execution cannot be allowed by this static policy",
            severity="critical",
            blocked_action=capability_id,
        )


def _validate_capability_class_rules(
    capability_id: str,
    class_name: str,
    capability: dict[str, Any],
    path: str,
    ctx: _ValidationContext,
) -> None:
    default_allowed = capability.get("default_allowed")
    if class_name in {"WRITE_GATED", "RUNTIME_GATED", "HUMAN_APPROVAL_REQUIRED", "BLOCKED_BY_DEFAULT", "NEVER_ALLOWED"}:
        if default_allowed is True:
            ctx.add(
                "ERR_DEFAULT_ALLOW_BLOCKED_CLASS",
                f"{path}.default_allowed",
                "gated, blocked, or never-allowed capability cannot be default allowed",
                severity="high",
                blocked_action=capability_id,
            )
    if class_name == "READ_SANITIZED":
        output_policy = capability.get("output_policy")
        if not _contains_word(output_policy, "sanitized"):
            ctx.add(
                "ERR_READ_SANITIZED_OUTPUT",
                f"{path}.output_policy",
                "READ_SANITIZED capability requires sanitized output policy",
                severity="high",
                blocked_action=capability_id,
            )
    if class_name == "NEVER_ALLOWED":
        approval_path = capability.get("approval_path")
        if not _is_none_value(approval_path):
            ctx.add(
                "ERR_NEVER_ALLOWED_APPROVAL_PATH",
                f"{path}.approval_path",
                "NEVER_ALLOWED capability cannot have an approval path",
                severity="critical",
                blocked_action=capability_id,
            )
        allowed_actor = capability.get("allowed_actor")
        if allowed_actor and not _is_none_value(allowed_actor):
            ctx.add(
                "ERR_GATE_BYPASS_ALLOWED",
                f"{path}.allowed_actor",
                "NEVER_ALLOWED capability cannot define allowed actors",
                severity="critical",
                blocked_action=capability_id,
            )
    if class_name == "RUNTIME_GATED" and capability.get("rollback_required") is not True:
        ctx.add(
            "ERR_MISSING_ROLLBACK",
            f"{path}.rollback_required",
            "RUNTIME_GATED capability requires rollback_required true",
            severity="high",
            blocked_action=capability_id,
        )


def _validate_capability_gate(
    class_name: str,
    capability: dict[str, Any],
    path: str,
    gates: set[str],
    ctx: _ValidationContext,
) -> None:
    gate_required = capability.get("gate_required")
    gate_id = capability.get("gate_id")
    if class_name in {"WRITE_GATED", "RUNTIME_GATED", "HUMAN_APPROVAL_REQUIRED"}:
        error_code = "ERR_RUNTIME_WITHOUT_GATE" if class_name == "RUNTIME_GATED" else "ERR_WRITE_WITHOUT_GATE"
        if gate_required is not True:
            ctx.missing_gates.append(path)
            ctx.add(
                error_code,
                f"{path}.gate_required",
                f"{class_name} requires gate_required true",
                severity="critical" if class_name == "RUNTIME_GATED" else "high",
            )
            return
        gate_values = _as_id_set(gate_id)
        if not gate_values or "none" in {gate.lower() for gate in gate_values}:
            ctx.missing_gates.append(path)
            ctx.add(
                error_code,
                f"{path}.gate_id",
                f"{class_name} requires a valid gate_id",
                severity="critical" if class_name == "RUNTIME_GATED" else "high",
            )
            return
        for item_id in gate_values:
            if item_id not in CANONICAL_GATES or item_id not in gates:
                ctx.missing_gates.append(item_id)
                ctx.add(
                    error_code,
                    f"{path}.gate_id",
                    "gate_id does not reference a declared canonical gate",
                    severity="high",
                )


def _validate_capability_trace(
    class_name: str,
    capability: dict[str, Any],
    path: str,
    traces: set[str],
    ctx: _ValidationContext,
) -> None:
    if capability.get("trace_required") is not True:
        ctx.missing_traces.append(path)
        ctx.add(
            "ERR_TRACE_REQUIRED_MISSING",
            f"{path}.trace_required",
            "trace_required must be true for every capability",
            severity="high",
        )
        return
    trace_values = _as_id_set(capability.get("trace_family", capability.get("trace_families")))
    if not trace_values:
        ctx.missing_traces.append(path)
        ctx.add(
            "ERR_TRACE_REQUIRED_MISSING",
            f"{path}.trace_family",
            "trace_family is required for every capability",
            severity="high",
        )
        return
    for item_id in trace_values:
        if item_id not in CANONICAL_TRACES or item_id not in traces:
            ctx.missing_traces.append(item_id)
            ctx.add(
                "ERR_TRACE_FAMILY_UNKNOWN",
                f"{path}.trace_family",
                "trace family does not reference a declared canonical trace",
                severity="high",
            )
    if class_name in {"WRITE_GATED", "RUNTIME_GATED", "HUMAN_APPROVAL_REQUIRED"} and "TRACE_HUMAN_GATE" not in traces:
        ctx.missing_traces.append("TRACE_HUMAN_GATE")
        ctx.add(
            "ERR_TRACE_REQUIRED_MISSING",
            "traces.TRACE_HUMAN_GATE",
            "gated capabilities require TRACE_HUMAN_GATE in the policy trace catalog",
            severity="high",
        )
    if "TRACE_VERDICT" not in traces:
        ctx.missing_traces.append("TRACE_VERDICT")
        ctx.add(
            "ERR_TRACE_REQUIRED_MISSING",
            "traces.TRACE_VERDICT",
            "final verdict trace is required",
            severity="high",
        )


def _validate_capability_eval(
    class_name: str,
    capability: dict[str, Any],
    path: str,
    evals: set[str],
    ctx: _ValidationContext,
) -> None:
    if capability.get("eval_required") is not True:
        ctx.missing_evals.append(path)
        ctx.add(
            "ERR_EVAL_REQUIRED_MISSING",
            f"{path}.eval_required",
            "eval_required must be true for every capability",
            severity="high",
        )
        return
    eval_values = _as_id_set(capability.get("eval_profile", capability.get("eval_profiles")))
    if not eval_values:
        ctx.missing_evals.append(path)
        ctx.add(
            "ERR_EVAL_REQUIRED_MISSING",
            f"{path}.eval_profile",
            "eval_profile is required for every capability",
            severity="high",
        )
        return
    for item_id in eval_values:
        if item_id not in CANONICAL_EVALS or item_id not in evals:
            ctx.missing_evals.append(item_id)
            ctx.add(
                "ERR_EVAL_PROFILE_UNKNOWN",
                f"{path}.eval_profile",
                "eval profile does not reference a declared canonical eval",
                severity="high",
            )
    if class_name in {"WRITE_GATED", "RUNTIME_GATED", "HUMAN_APPROVAL_REQUIRED"} and "EVAL_GATE_REQUIRED" not in evals:
        ctx.missing_evals.append("EVAL_GATE_REQUIRED")
        ctx.add(
            "ERR_EVAL_REQUIRED_MISSING",
            "evals.EVAL_GATE_REQUIRED",
            "gated capabilities require EVAL_GATE_REQUIRED in the policy eval catalog",
            severity="high",
        )


def _validate_never_allowed(value: Any, ctx: _ValidationContext) -> None:
    entries: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        entries = [(str(key), item) for key, item in value.items()]
    elif isinstance(value, list):
        entries = [(str(index), item) for index, item in enumerate(value)]
    for name, item in entries:
        path = f"never_allowed.{name}"
        if isinstance(item, dict):
            approval_path = item.get("approval_path")
            if not _is_none_value(approval_path):
                ctx.add(
                    "ERR_NEVER_ALLOWED_APPROVAL_PATH",
                    f"{path}.approval_path",
                    "never_allowed entry cannot have approval path",
                    severity="critical",
                    blocked_action=name,
                )
            class_name = item.get("capability_class", item.get("class"))
            if class_name and class_name != "NEVER_ALLOWED":
                ctx.add(
                    "ERR_GATE_BYPASS_ALLOWED",
                    f"{path}.capability_class",
                    "never_allowed entry must remain NEVER_ALLOWED",
                    severity="critical",
                    blocked_action=name,
                )
        elif isinstance(item, str) and item.lower() not in {"blocked", "never_allowed", "none"}:
            ctx.add(
                "ERR_NEVER_ALLOWED_APPROVAL_PATH",
                path,
                "never_allowed scalar entry is not a blocking value",
                severity="critical",
                blocked_action=name,
            )


def _validate_blocked_by_default(policy_data: dict[str, Any], ctx: _ValidationContext) -> None:
    blocked = policy_data.get("blocked_by_default")
    governor = policy_data.get("governor_decision_rules")
    for section_name, section in {
        "blocked_by_default": blocked,
        "governor_decision_rules": governor,
    }.items():
        if not isinstance(section, dict):
            continue
        unknown_value = section.get("unknown_capability")
        if unknown_value and unknown_value != "BLOCKED_BY_DEFAULT":
            ctx.add(
                "ERR_UNKNOWN_CAPABILITY",
                f"{section_name}.unknown_capability",
                "unknown capability must be blocked by default",
                severity="high",
            )
        if section.get("default_allowed") is True:
            ctx.add(
                "ERR_DEFAULT_ALLOW_BLOCKED_CLASS",
                f"{section_name}.default_allowed",
                "blocked-by-default behavior cannot be default allowed",
                severity="high",
            )


def _validate_strict_workers(value: Any, ctx: _ValidationContext) -> None:
    if not isinstance(value, dict):
        return
    for role, config in value.items():
        if not isinstance(config, dict):
            continue
        path = f"strict_worker_roles.{role}"
        if config.get("self_approval") is True or config.get("can_self_approve") is True:
            ctx.add(
                "ERR_SELF_APPROVAL",
                f"{path}.self_approval",
                "strict worker cannot self-approve",
                severity="critical",
                blocked_action="human_approval",
            )
        allowed = _as_id_set(config.get("allowed_capabilities"))
        if allowed.intersection({"secret_read", "credential_export"}):
            ctx.add(
                "ERR_SECRET_RISK",
                f"{path}.allowed_capabilities",
                "strict worker cannot allow secret access",
                severity="critical",
            )
        if allowed.intersection({"trade_execution", "unrestricted_shell", "sudo"}):
            ctx.add(
                "ERR_GATE_BYPASS_ALLOWED",
                f"{path}.allowed_capabilities",
                "strict worker capability is outside allowed safety scope",
                severity="critical",
            )
        if config.get("runtime_gate_required") is False and allowed.intersection(
            {"service_restart", "model_pull", "provider_switch", "install", "smoke_test_no_trade"}
        ):
            ctx.add(
                "ERR_RUNTIME_WITHOUT_GATE",
                f"{path}.runtime_gate_required",
                "strict worker runtime action requires a gate",
                severity="critical",
            )
        if "verdict" in config and _is_none_value(config.get("verdict")):
            ctx.add(
                "ERR_NEED_MORE_EVIDENCE",
                f"{path}.verdict",
                "strict worker output requires explicit verdict",
                severity="medium",
            )


def _validate_ollama_lab(value: Any, ctx: _ValidationContext) -> None:
    if not isinstance(value, dict):
        return
    for action in ["model_pull", "provider_switch", "service_restart", "install"]:
        config = value.get(action)
        if isinstance(config, dict):
            gate_id = config.get("gate_id")
            if not gate_id or _is_none_value(gate_id):
                ctx.add(
                    "ERR_OLLAMA_UNBOUNDED_ACTION",
                    f"ollama_lab_policy.{action}.gate_id",
                    "Ollama Lab mutating action requires a gate",
                    severity="high",
                    blocked_action=action,
                )
    for action in ["trade_execution", "secret_read", "unrestricted_shell"]:
        if _value_implies_allow(value.get(action)):
            error_code = "ERR_SECRET_RISK" if action == "secret_read" else "ERR_GATE_BYPASS_ALLOWED"
            ctx.add(
                error_code,
                f"ollama_lab_policy.{action}",
                "Ollama Lab policy cannot allow this action",
                severity="critical",
                blocked_action=action,
            )


def _validate_requested_capability(
    capability_id: str,
    policy_data: dict[str, Any],
    ctx: _ValidationContext,
) -> None:
    capabilities = _normalize_capabilities(policy_data.get("capabilities"), ctx)
    known = {str(item.get("capability_id") or item.get("id")) for item in capabilities}
    if capability_id not in known:
        ctx.blocked_capabilities.append(capability_id)
        ctx.add(
            "ERR_UNKNOWN_CAPABILITY",
            f"capabilities.{capability_id}",
            "requested capability is unknown and blocked by default",
            severity="medium",
            blocked_action=capability_id,
        )


def _build_report(ctx: _ValidationContext, *, parsed: bool) -> ValidationReport:
    if ctx.errors:
        sorted_errors = sorted(
            ctx.errors,
            key=lambda item: (
                VERDICT_PRIORITY.get(item.verdict, 99),
                SEVERITY_PRIORITY.get(item.severity, 99),
                item.path,
                item.error_code,
            ),
        )
        verdict = sorted_errors[0].verdict
        next_action = "blocked_until_policy_is_fixed"
        secret_risk_status = "detected" if any(error.error_code == "ERR_SECRET_RISK" for error in sorted_errors) else "not_detected"
    else:
        sorted_errors = []
        verdict = PASS_VERDICT
        next_action = "eligible_for_human_review"
        secret_risk_status = "not_detected"
    evidence = [
        f"source={ctx.source}",
        "mode=static_read_only",
        f"parsed={str(parsed).lower()}",
        "runtime_binding=not_loaded",
        "mcp_live_call=not_called",
    ]
    return ValidationReport(
        verdict=verdict,
        errors=sorted_errors,
        warnings=ctx.warnings,
        evidence_summary=evidence,
        blocked_capabilities=ctx.blocked_capabilities,
        missing_gates=ctx.missing_gates,
        missing_traces=ctx.missing_traces,
        missing_evals=ctx.missing_evals,
        secret_risk_status=secret_risk_status,
        next_action=next_action,
    )


def _ids_from_section(value: Any) -> set[str]:
    if isinstance(value, dict):
        return {str(key) for key in value}
    if isinstance(value, list):
        ids = set()
        for item in value:
            if isinstance(item, dict):
                item_id = item.get("id") or item.get("trace_family") or item.get("eval_profile") or item.get("gate_id")
                if item_id:
                    ids.add(str(item_id))
            else:
                ids.add(str(item))
        return ids
    return set()


def _as_id_set(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, list):
        return {str(item) for item in value if item is not None}
    if isinstance(value, set):
        return {str(item) for item in value if item is not None}
    if isinstance(value, dict):
        return {str(key) for key in value}
    return {str(value)}


def _is_none_value(value: Any) -> bool:
    if value is None:
        return True
    if value is False:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"none", "not_applicable", "null", "false", ""}
    if isinstance(value, list):
        return len(value) == 0
    return False


def _value_implies_allow(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {
            "allow",
            "allowed",
            "true",
            "yes",
            "approved",
            "human_gate",
            "approvable",
        }
    if isinstance(value, list):
        return any(_value_implies_allow(item) for item in value)
    if isinstance(value, dict):
        return any(_value_implies_allow(item) for item in value.values())
    return False


def _contains_word(value: Any, expected: str) -> bool:
    expected = expected.lower()
    if isinstance(value, str):
        return expected in value.lower()
    if isinstance(value, list):
        return any(_contains_word(item, expected) for item in value)
    if isinstance(value, dict):
        return any(_contains_word(item, expected) for item in value.values())
    return False
