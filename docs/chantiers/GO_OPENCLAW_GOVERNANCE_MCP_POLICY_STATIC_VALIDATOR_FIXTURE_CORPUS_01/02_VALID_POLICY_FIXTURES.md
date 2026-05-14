# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01 -- 02_VALID_POLICY_FIXTURES

## 1_MASTER_TARGET

Define valid conceptual policy fixtures for the future static validator.

## 2_INITIAL_PROJECT_DOC

These fixtures are Markdown documentation only. Snippets are not active policy files.

## 3_INITIAL_NEED

The future validator needs positive examples proving expected pass behavior.

## 4_MASTER_PROJECT_PLAN

Valid fixtures cover:

- minimal policy;
- read-only capability;
- read-sanitized logs;
- write-gated doc write;
- runtime-gated Ollama health check;
- never-allowed secret read blocked correctly.

## 6_FINAL_TARGET

Every valid fixture expects `PASS_POLICY_STATIC_VALIDATION` and `expected_error_code: none`.

## 7_CANONICAL_STATE

All valid snippets keep:

```text
runtime_binding: false
secret_policy: no_secret_allowed
default_status: BLOCKED_BY_DEFAULT
```

## 8_VALIDATED_PLAN

### VALID_MINIMAL_POLICY_01

```text
fixture_id: VALID_MINIMAL_POLICY_01
purpose: prove required top-level sections exist
expected_verdict: PASS_POLICY_STATIC_VALIDATION
expected_error_code: none
policy_snippet:
  policy:
    id: OPENCLAW_MCP_POLICY_DRAFT_01
    policy_version: 0.1-doc-only
    status: draft_doc_only
    default_status: BLOCKED_BY_DEFAULT
    runtime_binding: false
    secret_policy: no_secret_allowed
  capability_classes: present
  capabilities: present
  gates: present
  traces: present
  evals: present
  strict_worker_roles: present
  ollama_lab_policy: present
  governor_decision_rules: present
  never_allowed: present
  blocked_by_default: present
why: all required structural sections are present and runtime binding is false
related_validator_rule: SCHEMA_REQUIRED_TOP_LEVEL
related_gate: none
related_trace: TRACE_VERDICT
related_eval: EVAL_TRACE_COMPLETENESS
```

### VALID_READ_ONLY_REPO_STATE_01

```text
fixture_id: VALID_READ_ONLY_REPO_STATE_01
purpose: prove bounded read-only capability can pass static validation
expected_verdict: PASS_POLICY_STATIC_VALIDATION
expected_error_code: none
policy_snippet:
  capability_id: repo_state
  capability_class: READ_ONLY
  default_status: ALLOW_IF_BOUNDED
  gate_required: false
  gate_id: none
  trace_required: true
  trace_family: TRACE_MCP_CALL
  eval_required: true
  eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
  input_policy: bounded_repo_path
  output_policy: summary_only
  secret_policy: no_secret_allowed
why: read-only repo state has no mutation, no secret, no trade, trace, and eval
related_validator_rule: CLASS_READ_ONLY_BOUNDED
related_gate: none
related_trace: TRACE_MCP_CALL
related_eval: EVAL_MCP_BOUNDARY_COMPLIANCE
```

### VALID_READ_SANITIZED_LOGS_01

```text
fixture_id: VALID_READ_SANITIZED_LOGS_01
purpose: prove sanitized log fixture has explicit sanitized output
expected_verdict: PASS_POLICY_STATIC_VALIDATION
expected_error_code: none
policy_snippet:
  capability_id: logs_tail_sanitized
  capability_class: READ_SANITIZED
  default_status: ALLOW_IF_SANITIZED
  gate_required: false
  gate_id: none
  trace_required: true
  trace_family: TRACE_RUNTIME_READ
  eval_required: true
  eval_profile: EVAL_NO_SECRET_LEAK
  input_policy: named_log_source_and_redaction_rule
  output_policy: sanitized_excerpt_only
  secret_policy: redact_values_and_raw_env
why: output policy is sanitized and secret values are not allowed
related_validator_rule: CLASS_READ_SANITIZED_OUTPUT
related_gate: none
related_trace: TRACE_RUNTIME_READ
related_eval: EVAL_NO_SECRET_LEAK
```

### VALID_WRITE_GATED_DOC_FILE_01

