# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 09_CONCEPTUAL_FIXTURES

## 1_MASTER_TARGET

Define conceptual, non-executable fixtures for the future static validator.

## 2_INITIAL_PROJECT_DOC

These fixtures are documentation examples only. They are not YAML files, JSON files, scripts, tests, or runtime inputs.

## 3_INITIAL_NEED

The future implementation needs examples of expected pass and fail outcomes without creating a real fixture corpus in this GO.

## 4_MASTER_PROJECT_PLAN

Each conceptual fixture states:

- fixture id;
- intent;
- minimal non-secret shape;
- expected verdict;
- expected error code.

## 6_FINAL_TARGET

The final target is a doc-only fixture specification covering valid and invalid policy cases.

## 7_CANONICAL_STATE

All fixtures are in fenced `text` blocks and are not executable.

## 8_VALIDATED_PLAN

Fixture index:

| Fixture | Expected verdict |
|---|---|
| Valid minimal policy | `PASS_POLICY_STATIC_VALIDATION` |
| Missing required field | `FAIL_SCHEMA_MISSING_FIELD` |
| Unknown capability class | `FAIL_UNKNOWN_CLASS` |
| `WRITE_GATED` without gate | `FAIL_GATE_BINDING` |
| `NEVER_ALLOWED` with approval path | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` |
| Secret-like field detected | `FAIL_SECRET_RISK` |
| `runtime_binding` true | `FAIL_RUNTIME_BINDING_ENABLED` |
| Unknown capability request | `BLOCKED_WITH_REASON` with `BLOCKED_BY_DEFAULT` decision |
| Missing trace binding | `FAIL_TRACE_BINDING` |
| Missing eval binding | `FAIL_EVAL_BINDING` |

## 9_SELECTED_SOLUTION

### Fixture: valid minimal policy

```text
fixture_id: valid_minimal_policy
policy:
  id: OPENCLAW_MCP_POLICY_DRAFT_01
  policy_version: 0.1-doc-only
  status: draft_doc_only
  default_status: BLOCKED_BY_DEFAULT
  runtime_binding: false
  secret_policy: no_secret_allowed
sections:
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
expected_verdict: PASS_POLICY_STATIC_VALIDATION
```

### Fixture: missing required field

```text
fixture_id: missing_policy_default_status
policy:
  id: OPENCLAW_MCP_POLICY_DRAFT_01
  policy_version: 0.1-doc-only
  status: draft_doc_only
  runtime_binding: false
  secret_policy: no_secret_allowed
missing:
  policy.default_status
expected_error: ERR_SCHEMA_MISSING_FIELD
expected_verdict: FAIL_SCHEMA_MISSING_FIELD
```

### Fixture: unknown capability class

```text
fixture_id: unknown_capability_class
capability:
  capability_id: repo_state
  capability_class: UNSAFE_UNKNOWN_CLASS
expected_error: ERR_UNKNOWN_CLASS
expected_verdict: FAIL_UNKNOWN_CLASS
```

### Fixture: WRITE_GATED without gate

```text
fixture_id: write_gated_without_gate
capability:
  capability_id: create_doc_file
  capability_class: WRITE_GATED
  gate_required: true
  gate_id: none
expected_error: ERR_WRITE_WITHOUT_GATE
expected_verdict: FAIL_GATE_BINDING
```

### Fixture: NEVER_ALLOWED with approval path

```text
fixture_id: never_allowed_with_approval_path
capability:
  capability_id: credential_export
  capability_class: NEVER_ALLOWED
  approval_path: human_gate
expected_error: ERR_NEVER_ALLOWED_APPROVAL_PATH
expected_verdict: FAIL_NEVER_ALLOWED_APPROVAL_PATH
final_policy_verdict: FAIL_POLICY
```

### Fixture: secret-like field detected

```text
fixture_id: forbidden_secret_field_name
capability:
  capability_id: invalid_secret_display
  capability_class: NEVER_ALLOWED
  forbidden_field_name_present: credential_blob
expected_error: ERR_SECRET_RISK
expected_verdict: FAIL_SECRET_RISK
note: field name only; no secret value is present in this fixture
```

### Fixture: runtime_binding true

```text
fixture_id: runtime_binding_true
policy:
  runtime_binding: true
expected_error: ERR_RUNTIME_BINDING_ENABLED
expected_verdict: FAIL_RUNTIME_BINDING_ENABLED
```

### Fixture: unknown capability request

```text
fixture_id: unknown_capability_request
request:
  capability_id: capability_not_declared
policy:
  default_status: BLOCKED_BY_DEFAULT
expected_error: ERR_UNKNOWN_CAPABILITY
expected_decision: BLOCKED_BY_DEFAULT
expected_verdict: BLOCKED_WITH_REASON
```

### Fixture: missing trace binding

```text
fixture_id: missing_trace_binding
capability:
  capability_id: ollama_health_check
  capability_class: RUNTIME_GATED
  trace_required: true
  trace_family: TRACE_NOT_DECLARED
expected_error: ERR_TRACE_FAMILY_UNKNOWN
expected_verdict: FAIL_TRACE_BINDING
```

### Fixture: missing eval binding

```text
fixture_id: missing_eval_binding
capability:
  capability_id: repo_state
  capability_class: READ_ONLY
  eval_required: true
  eval_profile: EVAL_NOT_DECLARED
expected_error: ERR_EVAL_PROFILE_UNKNOWN
expected_verdict: FAIL_EVAL_BINDING
```

## 12_INVARIANTS

- Fixtures are conceptual only.
- Fixtures contain no secrets.
- Fixtures do not create runnable policy files.
- Fixtures do not implement a parser or validator.
- Each fixture has expected verdict and error behavior.

## 13_ESTABLISHED

The YAML draft already defined examples for policy capabilities. This file defines validator fixture expectations around those examples.

## 14_HYPOTHESIS

A future fixture corpus may turn these examples into `.yaml` or `.json` files, but only in a dedicated implementation or fixture GO.

## 15_REMAINING_GAP

No real fixture files exist yet.

## 16_TODO

- Use these examples to seed a future fixture corpus.
- Add additional fixtures for strict workers and Ollama Lab in a future GO if needed.

## 17_RESUME_POINT

Resume point:

```text
Fixtures here are examples, not test inputs.
```

## 18_TO_DOCUMENT

Future fixture files must remain no-secret and must include expected verdict metadata.

## 19_TO_REMEMBER

Conceptual fixtures make implementation safer, but do not replace static validation code.

## RISKS

- À qualifier.
