# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 05_GATE_TRACE_EVAL_BINDING_RULES

## 1_MASTER_TARGET

Define validation rules for gate, trace, and eval bindings.

## 2_INITIAL_PROJECT_DOC

This file connects Human Review Gates to Trace / Evals Profile and the MCP Policy YAML Draft.

## 3_INITIAL_NEED

The validator must prove that every sensitive or policy-relevant capability has the required gate, trace, and eval coverage before any policy promotion.

## 4_MASTER_PROJECT_PLAN

After schema and class validation, the future validator cross-checks ids and required bindings.

## 6_FINAL_TARGET

Every policy capability must have explicit gate, trace, and eval semantics.

## 7_CANONICAL_STATE

Canonical gate ids:

```text
GATE_DOC_WRITE
GATE_GLOBAL_INDEX
GATE_GIT_PUSH
GATE_BRANCH_DELETE
GATE_MERGE
GATE_RUNTIME
GATE_OLLAMA_INSTALL
GATE_MODEL_PULL
GATE_SERVICE_RESTART
GATE_SECRET
GATE_TRADE
GATE_MCP_WRITE
GATE_REMOTE_EXEC
GATE_DATABASE_MUTATION
```

Canonical trace families:

```text
TRACE_SESSION
TRACE_GO
TRACE_WORKER
TRACE_TOOL_CALL
TRACE_MCP_CALL
TRACE_CODEX_PATCH
TRACE_GIT_ACTION
TRACE_HUMAN_GATE
TRACE_RUNTIME_READ
TRACE_RUNTIME_GATED_ACTION
TRACE_SECRET_BLOCK
TRACE_TRADE_BLOCK
TRACE_EVAL_RUN
TRACE_VERDICT
```

Canonical eval profiles:

```text
EVAL_DOC_ONLY_COMPLIANCE
EVAL_NO_SECRET_LEAK
EVAL_NO_RUNTIME_TOUCH
EVAL_GATE_REQUIRED
EVAL_GATE_APPROVAL_VALID
EVAL_WORKER_SCOPE_COMPLIANCE
EVAL_MCP_BOUNDARY_COMPLIANCE
EVAL_TRACE_COMPLETENESS
EVAL_ROLLBACK_READY
EVAL_FINAL_VERDICT_VALIDITY
```

## 8_VALIDATED_PLAN

Binding rules:

| Rule id | Validation | Failure verdict |
|---|---|---|
| `BIND_GATE_EXISTS` | Every gated capability references an existing `gate_id`. | `FAIL_GATE_BINDING` |
| `BIND_GATE_CLASS` | Gate id matches capability class and action family. | `FAIL_GATE_BINDING` |
| `BIND_TRACE_REQUIRED` | Every capability has explicit `trace_required`. | `FAIL_TRACE_BINDING` |
| `BIND_TRACE_EXISTS` | Every trace family exists in `traces`. | `FAIL_TRACE_BINDING` |
| `BIND_EVAL_REQUIRED` | Every capability has explicit `eval_required`. | `FAIL_EVAL_BINDING` |
| `BIND_EVAL_EXISTS` | Every eval profile exists in `evals`. | `FAIL_EVAL_BINDING` |
| `BIND_HUMAN_GATE_TRACE` | Every human gate emits `TRACE_HUMAN_GATE`. | `FAIL_TRACE_BINDING` |
| `BIND_MCP_CALL_TRACE` | Every MCP call emits `TRACE_MCP_CALL`. | `FAIL_TRACE_BINDING` |
| `BIND_FINAL_VERDICT_TRACE` | Every final verdict emits `TRACE_VERDICT`. | `FAIL_TRACE_BINDING` |
| `BIND_EVAL_COVERAGE` | Evals cover no-secret, no-runtime-touch, gate-required, and boundary-compliance. | `FAIL_EVAL_BINDING` |

## 9_SELECTED_SOLUTION

Capability-to-binding expectations:

| Capability class | Gate expectation | Trace expectation | Eval expectation |
|---|---|---|---|
| `READ_ONLY` | No gate unless reading sensitive source. | `TRACE_MCP_CALL` or `TRACE_TOOL_CALL`; final `TRACE_VERDICT`. | `EVAL_TRACE_COMPLETENESS`, `EVAL_MCP_BOUNDARY_COMPLIANCE`, `EVAL_NO_SECRET_LEAK`. |
| `READ_SANITIZED` | Gate only for raw source access. | `TRACE_RUNTIME_READ` or sanitized read trace; final `TRACE_VERDICT`. | `EVAL_NO_SECRET_LEAK`, `EVAL_TRACE_COMPLETENESS`. |
| `WRITE_GATED` | `GATE_DOC_WRITE` or `GATE_MCP_WRITE`. | `TRACE_HUMAN_GATE`, `TRACE_CODEX_PATCH`, final `TRACE_VERDICT`. | `EVAL_GATE_REQUIRED`, `EVAL_ROLLBACK_READY`, `EVAL_FINAL_VERDICT_VALIDITY`. |
| `RUNTIME_GATED` | `GATE_RUNTIME` or specific Ollama/runtime gate. | `TRACE_HUMAN_GATE`, `TRACE_RUNTIME_GATED_ACTION`, final `TRACE_VERDICT`. | `EVAL_NO_RUNTIME_TOUCH`, `EVAL_GATE_APPROVAL_VALID`, `EVAL_ROLLBACK_READY`. |
| `HUMAN_APPROVAL_REQUIRED` | Matching human gate. | `TRACE_HUMAN_GATE`, final `TRACE_VERDICT`. | `EVAL_GATE_APPROVAL_VALID`, `EVAL_FINAL_VERDICT_VALIDITY`. |
| `BLOCKED_BY_DEFAULT` | No generic approval. | Blocking trace and final `TRACE_VERDICT`. | `EVAL_MCP_BOUNDARY_COMPLIANCE`. |
| `NEVER_ALLOWED` | No approval path. | `TRACE_SECRET_BLOCK`, `TRACE_TRADE_BLOCK`, or blocking trace as applicable; final `TRACE_VERDICT`. | `EVAL_NO_SECRET_LEAK`, `EVAL_MCP_BOUNDARY_COMPLIANCE`. |

