import json
import subprocess
import sys
import textwrap

from modules.governance.openclaw_mcp_policy_validator import validate_policy_text


def make_policy(capability_block: str, extra_policy: str = "", extra_sections: str = "") -> str:
    lines = [
        "policy:",
        "  id: OPENCLAW_MCP_POLICY_TEST_01",
        "  version: 0.1-test",
        "  status: draft_doc_only",
        "  default_status: BLOCKED_BY_DEFAULT",
        "  runtime_binding: false",
        "  secret_policy: no_secret_allowed",
        "  unknown_capability: BLOCKED_BY_DEFAULT",
    ]
    if extra_policy.strip():
        lines.append(textwrap.indent(textwrap.dedent(extra_policy).strip(), "  "))
    lines.extend(
        [
            "capability_classes:",
            "  READ_ONLY:",
            "    default_allowed: true",
            "    approval_path: none",
            "  READ_SANITIZED:",
            "    default_allowed: true",
            "    approval_path: conditional",
            "  WRITE_GATED:",
            "    default_allowed: false",
            "    approval_path: human_gate",
            "  RUNTIME_GATED:",
            "    default_allowed: false",
            "    approval_path: human_gate",
            "  HUMAN_APPROVAL_REQUIRED:",
            "    default_allowed: false",
            "    approval_path: human_gate",
            "  BLOCKED_BY_DEFAULT:",
            "    default_allowed: false",
            "    approval_path: none",
            "  NEVER_ALLOWED:",
            "    default_allowed: false",
            "    approval_path: none",
            "capabilities:",
            textwrap.indent(textwrap.dedent(capability_block).strip(), "  "),
            "gates:",
            "  GATE_DOC_WRITE: {}",
            "  GATE_RUNTIME: {}",
            "  GATE_SECRET: {}",
            "  GATE_TRADE: {}",
            "traces:",
            "  TRACE_MCP_CALL: {}",
            "  TRACE_HUMAN_GATE: {}",
            "  TRACE_RUNTIME_GATED_ACTION: {}",
            "  TRACE_SECRET_BLOCK: {}",
            "  TRACE_TRADE_BLOCK: {}",
            "  TRACE_VERDICT: {}",
            "evals:",
            "  EVAL_MCP_BOUNDARY_COMPLIANCE: {}",
            "  EVAL_NO_SECRET_LEAK: {}",
            "  EVAL_NO_RUNTIME_TOUCH: {}",
            "  EVAL_GATE_REQUIRED: {}",
            "  EVAL_GATE_APPROVAL_VALID: {}",
            "  EVAL_ROLLBACK_READY: {}",
            "  EVAL_TRACE_COMPLETENESS: {}",
            "  EVAL_FINAL_VERDICT_VALIDITY: {}",
            "strict_worker_roles:",
            "  Repo Auditor:",
            "    allowed_capabilities:",
            "      - repo_state",
            "    blocked_capabilities:",
            "      - secret_read",
            "    self_approval: false",
            "ollama_lab_policy:",
            "  ollama_health_check: read_only_or_gated",
            "governor_decision_rules:",
            "  unknown_capability: BLOCKED_BY_DEFAULT",
            "never_allowed:",
            "  secret_read:",
            "    capability_class: NEVER_ALLOWED",
            "    approval_path: none",
            "blocked_by_default:",
            "  unknown_capability: BLOCKED_BY_DEFAULT",
        ]
    )
    if extra_sections.strip():
        lines.append(textwrap.dedent(extra_sections).strip())
    return "\n".join(lines) + "\n"


READ_ONLY_CAPABILITY = """
repo_state:
  capability_class: READ_ONLY
  default_allowed: true
  gate_required: false
  gate_id: none
  trace_required: true
  trace_family: TRACE_MCP_CALL
  eval_required: true
  eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
  secret_policy: no_secret_allowed
  output_policy: bounded_summary
"""


def assert_verdict(policy_text: str, verdict: str, error_code: str | None = None):
    report = validate_policy_text(policy_text)
    assert report.verdict == verdict
    if error_code is not None:
        assert report.errors
        assert report.errors[0].error_code == error_code
    return report


def test_valid_minimal_policy_passes():
    assert_verdict(make_policy(READ_ONLY_CAPABILITY), "PASS_POLICY_STATIC_VALIDATION")


