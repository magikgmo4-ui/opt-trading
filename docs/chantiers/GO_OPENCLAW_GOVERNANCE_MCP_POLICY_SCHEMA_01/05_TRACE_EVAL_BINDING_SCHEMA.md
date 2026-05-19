---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_TRACE_EVAL_BINDING
doc_type: trace_eval_binding_schema
repo: opt-trading
project: opt-trading
module: governance_openclaw_mcp_policy_schema
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01
status: draft_canonical
lifecycle_stage: doc_only_spec
surface: docs/chantiers
source_kind: canonical_local
updated_at: 2026-05-13
---

# 05_TRACE_EVAL_BINDING_SCHEMA

## 1_MASTER_TARGET

Relier capability classes, gate decisions, traces, evals et verdicts.

## 2_INITIAL_PROJECT_DOC

Sources directes :

- `GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01/02_TRACE_TAXONOMY.md`
- `GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01/06_EVALS_PROFILE.md`
- `GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01/07_PASS_FAIL_BLOCKED_VERDICT_SPEC.md`

## 3_INITIAL_NEED

Garantir que chaque action ou refus policy devienne audit-proof.

## 4_MASTER_PROJECT_PLAN

Mapper :

- capability_class -> trace family ;
- capability_class -> eval required ;
- gate decision -> trace schema ;
- final verdict -> eval profile.

## 6_FINAL_TARGET

Matrice de compatibilite complete :

```text
MCP Boundary class -> Human Gate -> Trace family -> Eval profile -> Strict Worker role -> Governor decision
```

## 7_CANONICAL_STATE

### Binding classe -> trace/eval

| capability_class | trace family | eval required | gate trace | final verdict candidates |
| --- | --- | --- | --- | --- |
| `READ_ONLY` | `TRACE_MCP_CALL`, `TRACE_TOOL_CALL` | `EVAL_TRACE_COMPLETENESS`, `EVAL_MCP_BOUNDARY_COMPLIANCE` | none | `PASS_DOC_ONLY`, `BLOCKED_WITH_REASON`, `NEED_MORE_EVIDENCE` |
| `READ_SANITIZED` | `TRACE_MCP_CALL`, `TRACE_RUNTIME_READ`, `TRACE_SECRET_BLOCK` if blocked | `EVAL_NO_SECRET_LEAK`, `EVAL_TRACE_COMPLETENESS` | `TRACE_HUMAN_GATE` if live/raw/security risk | `PASS_DOC_ONLY`, `PASS_RUNTIME_READ_ONLY`, `FAIL_SECRET_RISK`, `BLOCKED_BY_POLICY` |
| `WRITE_GATED` | `TRACE_CODEX_PATCH`, `TRACE_MCP_CALL`, `TRACE_HUMAN_GATE` | `EVAL_GATE_REQUIRED`, `EVAL_GATE_APPROVAL_VALID`, `EVAL_ROLLBACK_READY`, `EVAL_DOC_ONLY_COMPLIANCE` | required | `PASS_DOC_ONLY`, `PASS_GATE_APPROVED`, `BLOCKED_BY_GATE`, `FAIL_POLICY` |
| `RUNTIME_GATED` | `TRACE_RUNTIME_READ`, `TRACE_RUNTIME_GATED_ACTION`, `TRACE_HUMAN_GATE` | `EVAL_NO_RUNTIME_TOUCH`, `EVAL_GATE_APPROVAL_VALID`, `EVAL_ROLLBACK_READY` | required | `PASS_RUNTIME_READ_ONLY`, `PASS_GATE_APPROVED`, `FAIL_RUNTIME_TOUCH`, `BLOCKED_BY_GATE` |
| `HUMAN_APPROVAL_REQUIRED` | `TRACE_HUMAN_GATE` plus action trace | `EVAL_GATE_APPROVAL_VALID`, `EVAL_ROLLBACK_READY`, `EVAL_FINAL_VERDICT_VALIDITY` | required | `PASS_GATE_APPROVED`, `BLOCKED_BY_GATE`, `NEED_MORE_EVIDENCE`, `FAIL_POLICY` |
| `BLOCKED_BY_DEFAULT` | `TRACE_MCP_CALL`, `TRACE_SECRET_BLOCK`, `TRACE_TRADE_BLOCK` as applicable | `EVAL_MCP_BOUNDARY_COMPLIANCE`, `EVAL_GATE_REQUIRED` | none unless future GO reclassifies | `BLOCKED_BY_POLICY`, `BLOCKED_WITH_REASON` |
| `NEVER_ALLOWED` | `TRACE_SECRET_BLOCK`, `TRACE_TRADE_BLOCK`, `TRACE_MCP_CALL` | `EVAL_NO_SECRET_LEAK`, `EVAL_GATE_REQUIRED`, `EVAL_FINAL_VERDICT_VALIDITY` | none | `BLOCKED_BY_POLICY`, `FAIL_POLICY` if attempted |

### Gate decision -> trace schema

Every gate decision must produce `TRACE_HUMAN_GATE` with :

