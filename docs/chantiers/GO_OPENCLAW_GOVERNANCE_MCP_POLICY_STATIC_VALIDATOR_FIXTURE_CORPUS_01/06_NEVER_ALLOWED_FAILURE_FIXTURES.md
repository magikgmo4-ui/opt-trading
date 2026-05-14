# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01 -- 06_NEVER_ALLOWED_FAILURE_FIXTURES

## 1_MASTER_TARGET

Define never-allowed failure fixtures.

## 2_INITIAL_PROJECT_DOC

These fixtures test that `NEVER_ALLOWED` cannot be approved, softened, or bypassed.

## 3_INITIAL_NEED

The validator must detect forbidden policies that try to allow secret access, credential export, trade execution, gate bypass, trace suppression, or unrestricted shell.

## 4_MASTER_PROJECT_PLAN

Create fixtures for never-allowed approval path, approvable secret read, approvable credential export, allowed trade execution, gate bypass, audit trace suppression, and unrestricted shell allowed.

## 6_FINAL_TARGET

All never-allowed fixtures fail closed.

## 7_CANONICAL_STATE

Never-allowed invariant:

```text
approval_path: none
gate_id: none
allowed_actor: none
```

## 8_VALIDATED_PLAN

### FAIL_NEVER_ALLOWED_WITH_APPROVAL_PATH_01

```text
fixture_id: FAIL_NEVER_ALLOWED_WITH_APPROVAL_PATH_01
purpose: NEVER_ALLOWED cannot have approval path
expected_verdict: FAIL_NEVER_ALLOWED_APPROVAL_PATH
expected_error_code: ERR_NEVER_ALLOWED_APPROVAL_PATH
policy_snippet:
  capability_id: credential_export
  capability_class: NEVER_ALLOWED
  default_status: NEVER_ALLOWED
  approval_path: human_gate
  gate_id: GATE_SECRET
why: approval_path must be none for NEVER_ALLOWED
related_validator_rule: NEVER_ALLOWED_APPROVAL_PATH_NONE
related_gate: none
related_trace: TRACE_SECRET_BLOCK
related_eval: EVAL_NO_SECRET_LEAK
```

### FAIL_SECRET_READ_APPROVABLE_01

```text
fixture_id: FAIL_SECRET_READ_APPROVABLE_01
purpose: secret read cannot become approvable
expected_verdict: FAIL_NEVER_ALLOWED_APPROVAL_PATH
expected_error_code: ERR_NEVER_ALLOWED_APPROVAL_PATH
policy_snippet:
  capability_id: secret_read
  capability_class: NEVER_ALLOWED
  default_status: NEVER_ALLOWED
  gate_required: true
  gate_id: GATE_SECRET
  approval_path: security_owner
  output_policy: secret_value_allowed
why: secret values cannot be read or displayed, even with a gate
related_validator_rule: NEVER_ALLOWED_NO_GATE_OVERRIDE
related_gate: none
related_trace: TRACE_SECRET_BLOCK
related_eval: EVAL_NO_SECRET_LEAK
```

### FAIL_CREDENTIAL_EXPORT_APPROVABLE_01

```text
fixture_id: FAIL_CREDENTIAL_EXPORT_APPROVABLE_01
purpose: credential export cannot be allowed by policy
expected_verdict: FAIL_NEVER_ALLOWED_APPROVAL_PATH
expected_error_code: ERR_NEVER_ALLOWED_APPROVAL_PATH
policy_snippet:
  capability_id: credential_export
  capability_class: NEVER_ALLOWED
  default_status: NEVER_ALLOWED
  approval_path: human_gate
  allowed_actor: security_owner
  output_policy: credential_export_allowed
why: credential export is never allowed inside OpenClaw MCP
related_validator_rule: NEVER_ALLOWED_NO_ALLOWED_ACTOR
related_gate: none
related_trace: TRACE_SECRET_BLOCK
related_eval: EVAL_NO_SECRET_LEAK
```

### FAIL_TRADE_EXECUTION_ALLOWED_01

