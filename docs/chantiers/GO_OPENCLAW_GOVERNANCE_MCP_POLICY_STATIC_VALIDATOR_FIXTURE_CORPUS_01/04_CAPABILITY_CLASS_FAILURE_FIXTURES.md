# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01 -- 04_CAPABILITY_CLASS_FAILURE_FIXTURES

## 1_MASTER_TARGET

Define capability class failure fixtures.

## 2_INITIAL_PROJECT_DOC

These fixtures test the seven canonical capability classes and class-specific invariants.

## 3_INITIAL_NEED

The validator must reject unknown classes and internally inconsistent class metadata.

## 4_MASTER_PROJECT_PLAN

Create fixtures for unknown class, unsanitized sanitized read, write-gated default allow, runtime-gated without gate, and blocked-by-default allowed true.

## 6_FINAL_TARGET

Every class failure fixture maps to `FAIL_UNKNOWN_CLASS`, `FAIL_GATE_BINDING`, or `FAIL_POLICY`.

## 7_CANONICAL_STATE

Canonical classes:

```text
READ_ONLY
READ_SANITIZED
WRITE_GATED
RUNTIME_GATED
HUMAN_APPROVAL_REQUIRED
BLOCKED_BY_DEFAULT
NEVER_ALLOWED
```

## 8_VALIDATED_PLAN

### FAIL_UNKNOWN_CLASS_01

```text
fixture_id: FAIL_UNKNOWN_CLASS_01
purpose: unknown capability class must fail
expected_verdict: FAIL_UNKNOWN_CLASS
expected_error_code: ERR_UNKNOWN_CLASS
policy_snippet:
  capability_id: repo_state
  capability_class: READ_BUT_NOT_CANONICAL
  default_status: ALLOW_IF_BOUNDED
why: capability_class is not in the canonical enum
related_validator_rule: CLASS_ENUM_VALIDITY
related_gate: none
related_trace: TRACE_MCP_CALL
related_eval: EVAL_MCP_BOUNDARY_COMPLIANCE
```

### FAIL_READ_SANITIZED_WITHOUT_SANITIZED_OUTPUT_01

```text
fixture_id: FAIL_READ_SANITIZED_WITHOUT_SANITIZED_OUTPUT_01
purpose: sanitized read must define sanitized output
expected_verdict: FAIL_POLICY
expected_error_code: ERR_READ_SANITIZED_OUTPUT
policy_snippet:
  capability_id: logs_tail_sanitized
  capability_class: READ_SANITIZED
  default_status: ALLOW_IF_SANITIZED
  output_policy: raw_log_excerpt
  trace_required: true
  trace_family: TRACE_RUNTIME_READ
  eval_required: true
  eval_profile: EVAL_NO_SECRET_LEAK
why: READ_SANITIZED requires sanitized output and cannot expose raw logs
related_validator_rule: CLASS_READ_SANITIZED_OUTPUT
related_gate: none
related_trace: TRACE_RUNTIME_READ
related_eval: EVAL_NO_SECRET_LEAK
```

### FAIL_WRITE_GATED_DEFAULT_ALLOWED_01

```text
fixture_id: FAIL_WRITE_GATED_DEFAULT_ALLOWED_01
purpose: write-gated capability cannot be default allowed
expected_verdict: FAIL_POLICY
expected_error_code: ERR_DEFAULT_ALLOW_BLOCKED_CLASS
policy_snippet:
  capability_id: create_doc_file
  capability_class: WRITE_GATED
  default_status: ALLOW_IF_BOUNDED
  gate_required: true
  gate_id: GATE_DOC_WRITE
why: WRITE_GATED must be blocked until gate and cannot default allow
related_validator_rule: CLASS_WRITE_GATED_DEFAULT_DENY
related_gate: GATE_DOC_WRITE
related_trace: TRACE_CODEX_PATCH
related_eval: EVAL_GATE_REQUIRED
```

### FAIL_RUNTIME_GATED_WITHOUT_GATE_01

```text
fixture_id: FAIL_RUNTIME_GATED_WITHOUT_GATE_01
purpose: runtime-gated capability must have a valid gate
expected_verdict: FAIL_GATE_BINDING
expected_error_code: ERR_RUNTIME_WITHOUT_GATE
policy_snippet:
  capability_id: ollama_health_check
  capability_class: RUNTIME_GATED
  default_status: NEEDS_GATE
  gate_required: true
  gate_id: none
  trace_required: true
  trace_family: TRACE_RUNTIME_READ
  eval_required: true
  eval_profile: EVAL_NO_RUNTIME_TOUCH
why: RUNTIME_GATED requires a valid runtime gate
related_validator_rule: CLASS_RUNTIME_GATED_GATE_REQUIRED
related_gate: GATE_RUNTIME
related_trace: TRACE_RUNTIME_READ
related_eval: EVAL_NO_RUNTIME_TOUCH
```

### FAIL_BLOCKED_BY_DEFAULT_ALLOWED_TRUE_01

```text
fixture_id: FAIL_BLOCKED_BY_DEFAULT_ALLOWED_TRUE_01
purpose: blocked-by-default class must not be allowed
expected_verdict: FAIL_POLICY
expected_error_code: ERR_DEFAULT_ALLOW_BLOCKED_CLASS
policy_snippet:
  capability_id: unknown_command_surface
  capability_class: BLOCKED_BY_DEFAULT
  default_allowed: true
  default_status: BLOCKED_BY_DEFAULT
  trace_required: true
  trace_family: TRACE_MCP_CALL
  eval_required: true
  eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
why: BLOCKED_BY_DEFAULT cannot be default allowed
related_validator_rule: CLASS_BLOCKED_BY_DEFAULT_DENY
related_gate: none
related_trace: TRACE_MCP_CALL
related_eval: EVAL_MCP_BOUNDARY_COMPLIANCE
```

## 9_SELECTED_SOLUTION

Class fixtures isolate class errors before gate, trace, or eval cross-reference checks where possible.

## 12_INVARIANTS

- Unknown class fails.
- Gated classes cannot be default allowed.
- Sanitized classes must define sanitized outputs.
- Blocked classes stay blocked.

## 13_ESTABLISHED

The class list comes from MCP Boundary and MCP Policy Schema.

## 14_HYPOTHESIS

Future implementation may report secondary errors, but each fixture declares one primary expected error code.

## 15_REMAINING_GAP

No runnable class tests exist.

## 16_TODO

- Add class fixtures to the expected verdict index.

## 17_RESUME_POINT

Resume point:

```text
Validate class enum and class invariants before binding checks.
```

## 18_TO_DOCUMENT

Future validator reports must show capability id and class field path.

## 19_TO_REMEMBER

Capability class is a security boundary.

## RISKS

- À qualifier.
