# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01 -- 05_GATE_TRACE_EVAL_FAILURE_FIXTURES

## 1_MASTER_TARGET

Define gate, trace, and eval binding failure fixtures.

## 2_INITIAL_PROJECT_DOC

These fixtures test the class -> gate -> trace -> eval chain.

## 3_INITIAL_NEED

The validator must fail closed when a gated capability lacks a gate, trace, final verdict trace, MCP trace, eval, or rollback evidence.

## 4_MASTER_PROJECT_PLAN

Create fixtures for missing gate id, missing gate trace, missing MCP call trace, missing final verdict trace, and missing eval binding.

## 6_FINAL_TARGET

Every binding failure has a deterministic verdict and primary error code.

## 7_CANONICAL_STATE

Canonical binding principle:

```text
Gate before sensitive action.
Trace before verdict.
Eval before promotion.
```

## 8_VALIDATED_PLAN

### FAIL_WRITE_GATED_WITHOUT_GATE_ID_01

```text
fixture_id: FAIL_WRITE_GATED_WITHOUT_GATE_ID_01
purpose: WRITE_GATED capability must reference valid gate id
expected_verdict: FAIL_GATE_BINDING
expected_error_code: ERR_WRITE_WITHOUT_GATE
policy_snippet:
  capability_id: create_doc_file
  capability_class: WRITE_GATED
  default_status: NEEDS_GATE
  gate_required: true
  gate_id: missing
  trace_required: true
  trace_family: TRACE_CODEX_PATCH
  eval_required: true
  eval_profile: EVAL_GATE_REQUIRED
why: gated write cannot proceed without a valid gate id
related_validator_rule: BIND_GATE_EXISTS
related_gate: GATE_DOC_WRITE
related_trace: TRACE_CODEX_PATCH
related_eval: EVAL_GATE_REQUIRED
```

### FAIL_GATE_WITHOUT_TRACE_01

```text
fixture_id: FAIL_GATE_WITHOUT_TRACE_01
purpose: human gate must produce TRACE_HUMAN_GATE
expected_verdict: FAIL_TRACE_BINDING
expected_error_code: ERR_TRACE_REQUIRED_MISSING
policy_snippet:
  capability_id: git_push
  capability_class: HUMAN_APPROVAL_REQUIRED
  gate_required: true
  gate_id: GATE_GIT_PUSH
  trace_required: false
  eval_required: true
  eval_profile: EVAL_GATE_APPROVAL_VALID
why: every human gate requires explicit trace coverage
related_validator_rule: BIND_HUMAN_GATE_TRACE
related_gate: GATE_GIT_PUSH
related_trace: TRACE_HUMAN_GATE
related_eval: EVAL_GATE_APPROVAL_VALID
```

### FAIL_MCP_CALL_WITHOUT_TRACE_MCP_CALL_01

```text
fixture_id: FAIL_MCP_CALL_WITHOUT_TRACE_MCP_CALL_01
purpose: MCP call must include TRACE_MCP_CALL
expected_verdict: FAIL_TRACE_BINDING
expected_error_code: ERR_TRACE_REQUIRED_MISSING
policy_snippet:
  capability_id: repo_state
  capability_class: READ_ONLY
  trace_required: true
  trace_family: TRACE_TOOL_CALL_ONLY
  eval_required: true
  eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
why: MCP capability needs TRACE_MCP_CALL or approved equivalent
related_validator_rule: BIND_MCP_CALL_TRACE
related_gate: none
related_trace: TRACE_MCP_CALL
related_eval: EVAL_MCP_BOUNDARY_COMPLIANCE
```

### FAIL_FINAL_VERDICT_WITHOUT_TRACE_VERDICT_01

```text
fixture_id: FAIL_FINAL_VERDICT_WITHOUT_TRACE_VERDICT_01
purpose: final verdict must have TRACE_VERDICT
expected_verdict: FAIL_TRACE_BINDING
expected_error_code: ERR_TRACE_REQUIRED_MISSING
policy_snippet:
  final_verdict_policy:
    verdicts: [PASS_POLICY_STATIC_VALIDATION, FAIL_POLICY]
    trace_required: true
    trace_family: TRACE_MCP_CALL
    final_trace_family: none
why: every final validator verdict must be represented by TRACE_VERDICT
related_validator_rule: BIND_FINAL_VERDICT_TRACE
related_gate: none
related_trace: TRACE_VERDICT
related_eval: EVAL_FINAL_VERDICT_VALIDITY
```

### FAIL_CAPABILITY_WITHOUT_EVAL_01

```text
fixture_id: FAIL_CAPABILITY_WITHOUT_EVAL_01
purpose: every capability must declare eval coverage
expected_verdict: FAIL_EVAL_BINDING
expected_error_code: ERR_EVAL_REQUIRED_MISSING
policy_snippet:
  capability_id: repo_state
  capability_class: READ_ONLY
  trace_required: true
  trace_family: TRACE_MCP_CALL
  eval_required: false
  eval_profile: none
why: eval coverage is mandatory before policy promotion
related_validator_rule: BIND_EVAL_REQUIRED
related_gate: none
related_trace: TRACE_MCP_CALL
related_eval: EVAL_TRACE_COMPLETENESS
```

## 9_SELECTED_SOLUTION

Binding fixtures make missing dependencies explicit instead of relying on later semantic failures.

## 12_INVARIANTS

- Gated actions require valid gate ids.
- Human gates require `TRACE_HUMAN_GATE`.
- MCP calls require MCP call trace.
- Final verdict requires `TRACE_VERDICT`.
- Every capability requires eval coverage.

## 13_ESTABLISHED

Trace / Evals Profile established trace before verdict and eval before promotion.

## 14_HYPOTHESIS

Future validator may report both trace and eval failures, but each fixture records one primary expected error.

## 15_REMAINING_GAP

No executable binding tests exist.

## 16_TODO

- Add these binding fixtures to the index table.

## 17_RESUME_POINT

Resume point:

```text
Binding failures close the chain before any policy promotion.
```

## 18_TO_DOCUMENT

Future reports must identify both the missing binding and the capability that requires it.

## 19_TO_REMEMBER

A policy without traces or evals cannot be trusted even if the capability class is valid.
