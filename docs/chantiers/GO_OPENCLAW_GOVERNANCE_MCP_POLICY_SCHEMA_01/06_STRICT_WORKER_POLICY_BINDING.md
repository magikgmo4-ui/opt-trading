---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_STRICT_WORKER_BINDING
doc_type: strict_worker_policy_binding
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

# 06_STRICT_WORKER_POLICY_BINDING

## 1_MASTER_TARGET

Definir comment un strict worker utilise le schema policy MCP.

## 2_INITIAL_PROJECT_DOC

Sources :

- `GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01/09_STRICT_WORKER_MCP_CONTRACT.md`
- `GO_OPENCLAW_GOVERNANCE_HUMAN_REVIEW_GATES_01/09_STRICT_WORKER_APPROVAL_CONTRACT.md`
- `GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01/03_AGENT_AND_WORKER_TRACE_SCHEMA.md`

## 3_INITIAL_NEED

Garantir qu'un strict worker produit preuves + verdict sans devenir autorite de write, runtime, secret, merge ou trade.

## 4_MASTER_PROJECT_PLAN

Definir :

- role ;
- scope ;
- allowed capabilities ;
- blocked capabilities ;
- output contract ;
- verdict contract ;
- no self-approval rule.

## 6_FINAL_TARGET

Contrat policy borne pour workers.

## 7_CANONICAL_STATE

### Role

Un strict worker est un acteur borne :

```text
one_worker = one_role + one_scope + one_trace + evidence + verdict
```

Il ne change pas de role pendant une mission.

### Scope

`machine_scope` et `tool_scope` doivent etre lus depuis la policy. Tout scope absent est bloque.

### Allowed capabilities par role

| Strict Worker role | Allowed classes | Allowed capabilities | Blocked capabilities | Output contract |
| --- | --- | --- | --- | --- |
| Repo Auditor | `READ_ONLY`, `READ_SANITIZED` | `repo_state`, `branch_state`, `go_index_read`, `machine_split_read` | push, merge, delete, runtime, secret, trade | repo audit + evidence + verdict |
| Documentation Worker | `READ_ONLY`, `WRITE_GATED` after GO scope | `chantier_read`, `create_doc_file`, `update_non_global_chantier_doc`, `create_inbox_entry` | global index write, runtime, secret, trade | doc diff summary + rollback |
| Runtime Safety Reviewer | `READ_ONLY`, `READ_SANITIZED`, `RUNTIME_GATED` review only | `runtime_policy_read`, `runtime_health_summary` from artifacts | restart, install, process kill, runtime mutation | risk verdict |
| MCP Security Reviewer | `READ_ONLY`, `READ_SANITIZED` | manifest read, classification review, blocked action analysis | unrestricted shell, sudo, secret read, MCP write execution | boundary verdict |
| Ollama Lab Reviewer | `READ_ONLY`, `READ_SANITIZED`, gated review only | `model_read`, `ollama_health_check` plan, `gateway_health_check` plan | model pull, provider switch, install, restart without gate | lab safety verdict |
| Trading Risk Gate | `READ_ONLY`, block review | no-trade proof review | trade execution, broker mutation, account secret | trade block verdict |
| Strict Worker Supervisor | `READ_ONLY`, `READ_SANITIZED` | worker trace read, verdict aggregation | approve own runtime, merge, push, trade, secret | supervision report |

### Verdict contract

Allowed worker verdicts :

```text
PASS
FAIL
BLOCKED
NEEDS_HUMAN_GATE
```

Final OpenClaw closeout verdicts remain the canonical PASS/FAIL/BLOCKED list from Trace/Evals.

### Output contract

Every worker output must contain :

```text
worker_id:
role:
scope:
capability_id:
capability_class:
allowed_by_policy:
blocked_by_policy:
evidence_refs:
gate_required:
gate_id:
trace_ref:
worker_verdict:
recommended_governor_decision:
```

## 8_VALIDATED_PLAN

Strict worker decision flow :

```text
read policy -> check scope -> collect evidence -> trace -> decide PASS/FAIL/BLOCKED/NEEDS_HUMAN_GATE -> Governor reviews
```

## 9_SELECTED_SOLUTION

Workers request approvals; they do not grant approvals.

## 12_INVARIANTS

- No self-approval.
- No worker merge.
- No worker push.
- No worker runtime mutation.
- No worker secret value read.
- No worker trade.
- No scope widening during task.

## 13_ESTABLISHED

Strict workers are bounded by the schema through actor, scope, class, gate, trace and eval fields.

## 14_HYPOTHESIS

A future worker registry can bind roles to policy entries.

## 15_REMAINING_GAP

No strict worker registry is generated here.

## 16_TODO

Future GO can map worker roles to concrete skill/tool ids.

## 17_RESUME_POINT

Use this file before delegating a policy-sensitive task to a worker.

## 18_TO_DOCUMENT

Future implementation should reject worker outputs missing role/scope/evidence/verdict.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
Strict workers consume policy, produce evidence and verdict, and never approve their own sensitive actions.
```

## RISKS

- À qualifier.
