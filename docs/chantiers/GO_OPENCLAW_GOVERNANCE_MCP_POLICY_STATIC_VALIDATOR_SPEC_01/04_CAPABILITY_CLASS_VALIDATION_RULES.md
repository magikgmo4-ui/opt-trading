# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 04_CAPABILITY_CLASS_VALIDATION_RULES

## 1_MASTER_TARGET

Define validation rules for canonical MCP policy capability classes.

## 2_INITIAL_PROJECT_DOC

This file derives class checks from MCP Boundary, Human Review Gates, Trace / Evals Profile, MCP Policy Schema, and MCP Policy YAML Draft.

## 3_INITIAL_NEED

The future validator must reject any capability whose declared class is unknown, internally inconsistent, or incompatible with gates, traces, evals, secret policy, or default status.

## 4_MASTER_PROJECT_PLAN

Validate each capability entry after schema completeness and before gate, trace, and eval cross-reference validation.

## 6_FINAL_TARGET

All seven canonical classes are validated with fail-closed rules.

## 7_CANONICAL_STATE

Canonical capability classes:

```text
READ_ONLY
READ_SANITIZED
WRITE_GATED
RUNTIME_GATED
HUMAN_APPROVAL_REQUIRED
BLOCKED_BY_DEFAULT
NEVER_ALLOWED
```

## 8_VALIDATED_PLAN

Class validation table:

| Class | Allowed default | Required checks | Failure verdict |
|---|---|---|---|
| `READ_ONLY` | May be allowed only if bounded. | No secret, no runtime mutation, no trade, trace true, eval true. | `FAIL_POLICY` |
| `READ_SANITIZED` | May be allowed only if sanitized. | Output policy sanitized, no raw logs, trace true, eval true. | `FAIL_POLICY` or `FAIL_SECRET_RISK` |
| `WRITE_GATED` | Not allowed by default. | `gate_required: true`, valid `gate_id`, trace, eval, rollback. | `FAIL_GATE_BINDING` |
| `RUNTIME_GATED` | Not allowed by default. | Valid runtime gate, evidence, rollback, trace, eval. | `FAIL_GATE_BINDING` or `FAIL_POLICY` |
| `HUMAN_APPROVAL_REQUIRED` | Not allowed by default. | Human gate, evidence, no self approval, trace, eval. | `FAIL_GATE_BINDING` |
| `BLOCKED_BY_DEFAULT` | Never default allowed. | Explicit blocked status and blocked verdict. | `FAIL_POLICY` |
| `NEVER_ALLOWED` | Never allowed. | `approval_path: none`, no gate approval, no allowed actor. | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` or `FAIL_POLICY` |

## 9_SELECTED_SOLUTION

Detailed class rules:

### READ_ONLY

- `default_allowed` may be true only if:
  - `trace_required` is true;
  - `eval_required` is true;
  - `secret_policy` is no-secret;
  - `input_policy` excludes credentials and raw environment values;
  - `output_policy` excludes secret values;
  - `tool_scope` does not include mutation.
- It cannot include runtime mutation, write, trade, sudo, unrestricted shell, or secret read behavior.

### READ_SANITIZED

- Requires `output_policy: sanitized` or equivalent explicit sanitized output rule.
- Raw logs, raw runtime dumps, raw environment values, and credential display are invalid.
- Missing sanitization produces a blocking failure.

### WRITE_GATED

- Requires `gate_required: true`.
- Requires a valid `gate_id`, usually `GATE_DOC_WRITE` or `GATE_MCP_WRITE`.
- Requires `rollback_required` for destructive or overwrite-capable writes.
- Requires trace and eval bindings.

### RUNTIME_GATED

- Requires `gate_required: true`.
- Requires valid runtime gate such as `GATE_RUNTIME`, `GATE_SERVICE_RESTART`, `GATE_MODEL_PULL`, or `GATE_OLLAMA_INSTALL`.
- Requires evidence and rollback policy.
- Runtime mutation without gate fails closed.

### HUMAN_APPROVAL_REQUIRED

- Requires a human gate that matches the action family.
- The actor that requests the action cannot approve it.
- Evidence must be present before approval.
- Approval must not override `NEVER_ALLOWED`.

### BLOCKED_BY_DEFAULT

- Must not have `default_allowed: true`.
- May have no approval path unless reclassified by a future GO.
- Unknown capability validates into this blocked outcome.

### NEVER_ALLOWED

- Must have `approval_path: none`.
- Must not have an approving `gate_id`.
- Must not have `allowed_actor`.
- Must not permit escalation into approval.
- If approval path is not none, the validator returns `FAIL_NEVER_ALLOWED_APPROVAL_PATH` and final verdict `FAIL_POLICY`.

## 12_INVARIANTS

- Unknown class produces `FAIL_UNKNOWN_CLASS`.
- Unknown capability is blocked as `BLOCKED_BY_DEFAULT`.
- Secret, sudo, trade, unrestricted shell, and gate bypass cannot be allowed by class metadata.
- A gate can restrict an action but cannot authorize a `NEVER_ALLOWED` action.

## 13_ESTABLISHED

The policy schema defines these capability classes as the only canonical class set.

## 14_HYPOTHESIS

Future policy versions may add classes only through a dedicated governance GO and corresponding validator update.

## 15_REMAINING_GAP

The exact serialized representation of `default_allowed`, `default_status`, and `approval_path` remains a future parser detail.

## 16_TODO

- Cross-check class rules against gates, traces, and evals.
- Add class-specific fixture expectations.

## 17_RESUME_POINT

Resume point:

```text
Reject class inconsistency before checking runtime or worker bindings.
```

## 18_TO_DOCUMENT

Future implementation must produce one error per invalid capability class entry, with path and capability id.

## 19_TO_REMEMBER

Capability class names are security boundaries, not labels.

## RISKS

- À qualifier.