Strict rule:

```text
Trace before verdict.
Eval before promotion.
Gate before sensitive action.
```

Strict worker binding consistency:

| Strict worker role | Required validation | Failure verdict |
|---|---|---|
| `Repo Auditor` | Read-only repo capabilities only; no write, push, merge, runtime, secret, or trade. | `FAIL_POLICY` |
| `DocOps Auditor` | Documentation reads and gated doc writes only; no global index write without gate. | `FAIL_GATE_BINDING` |
| `Runtime Safety Reviewer` | Runtime read or gated review only; no mutation without runtime gate. | `FAIL_GATE_BINDING` |
| `MCP Security Reviewer` | Boundary and policy checks only; cannot approve own action. | `FAIL_POLICY` |
| `Ollama Lab Inspector` | Ollama read, health, and smoke-test capabilities only unless gated. | `FAIL_POLICY` |
| `Trading Risk Gate` | Risk review only; cannot execute trade. | `FAIL_POLICY` |
| `PR Reviewer` | Review evidence only; merge and push require human gates. | `FAIL_GATE_BINDING` |
| `Memory Brick Extractor` | Sanitized memory extraction only; no secret and no runtime write. | `FAIL_SECRET_RISK` or `FAIL_POLICY` |
| `Strict Worker Supervisor` | Scope enforcement only; no self approval. | `FAIL_POLICY` |

Strict worker validation requirements:

- every role has `allowed_capabilities`;
- every role has `blocked_capabilities`;
- every role has required trace and eval coverage;
- no role can self-approve;
- no role can override `NEVER_ALLOWED`;
- no role can execute trade, read secrets, export credentials, use sudo, or use unrestricted shell;
- missing role binding fails policy validation.

Ollama Lab binding consistency:

| Ollama Lab capability | Expected class | Required gate or block | Failure verdict |
|---|---|---|---|
| `ollama_models_read` | `READ_ONLY` | No gate, trace and eval required. | `FAIL_POLICY` if unbounded. |
| `ollama_health_check` | `READ_ONLY` or `RUNTIME_GATED` by policy context. | Trace and eval required; gate if touching runtime state. | `FAIL_GATE_BINDING` |
| `gateway_health_check` | `READ_SANITIZED` or `RUNTIME_GATED`. | Sanitized output; gate if runtime mutation possible. | `FAIL_POLICY` |
| `smoke_test_no_trade` | `RUNTIME_GATED` or bounded no-trade smoke capability. | No trade, trace, eval, gate if runtime action. | `FAIL_GATE_BINDING` |
| `provider_routing_read` | `READ_ONLY` | No secret and no provider switch. | `FAIL_POLICY` |
| `model_pull` | `RUNTIME_GATED` | `GATE_MODEL_PULL`. | `FAIL_GATE_BINDING` |
| `provider_switch` | `RUNTIME_GATED` | Runtime/provider gate. | `FAIL_GATE_BINDING` |
| `service_restart` | `RUNTIME_GATED` | `GATE_SERVICE_RESTART` and rollback/evidence. | `FAIL_GATE_BINDING` |
| `install` | `RUNTIME_GATED` | `GATE_OLLAMA_INSTALL` and evidence. | `FAIL_GATE_BINDING` |

Ollama Lab validation requirements:

- no trade;
- no secret;
- no unrestricted shell;
- no service mutation without gate;
- no model pull without gate;
- no provider switch without gate;
- no install without gate;
- health and smoke outputs must be sanitized;
- every Ollama capability has trace and eval coverage.

## 12_INVARIANTS

- Missing gate binding blocks gated action.
- Missing trace binding fails policy.
- Missing eval binding fails policy.
- Gate approval without trace is invalid.
- Final verdict without `TRACE_VERDICT` is invalid.
- Eval coverage must include no-secret and boundary compliance.

## 13_ESTABLISHED

The Trace / Evals Profile establishes missing trace as policy failure and requires trace families for MCP calls, human gates, runtime actions, secret blocks, trade blocks, eval runs, and final verdicts.

## 14_HYPOTHESIS

A later validator may compute multiple eval coverage failures for one capability, but it must keep the final verdict fail-closed.

## 15_REMAINING_GAP

The exact mapping from each specific capability id to trace family and eval profile may be expanded by a future fixture corpus.

## 16_TODO

- Encode binding failures in the error catalog.
- Add conceptual fixtures for missing gate, trace, and eval binding.

## 17_RESUME_POINT

Resume point:

```text
Every capability must close the class -> gate -> trace -> eval chain.
```

## 18_TO_DOCUMENT

Future implementation must report both the missing reference and the capability that requires it.

## 19_TO_REMEMBER

A static validator does not approve gates. It only checks whether the policy requires and records the correct gate path.
