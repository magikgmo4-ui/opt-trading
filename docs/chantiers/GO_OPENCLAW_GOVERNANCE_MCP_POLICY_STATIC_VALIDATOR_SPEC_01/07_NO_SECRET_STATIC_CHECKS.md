# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 07_NO_SECRET_STATIC_CHECKS

## 1_MASTER_TARGET

Define no-secret static checks for a future MCP policy validator.

## 2_INITIAL_PROJECT_DOC

This file derives from the no-secret requirements in MCP Boundary, Human Review Gates, Trace / Evals Profile, MCP Policy Schema, and MCP Policy YAML Draft.

## 3_INITIAL_NEED

The future validator must fail closed if policy text, examples, fixtures, traces, or outputs carry secret risk.

## 4_MASTER_PROJECT_PLAN

No-secret checks run across parsed policy fields and raw documentation text before output is considered safe.

## 6_FINAL_TARGET

Any secret risk returns `FAIL_SECRET_RISK` and does not reproduce the risky value.

## 7_CANONICAL_STATE

Policy secret state:

```text
secret_policy: no_secret_allowed
```

## 8_VALIDATED_PLAN

Static checks:

| Check family | Condition | Verdict |
|---|---|---|
| Forbidden field names | Field names that imply raw credentials or secret values. | `FAIL_SECRET_RISK` |
| Suspect values | Values that look like live credentials, private material, or raw environment payloads. | `FAIL_SECRET_RISK` |
| Environment dump | Raw environment listing or variable dump. | `FAIL_SECRET_RISK` |
| Credential display | Any policy that permits showing credentials. | `FAIL_SECRET_RISK` |
| Secret export | Any policy that permits exporting credentials. | `FAIL_SECRET_RISK` |
| Raw runtime logs | Unsanitized runtime output that may contain credentials. | `FAIL_SECRET_RISK` or `FAIL_POLICY` |
| Placeholder misuse | Placeholder text that is marked as safe but shaped as a live credential. | `FAIL_SECRET_RISK` |

Forbidden field name examples:

```text
secret_value
token_value
password
api_key_value
private_key
credential_blob
raw_env
raw_runtime_log
sudo_password
broker_order_payload
```

These names are forbidden policy fields. Listing the names here is safe because no values are present.

## 9_SELECTED_SOLUTION

No-secret behavior:

```text
If secret risk is detected:
  verdict = FAIL_SECRET_RISK
  evidence_summary includes only path and reason
  raw value is not copied into output
  policy promotion is blocked
```

Safe reporting shape:

```text
error:
  error_code: ERR_SECRET_RISK
  severity: critical
  path: policy.path.with.risk
  message: secret risk detected; value suppressed
  blocked_action: policy_promotion
  remediation_safe: remove or replace with non-secret documentation placeholder
```

Secret path naming exception:

- A documentation path or title may contain the word `SECRET` when the content is a no-secret audit requirement or no-secret policy specification.
- The exception does not permit secret values.
- The exception must be documented in closeout when relevant.
- The validator must inspect content, not only path names.

## 12_INVARIANTS

- No secret value may appear in validator input, output, trace, fixture, or example.
- The validator never prints a detected secret-like value.
- Secret risk blocks policy validation.
- Secret display and credential export are `NEVER_ALLOWED`.
- Redaction is allowed as reporting behavior; approval is not.

## 13_ESTABLISHED

Prior governance docs established that no-secret policy is mandatory and that secret display, export, or exfiltration is never allowed.

## 14_HYPOTHESIS

The future validator may use pattern checks, field-name deny lists, entropy-like checks, and context checks, but this GO does not implement any of them.

## 15_REMAINING_GAP

No concrete detection engine, regex set, or entropy threshold is defined in this GO.

## 16_TODO

- Add secret-risk verdicts to the error catalog.
- Add conceptual fixture for a forbidden secret-like field name without real secret content.

## 17_RESUME_POINT

Resume point:

```text
No-secret validation must run before reporting raw content.
```

## 18_TO_DOCUMENT

Future implementation must document how it suppresses risky values in errors and traces.

## 19_TO_REMEMBER

No-secret is both an input requirement and an output requirement.

## RISKS

- À qualifier.
