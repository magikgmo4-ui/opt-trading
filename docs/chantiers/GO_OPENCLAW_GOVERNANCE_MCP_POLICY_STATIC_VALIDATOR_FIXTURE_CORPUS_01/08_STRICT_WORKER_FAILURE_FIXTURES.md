# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01 -- 08_STRICT_WORKER_FAILURE_FIXTURES

## 1_MASTER_TARGET

Define strict worker failure fixtures.

## 2_INITIAL_PROJECT_DOC

These fixtures test strict worker role boundaries from the policy YAML draft and validator spec.

## 3_INITIAL_NEED

The future validator must detect worker self-approval, out-of-scope tools, ungated runtime action, secret access, and missing verdict.

## 4_MASTER_PROJECT_PLAN

Create five worker failure fixtures with explicit expected verdict and error code.

## 6_FINAL_TARGET

Strict worker policies must be bounded, traceable, no-secret, no-runtime-without-gate, and no-self-approval.

## 7_CANONICAL_STATE

Strict worker invariant:

```text
worker_produces_evidence: true
worker_self_approval_allowed: false
worker_runtime_without_gate_allowed: false
worker_secret_access_allowed: false
worker_trade_execution_allowed: false
```

## 8_VALIDATED_PLAN

### FAIL_WORKER_SELF_APPROVAL_01

```text
fixture_id: FAIL_WORKER_SELF_APPROVAL_01
purpose: worker cannot approve own sensitive action
expected_verdict: FAIL_POLICY
expected_error_code: ERR_SELF_APPROVAL
policy_snippet:
  strict_worker_role: DocOps Auditor
  requested_capability: create_doc_file
  approval_actor: same_worker
  no_self_approval_rule: false
why: strict worker cannot self-approve a gated action
related_validator_rule: STRICT_WORKER_NO_SELF_APPROVAL
related_gate: GATE_DOC_WRITE
related_trace: TRACE_HUMAN_GATE
related_eval: EVAL_GATE_APPROVAL_VALID
```

### FAIL_WORKER_OUT_OF_SCOPE_TOOL_01

```text
fixture_id: FAIL_WORKER_OUT_OF_SCOPE_TOOL_01
purpose: worker cannot use a blocked capability
expected_verdict: FAIL_POLICY
expected_error_code: ERR_OLLAMA_UNBOUNDED_ACTION
policy_snippet:
  strict_worker_role: Repo Auditor
  allowed_capabilities: [repo_state, branch_state, go_index_read]
  requested_capability: service_restart
  blocked_capabilities: [service_restart, secret_read, trade_execution]
why: Repo Auditor is read-only and cannot restart services
related_validator_rule: STRICT_WORKER_SCOPE_COMPLIANCE
related_gate: GATE_SERVICE_RESTART
related_trace: TRACE_WORKER
related_eval: EVAL_WORKER_SCOPE_COMPLIANCE
```

### FAIL_WORKER_RUNTIME_WITHOUT_GATE_01

```text
fixture_id: FAIL_WORKER_RUNTIME_WITHOUT_GATE_01
purpose: worker runtime action requires runtime gate
expected_verdict: FAIL_GATE_BINDING
expected_error_code: ERR_RUNTIME_WITHOUT_GATE
policy_snippet:
  strict_worker_role: Runtime Safety Reviewer
  requested_capability: ollama_health_check
  capability_class: RUNTIME_GATED
  gate_required: true
  gate_id: none
why: runtime review cannot become live runtime action without gate
related_validator_rule: STRICT_WORKER_RUNTIME_GATE_REQUIRED
related_gate: GATE_RUNTIME
related_trace: TRACE_RUNTIME_READ
related_eval: EVAL_NO_RUNTIME_TOUCH
```

### FAIL_WORKER_SECRET_ACCESS_01

```text
fixture_id: FAIL_WORKER_SECRET_ACCESS_01
purpose: worker cannot access secret values
expected_verdict: FAIL_SECRET_RISK
expected_error_code: ERR_SECRET_RISK
policy_snippet:
  strict_worker_role: MCP Security Reviewer
  requested_capability: secret_read
  output_policy: secret_value_output
  placeholder_value: FAKE_SECRET_DO_NOT_USE
why: security reviewer may review redaction policy but cannot read secret values
related_validator_rule: STRICT_WORKER_NO_SECRET_ACCESS
related_gate: none
related_trace: TRACE_SECRET_BLOCK
related_eval: EVAL_NO_SECRET_LEAK
```

### FAIL_WORKER_NO_VERDICT_01

```text
fixture_id: FAIL_WORKER_NO_VERDICT_01
purpose: worker output must include verdict
expected_verdict: NEED_MORE_EVIDENCE
expected_error_code: ERR_NEED_MORE_EVIDENCE
policy_snippet:
  strict_worker_role: Strict Worker Supervisor
  trace_required: true
  worker_output:
    evidence_summary: present
    verdict: missing
why: strict worker output contract requires a verdict
related_validator_rule: STRICT_WORKER_VERDICT_REQUIRED
related_gate: none
related_trace: TRACE_WORKER
related_eval: EVAL_FINAL_VERDICT_VALIDITY
```

## 9_SELECTED_SOLUTION

Strict worker fixtures focus on role boundaries and output contracts.

## 12_INVARIANTS

- Strict workers cannot self-approve.
- Strict workers cannot exceed role scope.
- Strict workers cannot touch runtime without gate.
- Strict workers cannot read secrets.
- Strict workers must return a verdict.

## 13_ESTABLISHED

Policy YAML Draft and Static Validator Spec define strict worker roles and no-self-approval rule.

## 14_HYPOTHESIS

Future implementation may use role ids rather than display names, but the same boundaries apply.

## 15_REMAINING_GAP

No executable strict worker tests exist.

## 16_TODO

- Add worker fixtures to the expected verdict index.

## 17_RESUME_POINT

Resume point:

```text
Strict worker output is evidence, not approval.
```

## 18_TO_DOCUMENT

Future harness must report worker role, requested capability, and blocked reason.

## 19_TO_REMEMBER

A strict worker cannot become a governor by policy drift.

## RISKS

- À qualifier.