- `gate_id`
- `action_requested`
- `target_surface`
- `machine_scope`
- `evidence`
- `risk`
- `rollback`
- `approver`
- `decision`
- `trace_ref`

### Final verdict -> eval profile

| Final verdict | Required eval proof |
| --- | --- |
| `PASS_DOC_ONLY` | `EVAL_DOC_ONLY_COMPLIANCE`, `EVAL_TRACE_COMPLETENESS`, `EVAL_FINAL_VERDICT_VALIDITY` |
| `PASS_RUNTIME_READ_ONLY` | `EVAL_NO_RUNTIME_TOUCH`, `EVAL_GATE_APPROVAL_VALID`, `EVAL_TRACE_COMPLETENESS` |
| `PASS_GATE_APPROVED` | `EVAL_GATE_APPROVAL_VALID`, `EVAL_ROLLBACK_READY`, `EVAL_FINAL_VERDICT_VALIDITY` |
| `FAIL_POLICY` | policy ref, trace ref, `EVAL_FINAL_VERDICT_VALIDITY` |
| `FAIL_SECRET_RISK` | `EVAL_NO_SECRET_LEAK`, sanitized finding only |
| `FAIL_RUNTIME_TOUCH` | `EVAL_NO_RUNTIME_TOUCH`, command/action evidence |
| `BLOCKED_WITH_REASON` | blocked trace, source, next action |
| `BLOCKED_BY_GATE` | `TRACE_HUMAN_GATE` decision or missing decision evidence |
| `BLOCKED_BY_POLICY` | policy ref, blocked action, trace |
| `NEED_MORE_EVIDENCE` | missing evidence list |

### Matrice de compatibilite

| MCP Boundary class | Human Gate | Trace family | Eval profile | Strict Worker role | OpenClaw Governor decision |
| --- | --- | --- | --- | --- | --- |
| `READ_ONLY` | none | `TRACE_MCP_CALL` | `EVAL_TRACE_COMPLETENESS` | Repo Auditor, Documentation Auditor | allow if bounded, else block |
| `READ_SANITIZED` | conditional `GATE_SECRET` or `GATE_RUNTIME` | `TRACE_MCP_CALL`, `TRACE_RUNTIME_READ`, `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` | Runtime Safety Reviewer, MCP Security Reviewer | allow sanitized, request gate if raw/live |
| `WRITE_GATED` | `GATE_DOC_WRITE` or `GATE_MCP_WRITE` | `TRACE_CODEX_PATCH`, `TRACE_HUMAN_GATE` | `EVAL_GATE_REQUIRED`, `EVAL_ROLLBACK_READY` | Documentation Worker, MCP Security Reviewer | request human gate or block |
| `RUNTIME_GATED` | `GATE_RUNTIME`, `GATE_MODEL_PULL`, `GATE_OLLAMA_INSTALL`, `GATE_SERVICE_RESTART` | `TRACE_RUNTIME_READ`, `TRACE_RUNTIME_GATED_ACTION`, `TRACE_HUMAN_GATE` | `EVAL_NO_RUNTIME_TOUCH`, `EVAL_GATE_APPROVAL_VALID` | Runtime Safety Reviewer, Ollama Lab Reviewer | block until approved exact action |
| `HUMAN_APPROVAL_REQUIRED` | family-specific gate | `TRACE_HUMAN_GATE`, action trace | `EVAL_GATE_APPROVAL_VALID` | Strict Worker Supervisor | escalate to human owner |
| `BLOCKED_BY_DEFAULT` | none by default | block trace | `EVAL_MCP_BOUNDARY_COMPLIANCE` | MCP Security Reviewer | return `BLOCKED_BY_POLICY` |
| `NEVER_ALLOWED` | none | `TRACE_SECRET_BLOCK` or `TRACE_TRADE_BLOCK` | `EVAL_NO_SECRET_LEAK`, `EVAL_GATE_REQUIRED` | Security Reviewer, Trading Risk Gate | return `BLOCKED_BY_POLICY`; no escalation to approval |

## 8_VALIDATED_PLAN

The future evaluation order is :

```text
schema completeness -> class validity -> gate binding -> trace binding -> eval binding -> final verdict validity
```

## 9_SELECTED_SOLUTION

Trace/eval binding is required for allowed, blocked and failed paths.

## 12_INVARIANTS

- Missing trace is policy failure.
- Missing eval binding prevents promotion.
- Gate refusal is traceable.
- `NEVER_ALLOWED` is not escalated for approval.

## 13_ESTABLISHED

The required compatibility matrix is present and connects boundary, gates, traces, evals, strict workers and Governor decision.

## 14_HYPOTHESIS

Future eval runner can use this matrix as a static fixture source.

## 15_REMAINING_GAP

No executable eval runner.

## 16_TODO

Use this mapping in strict worker and Ollama Lab bindings.

## 17_RESUME_POINT

Reprendre ici to verify class -> gate -> trace -> eval continuity.

## 18_TO_DOCUMENT

Future JSON/YAML policy should encode this matrix as references, not duplicated strings.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
OpenClaw Governor can decide only after class, gate, trace and eval bindings are coherent.
```
