# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01 -- 03_SCHEMA_FAILURE_FIXTURES

## 1_MASTER_TARGET

Define schema failure fixtures for the future static validator.

## 2_INITIAL_PROJECT_DOC

These fixtures exercise required field and top-level section validation.

## 3_INITIAL_NEED

The validator must fail closed when policy structure is incomplete or runtime-bound.

## 4_MASTER_PROJECT_PLAN

Create schema fixtures for missing policy id, missing default status, runtime binding true, missing capability classes, and missing governor rules.

## 6_FINAL_TARGET

Each schema failure fixture declares a deterministic failure verdict and one primary error code.

## 7_CANONICAL_STATE

The canonical schema requires:

```text
policy.id
policy.version or policy.policy_version
policy.status
policy.default_status
policy.runtime_binding
policy.secret_policy
capability_classes
capabilities
gates
traces
evals
strict_worker_roles
ollama_lab_policy
governor_decision_rules
never_allowed
blocked_by_default
```

## 8_VALIDATED_PLAN

### FAIL_MISSING_POLICY_ID_01

```text
fixture_id: FAIL_MISSING_POLICY_ID_01
purpose: missing policy id must fail schema validation
expected_verdict: FAIL_SCHEMA_MISSING_FIELD
expected_error_code: ERR_SCHEMA_MISSING_FIELD
policy_snippet:
  policy:
    policy_version: 0.1-doc-only
    status: draft_doc_only
    default_status: BLOCKED_BY_DEFAULT
    runtime_binding: false
    secret_policy: no_secret_allowed
why: policy.id is required and cannot be inferred
related_validator_rule: SCHEMA_POLICY_ID
related_gate: none
related_trace: TRACE_VERDICT
related_eval: EVAL_TRACE_COMPLETENESS
```

### FAIL_MISSING_DEFAULT_STATUS_01

```text
fixture_id: FAIL_MISSING_DEFAULT_STATUS_01
purpose: missing policy default must fail closed
expected_verdict: FAIL_SCHEMA_MISSING_FIELD
expected_error_code: ERR_SCHEMA_MISSING_FIELD
policy_snippet:
  policy:
    id: OPENCLAW_MCP_POLICY_DRAFT_01
    policy_version: 0.1-doc-only
    status: draft_doc_only
    runtime_binding: false
    secret_policy: no_secret_allowed
why: default_status is mandatory and must not be inferred
related_validator_rule: SCHEMA_DEFAULT_BLOCKED
related_gate: none
related_trace: TRACE_VERDICT
related_eval: EVAL_MCP_BOUNDARY_COMPLIANCE
```

### FAIL_RUNTIME_BINDING_TRUE_01

```text
fixture_id: FAIL_RUNTIME_BINDING_TRUE_01
purpose: runtime-bound draft must be rejected
expected_verdict: FAIL_RUNTIME_BINDING_ENABLED
expected_error_code: ERR_RUNTIME_BINDING_ENABLED
policy_snippet:
  policy:
    id: OPENCLAW_MCP_POLICY_DRAFT_01
    policy_version: 0.1-doc-only
    status: draft_doc_only
    default_status: BLOCKED_BY_DEFAULT
    runtime_binding: true
    secret_policy: no_secret_allowed
why: policy drafts in this chain are documentation only and cannot bind runtime
related_validator_rule: SCHEMA_RUNTIME_FALSE
related_gate: GATE_RUNTIME
related_trace: TRACE_VERDICT
related_eval: EVAL_NO_RUNTIME_TOUCH
```

### FAIL_MISSING_CAPABILITY_CLASSES_01

```text
fixture_id: FAIL_MISSING_CAPABILITY_CLASSES_01
purpose: missing class section must fail schema validation
expected_verdict: FAIL_SCHEMA_MISSING_FIELD
expected_error_code: ERR_SCHEMA_MISSING_FIELD
policy_snippet:
  policy:
    id: OPENCLAW_MCP_POLICY_DRAFT_01
    policy_version: 0.1-doc-only
    status: draft_doc_only
    default_status: BLOCKED_BY_DEFAULT
    runtime_binding: false
    secret_policy: no_secret_allowed
  capabilities: present
  gates: present
  traces: present
  evals: present
why: class validation cannot run without capability_classes
related_validator_rule: SCHEMA_REQUIRED_TOP_LEVEL
related_gate: none
related_trace: TRACE_VERDICT
related_eval: EVAL_MCP_BOUNDARY_COMPLIANCE
```

### FAIL_MISSING_GOVERNOR_RULES_01

```text
fixture_id: FAIL_MISSING_GOVERNOR_RULES_01
purpose: missing governor decision rules must fail schema validation
expected_verdict: FAIL_SCHEMA_MISSING_FIELD
expected_error_code: ERR_SCHEMA_MISSING_FIELD
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
why: governor decision rules are required for fail-closed decisions
related_validator_rule: SCHEMA_REQUIRED_TOP_LEVEL
related_gate: none
related_trace: TRACE_VERDICT
related_eval: EVAL_FINAL_VERDICT_VALIDITY
```

## 9_SELECTED_SOLUTION

Schema failures use the most specific static validator verdict available. Missing required fields use `FAIL_SCHEMA_MISSING_FIELD`.

## 12_INVARIANTS

- Missing schema data blocks validation.
- Runtime binding true blocks validation.
- Defaults are never inferred.

## 13_ESTABLISHED

The static validator spec established required fields and `runtime_binding: false`.

## 14_HYPOTHESIS

Future parser behavior may add duplicate-key validation, but these fixtures cover required-field absence.

## 15_REMAINING_GAP

No executable schema tests exist.

## 16_TODO

- Add schema fixtures to the global fixture index.

## 17_RESUME_POINT

Resume point:

```text
Schema checks run before semantic class and binding checks.
```

## 18_TO_DOCUMENT

Future harness must preserve one primary error code per fixture.

## 19_TO_REMEMBER

Schema ambiguity is a policy failure, not a warning.
