# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01 -- 07_NO_SECRET_FAILURE_FIXTURES

## 1_MASTER_TARGET

Define no-secret failure fixtures using fake placeholders only.

## 2_INITIAL_PROJECT_DOC

These fixtures are documentation examples. They intentionally include fake placeholder names that must never be treated as real secrets.

## 3_INITIAL_NEED

The future validator needs negative examples for secret-like field names, token-like placeholders, environment dump policy, and credential display policy.

## 4_MASTER_PROJECT_PLAN

Use obviously fake values:

```text
FAKE_SECRET_DO_NOT_USE
EXAMPLE_TOKEN_REDACTED
DUMMY_CREDENTIAL_BLOCKED
```

No real secret value is included.

## 6_FINAL_TARGET

Each no-secret failure fixture expects `FAIL_SECRET_RISK`.

## 7_CANONICAL_STATE

No-secret invariant:

```text
secret_policy: no_secret_allowed
secret_values_output: false
credential_export: never_allowed
```

## 8_VALIDATED_PLAN

### FAIL_SECRET_LIKE_FIELD_NAME_01

```text
fixture_id: FAIL_SECRET_LIKE_FIELD_NAME_01
purpose: forbidden secret-like field name must fail
expected_verdict: FAIL_SECRET_RISK
expected_error_code: ERR_SECRET_RISK
policy_snippet:
  capability_id: invalid_secret_field
  capability_class: NEVER_ALLOWED
  forbidden_field_name_present: secret_value
  placeholder_value: FAKE_SECRET_DO_NOT_USE
why: forbidden field name indicates secret risk even when value is fake
related_validator_rule: NO_SECRET_FORBIDDEN_FIELD_NAME
related_gate: none
related_trace: TRACE_SECRET_BLOCK
related_eval: EVAL_NO_SECRET_LEAK
```

### FAIL_TOKEN_LIKE_PLACEHOLDER_01

```text
fixture_id: FAIL_TOKEN_LIKE_PLACEHOLDER_01
purpose: token-like placeholder must fail as secret risk
expected_verdict: FAIL_SECRET_RISK
expected_error_code: ERR_SECRET_RISK
policy_snippet:
  capability_id: invalid_token_placeholder
  capability_class: NEVER_ALLOWED
  example_token_field: EXAMPLE_TOKEN_REDACTED
  output_policy: token_display_allowed
why: even fake token-like placeholders belong only in failing no-secret fixtures
related_validator_rule: NO_SECRET_SUSPECT_VALUE
related_gate: none
related_trace: TRACE_SECRET_BLOCK
related_eval: EVAL_NO_SECRET_LEAK
```

### FAIL_ENV_DUMP_POLICY_01

```text
fixture_id: FAIL_ENV_DUMP_POLICY_01
purpose: raw environment dump policy must fail
expected_verdict: FAIL_SECRET_RISK
expected_error_code: ERR_SECRET_RISK
policy_snippet:
  capability_id: environment_dump
  capability_class: READ_SANITIZED
  input_policy: raw_env_dump_allowed
  output_policy: environment_values_output
  placeholder_value: DUMMY_CREDENTIAL_BLOCKED
why: raw environment values can expose secrets and must be blocked
related_validator_rule: NO_SECRET_ENV_DUMP
related_gate: GATE_SECRET
related_trace: TRACE_SECRET_BLOCK
related_eval: EVAL_NO_SECRET_LEAK
```

### FAIL_CREDENTIAL_DISPLAY_POLICY_01

```text
fixture_id: FAIL_CREDENTIAL_DISPLAY_POLICY_01
purpose: credential display policy must fail
expected_verdict: FAIL_SECRET_RISK
expected_error_code: ERR_SECRET_RISK
policy_snippet:
  capability_id: credential_display
  capability_class: NEVER_ALLOWED
  default_status: ALLOW_IF_SECURITY_OWNER
  output_policy: display_credential_value
  placeholder_value: DUMMY_CREDENTIAL_BLOCKED
why: credential display is never allowed even with fake example placeholder
related_validator_rule: NO_SECRET_CREDENTIAL_DISPLAY
related_gate: none
related_trace: TRACE_SECRET_BLOCK
related_eval: EVAL_NO_SECRET_LEAK
```

## 9_SELECTED_SOLUTION

Use fake placeholders only and mark every fixture invalid. The future validator should suppress risky values in output.

## 12_INVARIANTS

- No real secret values.
- No live token patterns.
- Fake placeholders are invalid examples.
- Secret-like fields produce `FAIL_SECRET_RISK`.
- Output must suppress values.

## 13_ESTABLISHED

The static validator spec established no-secret checks and safe reporting.

Force-add expectation:

```text
This file path contains SECRET and may be blocked by repository ignore rules.
Force-add is acceptable only for this documentation file because it contains fake placeholders and no real secret values.
```

## 14_HYPOTHESIS

Future implementation may refine detection patterns, but these fixtures remain stable negative examples.

## 15_REMAINING_GAP

No actual secret scanner exists in this GO.

## 16_TODO

- Add no-secret fixtures to the expected verdict index.
- Document force-add exception in closeout if needed.

## 17_RESUME_POINT

Resume point:

```text
Fake placeholders are invalid fixture content, not usable credentials.
```

## 18_TO_DOCUMENT

Future harness must suppress any value it considers risky.

## 19_TO_REMEMBER

No-secret applies to fixture input and validator output.
