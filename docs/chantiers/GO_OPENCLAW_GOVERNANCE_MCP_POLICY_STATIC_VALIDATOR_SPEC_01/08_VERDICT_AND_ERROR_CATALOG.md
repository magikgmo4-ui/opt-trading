# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 08_VERDICT_AND_ERROR_CATALOG

## 1_MASTER_TARGET

Define the standard verdicts and error catalog for the future static validator.

## 2_INITIAL_PROJECT_DOC

The catalog extends the existing governance verdicts with static policy validation verdicts.

## 3_INITIAL_NEED

Every validator failure must be clear, deterministic, no-secret, and actionable without auto-fix.

## 4_MASTER_PROJECT_PLAN

The catalog maps:

- error code;
- severity;
- condition;
- verdict;
- human-readable message;
- safe remediation;
- blocked action.

## 6_FINAL_TARGET

The final target is a reusable verdict and error vocabulary for the future implementation.

## 7_CANONICAL_STATE

Required verdicts for this GO:

```text
PASS_POLICY_STATIC_VALIDATION
FAIL_SCHEMA_MISSING_FIELD
FAIL_UNKNOWN_CLASS
FAIL_GATE_BINDING
FAIL_TRACE_BINDING
FAIL_EVAL_BINDING
FAIL_NEVER_ALLOWED_APPROVAL_PATH
FAIL_SECRET_RISK
FAIL_RUNTIME_BINDING_ENABLED
FAIL_POLICY
BLOCKED_WITH_REASON
NEED_MORE_EVIDENCE
```

## 8_VALIDATED_PLAN

Verdict meanings:

| Verdict | Meaning | Promotion allowed |
|---|---|---:|
| `PASS_POLICY_STATIC_VALIDATION` | Policy passed static checks. | Only to human review, not runtime. |
| `FAIL_SCHEMA_MISSING_FIELD` | Required field absent. | No. |
| `FAIL_UNKNOWN_CLASS` | Capability class is not canonical. | No. |
| `FAIL_GATE_BINDING` | Gate reference or gate requirement invalid. | No. |
| `FAIL_TRACE_BINDING` | Trace reference or trace requirement invalid. | No. |
| `FAIL_EVAL_BINDING` | Eval reference or eval requirement invalid. | No. |
| `FAIL_NEVER_ALLOWED_APPROVAL_PATH` | A never-allowed entry has an approval path. | No. |
| `FAIL_SECRET_RISK` | Secret risk detected. | No. |
| `FAIL_RUNTIME_BINDING_ENABLED` | Policy enables runtime binding. | No. |
| `FAIL_POLICY` | General policy inconsistency. | No. |
| `BLOCKED_WITH_REASON` | Request is blocked with explicit reason. | No. |
| `NEED_MORE_EVIDENCE` | Evidence missing for a decision. | No. |

## 9_SELECTED_SOLUTION

Error catalog:

| error_code | severity | condition | verdict | human readable message | remediation safe | blocked action |
|---|---|---|---|---|---|---|
| `ERR_SCHEMA_MISSING_FIELD` | high | Required field absent. | `FAIL_SCHEMA_MISSING_FIELD` | Required policy field is missing. | Add the field as documentation only. | policy promotion |
| `ERR_POLICY_VERSION_CONFLICT` | high | Version aliases conflict. | `FAIL_POLICY` | Policy version fields conflict. | Keep one canonical matching version. | policy promotion |
| `ERR_RUNTIME_BINDING_ENABLED` | critical | `policy.runtime_binding` is true. | `FAIL_RUNTIME_BINDING_ENABLED` | Runtime binding must remain disabled. | Set runtime binding false in documentation. | runtime use |
| `ERR_SECRET_POLICY_MISSING` | critical | Secret policy absent. | `FAIL_SCHEMA_MISSING_FIELD` | Secret policy is required. | Add no-secret policy. | policy promotion |
| `ERR_SECRET_RISK` | critical | Secret-like content or forbidden secret field detected. | `FAIL_SECRET_RISK` | Secret risk detected; value suppressed. | Remove secret-like content and use safe placeholder. | policy promotion |
| `ERR_UNKNOWN_CLASS` | high | Capability class not canonical. | `FAIL_UNKNOWN_CLASS` | Capability class is unknown. | Use a canonical class or create a future GO. | capability use |
| `ERR_UNKNOWN_CAPABILITY` | medium | Requested capability absent from policy. | `BLOCKED_WITH_REASON` | Capability is unknown and blocked by default. | Add capability through future policy GO. | capability use |
| `ERR_DEFAULT_ALLOW_BLOCKED_CLASS` | high | Blocked class is default allowed. | `FAIL_POLICY` | Blocked classes cannot be default allowed. | Set default allowed false. | capability use |
| `ERR_READ_SANITIZED_OUTPUT` | high | Sanitized read lacks sanitized output policy. | `FAIL_POLICY` | Sanitized read must define sanitized output. | Add sanitized output rule. | data output |
| `ERR_WRITE_WITHOUT_GATE` | high | Gated write lacks valid gate. | `FAIL_GATE_BINDING` | Write-gated capability requires a gate. | Add valid gate id. | write action |
| `ERR_RUNTIME_WITHOUT_GATE` | critical | Runtime-gated capability lacks valid gate. | `FAIL_GATE_BINDING` | Runtime action requires a runtime gate. | Add valid runtime gate id and evidence rule. | runtime action |
| `ERR_MISSING_ROLLBACK` | high | Destructive or runtime action lacks rollback rule. | `FAIL_POLICY` | Rollback rule is required. | Add rollback rule as documentation. | destructive action |
| `ERR_TRACE_REQUIRED_MISSING` | high | Capability lacks explicit trace requirement. | `FAIL_TRACE_BINDING` | Trace requirement is missing. | Add trace_required true and trace family. | policy promotion |
| `ERR_TRACE_FAMILY_UNKNOWN` | high | Trace family is not canonical. | `FAIL_TRACE_BINDING` | Trace family is unknown. | Use canonical trace family. | policy promotion |
| `ERR_EVAL_REQUIRED_MISSING` | high | Capability lacks explicit eval requirement. | `FAIL_EVAL_BINDING` | Eval requirement is missing. | Add eval_required true and eval profile. | policy promotion |
| `ERR_EVAL_PROFILE_UNKNOWN` | high | Eval profile is not canonical. | `FAIL_EVAL_BINDING` | Eval profile is unknown. | Use canonical eval profile. | policy promotion |
| `ERR_NEVER_ALLOWED_APPROVAL_PATH` | critical | `NEVER_ALLOWED` has approval path other than none. | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` | Never-allowed capability cannot be approved. | Set approval path to none. | forbidden action |
| `ERR_GATE_BYPASS_ALLOWED` | critical | Policy allows bypassing a human gate. | `FAIL_POLICY` | Gate bypass is never allowed. | Remove bypass permission. | sensitive action |
| `ERR_SUPPRESS_TRACE_ALLOWED` | critical | Policy allows suppressing audit trace. | `FAIL_POLICY` | Suppressing audit trace is never allowed. | Remove trace suppression rule. | audit suppression |
| `ERR_SELF_APPROVAL` | critical | Worker can approve its own action. | `FAIL_POLICY` | Self approval is never allowed. | Separate requester and approver. | human approval |
| `ERR_OLLAMA_UNBOUNDED_ACTION` | high | Ollama action is not gated or bounded. | `FAIL_POLICY` | Ollama Lab action must be bounded. | Bind to read-only or gated class. | Ollama action |
| `ERR_NEED_MORE_EVIDENCE` | medium | Evidence missing for non-final review. | `NEED_MORE_EVIDENCE` | More evidence is required. | Add non-secret evidence summary. | policy promotion |

## 12_INVARIANTS

- Every failure has one primary verdict.
- Critical errors block promotion.
- No error message contains secret values.
- Remediation is advisory and non-mutating.
- A pass verdict does not authorize runtime use.

## 13_ESTABLISHED

The prior Trace / Evals Profile established final verdict trace requirements. This catalog adds static validation verdicts while preserving blocked and fail verdicts.

## 14_HYPOTHESIS

Future implementation may include machine-readable error ids exactly matching this catalog.

## 15_REMAINING_GAP

No actual error serializer exists in this GO.

## 16_TODO

- Use these error ids in conceptual fixtures.
- Use these verdicts in closeout and future implementation planning.

## 17_RESUME_POINT

Resume point:

```text
Every validator outcome must map to this catalog or a future governance-approved extension.
```

## 18_TO_DOCUMENT

Future implementation must document precedence when multiple errors occur. Recommended precedence is secret risk, runtime binding, never-allowed approval path, schema missing field, unknown class, binding failures, other policy failures.

## 19_TO_REMEMBER

Error reporting is part of the safety boundary because it prevents silent policy drift.

## RISKS

- À qualifier.