```text
fixture_id: VALID_WRITE_GATED_DOC_FILE_01
purpose: prove doc write is valid only when gated and rollback-ready
expected_verdict: PASS_POLICY_STATIC_VALIDATION
expected_error_code: none
policy_snippet:
  capability_id: create_doc_file
  capability_class: WRITE_GATED
  default_status: NEEDS_GATE
  gate_required: true
  gate_id: GATE_DOC_WRITE
  trace_required: true
  trace_family: TRACE_CODEX_PATCH
  eval_required: true
  eval_profile: EVAL_ROLLBACK_READY
  rollback_required: true
  rollback_policy: delete_created_file_or_revert_patch
  secret_policy: no_secret_allowed
why: gated write includes gate, trace, eval, and rollback rule
related_validator_rule: BIND_GATE_EXISTS
related_gate: GATE_DOC_WRITE
related_trace: TRACE_CODEX_PATCH
related_eval: EVAL_ROLLBACK_READY
```

### VALID_RUNTIME_GATED_OLLAMA_HEALTH_01

```text
fixture_id: VALID_RUNTIME_GATED_OLLAMA_HEALTH_01
purpose: prove Ollama health check is valid when runtime-gated and sanitized
expected_verdict: PASS_POLICY_STATIC_VALIDATION
expected_error_code: none
policy_snippet:
  capability_id: ollama_health_check
  capability_class: RUNTIME_GATED
  default_status: NEEDS_GATE
  gate_required: true
  gate_id: GATE_RUNTIME
  trace_required: true
  trace_family: TRACE_RUNTIME_READ
  eval_required: true
  eval_profile: EVAL_NO_RUNTIME_TOUCH
  output_policy: sanitized_health_report
  rollback_required: true
  rollback_policy: stop_or_restore_if_runtime_effect_detected
  trade_policy: no_trade
  secret_policy: no_secret_allowed
why: runtime surface has gate, trace, eval, rollback, no-trade, and sanitized output
related_validator_rule: OLLAMA_RUNTIME_GATED_BOUNDARY
related_gate: GATE_RUNTIME
related_trace: TRACE_RUNTIME_READ
related_eval: EVAL_NO_RUNTIME_TOUCH
```

### VALID_NEVER_ALLOWED_SECRET_READ_BLOCKED_01

```text
fixture_id: VALID_NEVER_ALLOWED_SECRET_READ_BLOCKED_01
purpose: prove a never-allowed secret read is valid only as blocked policy
expected_verdict: PASS_POLICY_STATIC_VALIDATION
expected_error_code: none
policy_snippet:
  capability_id: secret_read
  capability_class: NEVER_ALLOWED
  default_status: NEVER_ALLOWED
  gate_required: false
  gate_id: none
  approval_path: none
  trace_required: true
  trace_family: TRACE_SECRET_BLOCK
  eval_required: true
  eval_profile: EVAL_NO_SECRET_LEAK
  output_policy: blocked_reason_only
  secret_policy: values_never_read_or_displayed
why: never-allowed has no approval path and emits secret block trace
related_validator_rule: NEVER_ALLOWED_APPROVAL_PATH_NONE
related_gate: none
related_trace: TRACE_SECRET_BLOCK
related_eval: EVAL_NO_SECRET_LEAK
```

## 9_SELECTED_SOLUTION

Use positive fixtures to prove that passing validation still does not authorize runtime use. `PASS_POLICY_STATIC_VALIDATION` only means the policy document is statically coherent.

## 12_INVARIANTS

- Valid fixtures are still documentation only.
- Valid fixtures do not activate policy.
- Valid fixtures do not create runtime authority.
- Valid fixtures include gate, trace, and eval coherence.

## 13_ESTABLISHED

These fixtures cover the positive paths requested for minimal policy, read-only, read-sanitized, write-gated, runtime-gated, and never-allowed blocked policy.

## 14_HYPOTHESIS

Future validator tests may split these snippets into independent fixture files, but this GO keeps them in Markdown.

## 15_REMAINING_GAP

No executable pass tests exist yet.

## 16_TODO

- Add all fixtures to the index table.
- Preserve `expected_error_code: none` for valid fixtures.

## 17_RESUME_POINT

Resume point:

```text
Valid fixtures establish coherent policy examples, not operational permission.
```

## 18_TO_DOCUMENT

Future harness must verify that all valid fixtures still keep `runtime_binding: false`.

## 19_TO_REMEMBER

Passing static validation is not a human gate approval.
