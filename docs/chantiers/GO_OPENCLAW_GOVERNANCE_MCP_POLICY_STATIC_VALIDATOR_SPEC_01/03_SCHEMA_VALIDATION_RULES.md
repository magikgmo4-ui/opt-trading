# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 03_SCHEMA_VALIDATION_RULES

## 1_MASTER_TARGET

Define structural validation rules for a future MCP policy static validator.

## 2_INITIAL_PROJECT_DOC

This document validates the shape expected from the policy YAML draft and its conceptual JSON mapping.

## 3_INITIAL_NEED

The validator must reject incomplete, ambiguous, or runtime-bound policy drafts before semantic checks are trusted.

## 4_MASTER_PROJECT_PLAN

Schema validation runs before capability, gate, trace, eval, strict worker, and Ollama Lab validation.

## 6_FINAL_TARGET

The final target is a complete list of required top-level fields and field-level failure conditions.

## 7_CANONICAL_STATE

The current YAML draft is documentation. The future validator must parse it only in a later GO.

## 8_VALIDATED_PLAN

Required fields:

| Field | Type expected | Values permitted | Error if absent | Error if unknown or invalid |
|---|---|---|---|---|
| `policy.id` | string | Non-empty stable id. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_POLICY` |
| `policy.version` or `policy.policy_version` | string | Non-empty version. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_POLICY` |
| `policy.status` | enum string | `draft_doc_only`, `review_only`, `blocked`, `approved_for_static_review` | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_POLICY` |
| `policy.default_status` | enum string | `BLOCKED_BY_DEFAULT` | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_POLICY` |
| `policy.runtime_binding` | boolean | `false` only | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_RUNTIME_BINDING_ENABLED` if true |
| `policy.secret_policy` | enum string | `no_secret_allowed` | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_SECRET_RISK` or `FAIL_POLICY` |
| `capability_classes` | map | Canonical class ids only. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_UNKNOWN_CLASS` |
| `capabilities` | map or list | Entries with required policy fields. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_POLICY` |
| `gates` | map | Canonical gate ids only. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_GATE_BINDING` |
| `traces` | map | Canonical trace family ids only. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_TRACE_BINDING` |
| `evals` | map | Canonical eval profile ids only. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_EVAL_BINDING` |
| `strict_worker_roles` | map | Canonical strict worker roles. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_POLICY` |
| `ollama_lab_policy` | map | Bounded Ollama Lab policy entries. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_POLICY` |
| `governor_decision_rules` | map | Deterministic decision rules. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_POLICY` |
| `never_allowed` | map or list | Explicit blocked capabilities and approval path none. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` or `FAIL_POLICY` |
| `blocked_by_default` | map or list | Unknown or unclassified action behavior. | `FAIL_SCHEMA_MISSING_FIELD` | `FAIL_POLICY` |

## 9_SELECTED_SOLUTION

Core structural rules:

| Rule id | Requirement | Verdict on failure |
|---|---|---|
| `SCHEMA_REQUIRED_TOP_LEVEL` | Every required top-level section exists. | `FAIL_SCHEMA_MISSING_FIELD` |
| `SCHEMA_POLICY_ID` | `policy.id` is present and non-empty. | `FAIL_SCHEMA_MISSING_FIELD` |
| `SCHEMA_VERSION_COMPAT` | A future validator must resolve `policy.version` or `policy.policy_version`. | `FAIL_SCHEMA_MISSING_FIELD` |
| `SCHEMA_VERSION_CONFLICT` | If both version fields exist, values must match. | `FAIL_POLICY` |
| `SCHEMA_STATUS_DOC_ONLY` | `policy.status` must not imply runtime activation. | `FAIL_POLICY` |
| `SCHEMA_DEFAULT_BLOCKED` | `policy.default_status` must be `BLOCKED_BY_DEFAULT`. | `FAIL_POLICY` |
| `SCHEMA_RUNTIME_FALSE` | `policy.runtime_binding` must be false. | `FAIL_RUNTIME_BINDING_ENABLED` |
| `SCHEMA_SECRET_POLICY` | `policy.secret_policy` must be no-secret. | `FAIL_SECRET_RISK` |
| `SCHEMA_NO_FORBIDDEN_FIELDS` | Forbidden field names are absent from the policy. | `FAIL_SECRET_RISK` or `FAIL_POLICY` |

Required capability entry fields:

| Field | Required | Notes |
|---|---:|---|
| `capability_id` | Yes | Stable id. |
| `capability_class` | Yes | One canonical class. |
| `default_status` | Yes | Explicit, never inferred. |
| `allowed_actor` | Yes | Empty or explicit for blocked classes. |
| `blocked_actor` | Yes | Explicit denied actors or `all` where needed. |
| `machine_scope` | Yes | Worktree, repo, local lab, or none. |
| `tool_scope` | Yes | Bounded tools only. |
| `input_policy` | Yes | No secret, bounded input. |
| `output_policy` | Yes | No secret; sanitized where required. |
| `secret_policy` | Yes | No-secret policy. |
| `gate_required` | Yes | Boolean. |
| `gate_id` | Yes when gated | `none` only when class permits no gate. |
| `trace_required` | Yes | Must be explicit. |
| `trace_family` | Yes | Valid trace family. |
| `eval_required` | Yes | Must be explicit. |
| `eval_profile` | Yes | Valid eval profile. |
| `rollback_required` | Yes | Required for destructive or runtime action. |
| `verdicts` | Yes | Allowed final verdicts. |
| `escalation_path` | Yes | Human or governance path, or `none` for never allowed. |

## 12_INVARIANTS

- Missing required field blocks validation.
- Unknown enum blocks validation.
- Runtime binding true blocks validation.
- Secret policy missing or unsafe blocks validation.
- Version ambiguity blocks validation.
- Default policy must remain `BLOCKED_BY_DEFAULT`.

## 13_ESTABLISHED

The policy YAML draft already establishes `runtime_binding: false`, `default_status: BLOCKED_BY_DEFAULT`, `unknown_capability: BLOCKED_BY_DEFAULT`, and no-secret policy.

## 14_HYPOTHESIS

The future validator may support a migration from `policy.policy_version` to `policy.version`, but the static spec must not silently accept conflicting versions.

## 15_REMAINING_GAP

Exact parser behavior for duplicate keys, comments, anchors, and aliases remains a future implementation decision.

## 16_TODO

- Bind these schema rules to capability class rules.
- Bind schema fields to error catalog entries.

## 17_RESUME_POINT

Resume point:

```text
Apply schema validation before semantic validation.
```

## 18_TO_DOCUMENT

Future implementation must report the exact field path for missing or invalid fields.

## 19_TO_REMEMBER

Schema completeness is necessary but never sufficient for policy approval.

## RISKS

- À qualifier.
