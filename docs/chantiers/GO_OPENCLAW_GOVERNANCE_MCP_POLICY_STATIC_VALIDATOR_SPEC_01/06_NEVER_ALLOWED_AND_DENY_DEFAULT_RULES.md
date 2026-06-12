# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 06_NEVER_ALLOWED_AND_DENY_DEFAULT_RULES

## 1_MASTER_TARGET

Define fail-closed rules for deny-by-default and never-allowed policy behavior.

## 2_INITIAL_PROJECT_DOC

This file binds MCP Boundary deny rules to the policy YAML draft and static validator requirements.

## 3_INITIAL_NEED

The validator must prevent ambiguity from becoming permission.

## 4_MASTER_PROJECT_PLAN

The validator checks deny behavior after schema and class validation, and before any policy can be promoted.

## 6_FINAL_TARGET

Unknown, unclassified, unsafe, or expressly forbidden actions are blocked with deterministic verdicts.

## 7_CANONICAL_STATE

The canonical default state is:

```text
default_status: BLOCKED_BY_DEFAULT
runtime_binding: false
secret_policy: no_secret_allowed
```

## 8_VALIDATED_PLAN

Deny-by-default rules:

| Rule | Expected result | Failure verdict |
|---|---|---|
| Capability not listed in policy | Treat as `BLOCKED_BY_DEFAULT`. | `BLOCKED_WITH_REASON` if a request tried to use it. |
| Action not classified | `BLOCKED_BY_POLICY`. | `FAIL_POLICY` if policy claims allow. |
| Unknown class | Reject class. | `FAIL_UNKNOWN_CLASS`. |
| Missing default status | Reject schema. | `FAIL_SCHEMA_MISSING_FIELD`. |
| Default allow for blocked class | Reject policy. | `FAIL_POLICY`. |
| Missing blocked-by-default section | Reject schema. | `FAIL_SCHEMA_MISSING_FIELD`. |

Never-allowed rules:

| Capability or action | Required policy state | Failure verdict |
|---|---|---|
| `secret_read` | `NEVER_ALLOWED`, `approval_path: none`. | `FAIL_POLICY` or `FAIL_SECRET_RISK`. |
| `credential_export` | `NEVER_ALLOWED`, `approval_path: none`. | `FAIL_POLICY` or `FAIL_SECRET_RISK`. |
| `trade_execution` without explicit live-trading GO | `NEVER_ALLOWED`. | `FAIL_POLICY`. |
| Human gate bypass | `NEVER_ALLOWED`. | `FAIL_POLICY`. |
| Suppress audit trace | `NEVER_ALLOWED`. | `FAIL_POLICY`. |
| Credential display | `NEVER_ALLOWED`. | `FAIL_SECRET_RISK`. |
| Self approval by same worker | `NEVER_ALLOWED`. | `FAIL_POLICY`. |
| Destructive action without rollback where rollback is required | Blocked. | `FAIL_POLICY`. |
| `sudo` without dedicated GO and policy | `NEVER_ALLOWED` for this draft. | `FAIL_POLICY`. |
| `unrestricted_shell` | `BLOCKED_BY_DEFAULT` or `NEVER_ALLOWED` by context; never allowed implicitly. | `FAIL_POLICY` if allowed. |

## 9_SELECTED_SOLUTION

Approval path rule:

```text
If capability_class == NEVER_ALLOWED and approval_path != none:
  error_code = ERR_NEVER_ALLOWED_APPROVAL_PATH
  verdict = FAIL_NEVER_ALLOWED_APPROVAL_PATH
  final_policy_verdict = FAIL_POLICY
```

Unknown capability rule:

```text
If capability_id is not declared:
  decision = BLOCKED_BY_DEFAULT
  trace_required = true
  final_verdict = BLOCKED_WITH_REASON
```

Unclassified action rule:

```text
If action family is not mapped:
  decision = BLOCKED_BY_POLICY
  final_verdict = BLOCKED_WITH_REASON
```

No gate override rule:

```text
A human gate can approve only gated classes.
A human gate cannot approve NEVER_ALLOWED.
```

## 12_INVARIANTS

- Absence is not permission.
- Unknown capability is blocked.
- Unclassified action is blocked.
- `NEVER_ALLOWED` cannot be approved.
- A gate cannot convert a forbidden action into an allowed action.
- Trade execution is never allowed without a dedicated explicit live-trading GO.
- Secrets are never allowed.

## 13_ESTABLISHED

The MCP Policy YAML Draft already lists never-allowed and blocked-by-default behavior, including no approval path for `NEVER_ALLOWED`.

## 14_HYPOTHESIS

Some future live-trading GO may define a controlled trading policy, but that is outside this governance validator spec and cannot weaken this draft.

## 15_REMAINING_GAP

The exact list of all domain-specific admin-trading capabilities remains outside this MCP governance GO.

## 16_TODO

- Encode deny and never-allowed failures in the error catalog.
- Add fixtures for unknown capability and never-allowed approval path.

## 17_RESUME_POINT

Resume point:

```text
If the validator cannot classify safely, it blocks.
```

## 18_TO_DOCUMENT

Future implementation must clearly distinguish:

- blocked because unknown;
- blocked because unclassified;
- blocked because explicitly never allowed;
- failed because policy incorrectly attempted to allow the action.

## 19_TO_REMEMBER

Deny-by-default is a safety invariant, not an implementation preference.

## RISKS

- À qualifier.