def test_missing_policy_id_fails_schema():
    policy = make_policy(READ_ONLY_CAPABILITY).replace("  id: OPENCLAW_MCP_POLICY_TEST_01\n", "")
    assert_verdict(policy, "FAIL_SCHEMA_MISSING_FIELD", "ERR_SCHEMA_MISSING_FIELD")


def test_unknown_capability_class_fails():
    policy = make_policy(READ_ONLY_CAPABILITY.replace("READ_ONLY", "UNKNOWN_CLASS"))
    assert_verdict(policy, "FAIL_UNKNOWN_CLASS", "ERR_UNKNOWN_CLASS")


def test_write_gated_without_gate_fails():
    capability = """
    create_doc_file:
      capability_class: WRITE_GATED
      default_allowed: false
      gate_required: true
      gate_id: none
      trace_required: true
      trace_family: TRACE_HUMAN_GATE
      eval_required: true
      eval_profile: EVAL_GATE_REQUIRED
      rollback_required: true
    """
    assert_verdict(make_policy(capability), "FAIL_GATE_BINDING", "ERR_WRITE_WITHOUT_GATE")


def test_missing_trace_binding_fails():
    policy = make_policy(READ_ONLY_CAPABILITY.replace("  trace_required: true\n", "  trace_required: false\n"))
    assert_verdict(policy, "FAIL_TRACE_BINDING", "ERR_TRACE_REQUIRED_MISSING")


def test_missing_eval_binding_fails():
    policy = make_policy(READ_ONLY_CAPABILITY.replace("  eval_required: true\n", "  eval_required: false\n"))
    assert_verdict(policy, "FAIL_EVAL_BINDING", "ERR_EVAL_REQUIRED_MISSING")


def test_never_allowed_with_approval_path_fails():
    capability = """
    secret_read:
      capability_class: NEVER_ALLOWED
      default_allowed: false
      gate_required: false
      gate_id: none
      trace_required: true
      trace_family: TRACE_SECRET_BLOCK
      eval_required: true
      eval_profile: EVAL_NO_SECRET_LEAK
      approval_path: human_gate
    """
    assert_verdict(
        make_policy(capability),
        "FAIL_NEVER_ALLOWED_APPROVAL_PATH",
        "ERR_NEVER_ALLOWED_APPROVAL_PATH",
    )


def test_secret_like_value_fails_without_echoing_value():
    policy = make_policy(READ_ONLY_CAPABILITY, extra_policy="note: FAKE_SECRET_DO_NOT_USE")
    report = assert_verdict(policy, "FAIL_SECRET_RISK", "ERR_SECRET_RISK")
    assert "FAKE_SECRET_DO_NOT_USE" not in report.to_json()


def test_runtime_binding_true_fails():
    policy = make_policy(READ_ONLY_CAPABILITY).replace("  runtime_binding: false\n", "  runtime_binding: true\n")
    assert_verdict(policy, "FAIL_RUNTIME_BINDING_ENABLED", "ERR_RUNTIME_BINDING_ENABLED")


def test_unknown_capability_must_be_blocked_by_default():
    policy = make_policy(READ_ONLY_CAPABILITY).replace(
        "unknown_capability: BLOCKED_BY_DEFAULT",
        "unknown_capability: ALLOW",
        1,
    )
    assert_verdict(policy, "BLOCKED_WITH_REASON", "ERR_UNKNOWN_CAPABILITY")


def test_requested_unknown_capability_blocks():
    report = validate_policy_text(make_policy(READ_ONLY_CAPABILITY), requested_capability="missing_tool")
    assert report.verdict == "BLOCKED_WITH_REASON"
    assert report.errors[0].error_code == "ERR_UNKNOWN_CAPABILITY"
    assert report.blocked_capabilities == ["missing_tool"]


def test_cli_outputs_json_and_exit_code(tmp_path):
    policy_file = tmp_path / "policy.yaml"
    policy_file.write_text(make_policy(READ_ONLY_CAPABILITY), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "modules.governance.openclaw_mcp_policy_validator", str(policy_file)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "PASS_POLICY_STATIC_VALIDATION"
    assert payload["passed"] is True