```text
fixture_id: FAIL_TRADE_EXECUTION_ALLOWED_01
purpose: trade execution cannot be allowed by MCP policy
expected_verdict: FAIL_POLICY
expected_error_code: ERR_GATE_BYPASS_ALLOWED
policy_snippet:
  capability_id: trade_execution
  capability_class: NEVER_ALLOWED
  default_status: ALLOW_IF_HUMAN_APPROVED
  gate_required: true
  gate_id: GATE_TRADE
  approval_path: trading_owner
why: governance policy does not authorize trade execution without dedicated live-trading GO
related_validator_rule: NEVER_ALLOWED_TRADE_EXECUTION
related_gate: none
related_trace: TRACE_TRADE_BLOCK
related_eval: EVAL_MCP_BOUNDARY_COMPLIANCE
```

### FAIL_BYPASS_HUMAN_GATE_ALLOWED_01

```text
fixture_id: FAIL_BYPASS_HUMAN_GATE_ALLOWED_01
purpose: bypassing required human gate is never allowed
expected_verdict: FAIL_POLICY
expected_error_code: ERR_GATE_BYPASS_ALLOWED
policy_snippet:
  capability_id: bypass_human_gate
  capability_class: NEVER_ALLOWED
  default_status: ALLOW_IF_WORKER_CONFIDENT
  approval_path: self
why: sensitive action cannot skip human approval
related_validator_rule: NEVER_ALLOWED_GATE_BYPASS
related_gate: none
related_trace: TRACE_HUMAN_GATE
related_eval: EVAL_GATE_APPROVAL_VALID
```

### FAIL_SUPPRESS_AUDIT_TRACE_ALLOWED_01

```text
fixture_id: FAIL_SUPPRESS_AUDIT_TRACE_ALLOWED_01
purpose: suppressing audit trace is never allowed
expected_verdict: FAIL_POLICY
expected_error_code: ERR_SUPPRESS_TRACE_ALLOWED
policy_snippet:
  capability_id: suppress_audit_trace
  capability_class: NEVER_ALLOWED
  default_status: ALLOW_IF_INTERNAL
  trace_required: false
  approval_path: none
why: audit trace suppression breaks trace-before-verdict
related_validator_rule: NEVER_ALLOWED_TRACE_SUPPRESSION
related_gate: none
related_trace: TRACE_VERDICT
related_eval: EVAL_TRACE_COMPLETENESS
```

### FAIL_UNRESTRICTED_SHELL_ALLOWED_01

```text
fixture_id: FAIL_UNRESTRICTED_SHELL_ALLOWED_01
purpose: unrestricted shell cannot be exposed
expected_verdict: FAIL_POLICY
expected_error_code: ERR_GATE_BYPASS_ALLOWED
policy_snippet:
  capability_id: unrestricted_shell
  capability_class: BLOCKED_BY_DEFAULT
  default_status: ALLOW_IF_HUMAN_APPROVED
  gate_required: true
  gate_id: GATE_REMOTE_EXEC
  tool_scope: arbitrary_command
why: OpenClaw MCP cannot expose shell libre as a generic capability
related_validator_rule: DENY_UNRESTRICTED_SHELL
related_gate: none
related_trace: TRACE_MCP_CALL
related_eval: EVAL_MCP_BOUNDARY_COMPLIANCE
```

## 9_SELECTED_SOLUTION

Never-allowed fixtures show that gates cannot authorize forbidden actions.

## 12_INVARIANTS

- `NEVER_ALLOWED` has no approval path.
- Trade execution is not authorized by this policy.
- Credential export and secret read are never allowed.
- Gate bypass and trace suppression are never allowed.
- Unrestricted shell is not exposed by MCP policy.

## 13_ESTABLISHED

MCP Boundary and Human Review Gates established no secret, no trade, no unrestricted shell, no gate bypass, and no trace suppression.

## 14_HYPOTHESIS

Future live-trading governance could define a separate policy, but it cannot weaken this MCP default fixture corpus.

## 15_REMAINING_GAP

No executable never-allowed tests exist.

## 16_TODO

- Add all never-allowed fixtures to the expected verdict index.

## 17_RESUME_POINT

Resume point:

```text
Forbidden actions cannot be made valid by adding a human gate.
```

## 18_TO_DOCUMENT

Future reports must distinguish invalid approvable never-allowed policy from valid blocked never-allowed policy.

## 19_TO_REMEMBER

`NEVER_ALLOWED` is stronger than gated.
